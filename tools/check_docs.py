#!/usr/bin/env python3
"""Offline checks for this repository's Markdown subset; not a game/fact checker.

Supports ATX headings, explicit anchors, inline/image links (balanced targets),
full/collapsed reference links, and fenced code. No network calls or mutations.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXCLUDED = {'.git', 'node_modules', '.venv', '__pycache__'}


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Exclude fenced code while retaining original line numbers."""
    result, fence, length = [], '', 0
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if match:
            marker = match.group(1)
            if not fence:
                fence, length = marker[0], len(marker)
                continue
            if marker[0] == fence and len(marker) >= length and not match.group(2).strip():
                fence, length = '', 0
                continue
        if not fence:
            result.append((number, line))
    return result


def slug(text: str) -> str:
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'!?\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = html.unescape(text).strip().lower()
    text = ''.join(c for c in text if c in '-_' or c.isspace() or
                   unicodedata.category(c)[0] in 'LNM')
    return re.sub(r'\s', '-', text)


def heading_data(text: str) -> tuple[list[str], set[str]]:
    headings, anchors, used = [], set(), set()
    for _, line in prose_lines(text):
        for match in re.finditer(r'<a\s+[^>]*(?:id|name)=["\']([^"\']+)["\']', line, re.I):
            anchors.add(html.unescape(match.group(1)))
        match = re.match(r'^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if not match:
            continue
        if len(match.group(1)) == 1:
            headings.append(match.group(2))
        base = slug(match.group(2))
        candidate, suffix = base, 0
        while candidate in used:
            suffix += 1
            candidate = f'{base}-{suffix}'
        used.add(candidate)
        anchors.add(candidate)
    return headings, anchors


def reference_key(value: str) -> str:
    return ' '.join(value.split()).casefold()


def destination(value: str) -> str:
    value = value.strip()
    if value.startswith('<'):
        end = value.find('>')
        return value[1:end] if end != -1 else value
    return re.split(r'\s+["\']', value, maxsplit=1)[0].strip()


def links(text: str) -> list[tuple[int, str]]:
    lines = prose_lines(text)
    refs: dict[str, str] = {}
    for _, line in lines:
        match = re.match(r'^\s{0,3}\[([^\]]+)\]:\s*(.+)$', line)
        if match:
            refs[reference_key(match.group(1))] = destination(match.group(2))
    result = []
    for number, line in lines:
        if re.match(r'^\s{0,3}\[[^\]]+\]:', line):
            continue
        # Inline code can contain documentation examples; it is not a link.
        line = re.sub(r'(`+).*?\1', '', line)
        for match in re.finditer(r'(?<!\\)\[([^\]\n]*(?:\\.[^\]\n]*)*)\]', line):
            pos = match.end()
            if pos < len(line) and line[pos] == '(':
                depth, end = 1, pos + 1
                while end < len(line) and depth:
                    if line[end] == '\\':
                        end += 2
                        continue
                    depth += (line[end] == '(') - (line[end] == ')')
                    end += 1
                if depth == 0:
                    result.append((number, destination(line[pos + 1:end - 1])))
            elif pos < len(line) and line[pos] == '[':
                end = line.find(']', pos + 1)
                if end != -1:
                    key = reference_key(line[pos + 1:end] or match.group(1))
                    if key in refs:
                        result.append((number, refs[key]))
                    else:
                        result.append((number, f'!undefined-reference:{key}'))
    return result


def inspect(root: Path, require_registry: bool = True) -> dict:
    root = root.resolve()
    paths = sorted(p for p in root.rglob('*.md') if not any(x in EXCLUDED for x in p.relative_to(root).parts))
    texts, errors, warnings = {}, [], []
    for path in paths:
        name = path.relative_to(root).as_posix()
        try:
            texts[name] = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append({'path': name, 'code': 'read-error', 'detail': str(exc)})
    outlines = {name: heading_data(text) for name, text in texts.items()}
    local_count = external_count = 0
    for name, text in texts.items():
        heads, _ = outlines[name]
        if len(heads) != 1:
            errors.append({'path': name, 'code': 'h1-count', 'detail': len(heads)})
        for line, target in links(text):
            if target.startswith('!undefined-reference:'):
                errors.append({'path': name, 'line': line, 'code': 'undefined-reference', 'detail': target})
                continue
            target = html.unescape(target)
            uri = urlsplit(target)
            if uri.scheme or uri.netloc:
                if uri.scheme.lower() in {'javascript', 'data'}:
                    errors.append({'path': name, 'line': line, 'code': 'unsafe-link', 'detail': target})
                else:
                    external_count += 1
                continue
            local_count += 1
            rel = unquote(uri.path)
            resolved = ((root / rel.lstrip('/')) if rel.startswith('/') else (root / name).parent / rel).resolve() if rel else root / name
            if not resolved.is_relative_to(root):
                errors.append({'path': name, 'line': line, 'code': 'path-outside-repo', 'detail': target})
                continue
            if not resolved.exists():
                errors.append({'path': name, 'line': line, 'code': 'missing-target', 'detail': target})
                continue
            if uri.fragment and resolved.suffix.lower() == '.md':
                key = resolved.relative_to(root).as_posix()
                anchor = unquote(uri.fragment)
                if anchor not in outlines.get(key, ([], set()))[1]:
                    errors.append({'path': name, 'line': line, 'code': 'missing-anchor', 'detail': target})
    registry = root / 'docs/document-map.json'
    registry_count = 0
    if registry.exists():
        try:
            rows = json.loads(registry.read_text(encoding='utf-8'))['documents']
            registry_count = len(rows)
            for field in ('id', 'path'):
                duplicates = [k for k, n in Counter(row[field] for row in rows).items() if n > 1]
                if duplicates:
                    errors.append({'path': 'docs/document-map.json', 'code': f'duplicate-{field}', 'detail': duplicates})
            listed = {row['path'] for row in rows}
            if listed != set(texts):
                errors.append({'path': 'docs/document-map.json', 'code': 'registry-coverage',
                               'detail': {'unlisted': sorted(set(texts) - listed), 'missing': sorted(listed - set(texts))}})
            for row in rows:
                if row['path'] in outlines and outlines[row['path']][0] != [row['title']]:
                    errors.append({'path': row['path'], 'code': 'registry-title', 'detail': row['title']})
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append({'path': 'docs/document-map.json', 'code': 'invalid-registry', 'detail': str(exc)})
    elif require_registry:
        errors.append({'path': 'docs/document-map.json', 'code': 'missing-registry', 'detail': 'Expected document inventory.'})
    return {'scope': 'local Markdown paths, anchors, H1 and registry only; no gameplay or external fact verification',
            'markdown_files': len(paths), 'local_links': local_count, 'external_links_not_fetched': external_count,
            'registry_entries': registry_count, 'errors': errors, 'warnings': warnings,
            'result': 'pass' if not errors else 'fail'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--report', type=Path)
    parser.add_argument('--no-registry', action='store_true', help='Only for pre-registry historical baselines.')
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error('--root must be an existing directory')
    report = inspect(args.root, not args.no_registry)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + '\n', encoding='utf-8')
    print(output)
    return 0 if not report['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())
