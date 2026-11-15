"""Tests for documentation tooling, not for the game."""
import json
import tempfile
import unittest
from pathlib import Path
from check_docs import heading_data, inspect, links, slug


class MarkdownTests(unittest.TestCase):
    def test_unicode_slug(self):
        self.assertEqual(slug('H. 2026-11-16｜三門科技'), 'h-2026-11-16三門科技')

    def test_duplicate_headings(self):
        _, anchors = heading_data('# A\n## Same\n## Same\n## Same-1\n')
        self.assertTrue({'same', 'same-1', 'same-1-1'} <= anchors)

    def test_explicit_anchor(self):
        self.assertIn('stable-id', heading_data('# A\n<a id="stable-id"></a>')[1])

    def test_fence_excluded(self):
        text = '# A\n```md\n# Not a heading\n[bad](missing.md)\n```\n'
        self.assertEqual(heading_data(text)[0], ['A'])
        self.assertEqual(links(text), [])

    def test_inline_code_excluded(self):
        self.assertEqual(links('`[example](absent.md)`'), [])

    def test_balanced_destination(self):
        self.assertEqual(links('[x](docs/name(v1).md)')[0][1], 'docs/name(v1).md')

    def test_reference_links(self):
        self.assertEqual([url for _, url in links('[one][r]\n[r][]\n[r]: docs/a.md')], ['docs/a.md', 'docs/a.md'])

    def test_missing_reference(self):
        self.assertEqual(links('[one][missing]')[0][1], '!undefined-reference:missing')

    def test_image_link(self):
        self.assertEqual(links('![alt](asset.png)')[0][1], 'asset.png')

    def test_angle_destination(self):
        self.assertEqual(links('[x](<a b.md> "Title")')[0][1], 'a b.md')

    def test_external_not_fetched(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.md').write_text('# A\n[x](https://example.invalid/)', encoding='utf8')
            report = inspect(root, False)
            self.assertEqual(report['result'], 'pass')
            self.assertEqual(report['external_links_not_fetched'], 1)

    def test_paths_and_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.md').write_text('# A\n[b](b.md#內容)\n[z](b.md#missing)\n', encoding='utf8')
            (root / 'b.md').write_text('# B\n## 內容\n', encoding='utf8')
            self.assertEqual([e['code'] for e in inspect(root, False)['errors']], ['missing-anchor'])

    def test_missing_target_and_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.md').write_text('# A\n[x](none.md)\n[y](../../outside.md)', encoding='utf8')
            self.assertEqual({e['code'] for e in inspect(root, False)['errors']}, {'missing-target', 'path-outside-repo'})

    def test_registry_coverage_and_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'a.md').write_text('# A', encoding='utf8')
            (root / 'b.md').write_text('# B', encoding='utf8')
            rows = [{'id': 'A', 'path': 'a.md', 'title': 'A'}] * 2
            (root / 'docs/document-map.json').write_text(json.dumps({'documents': rows}), encoding='utf8')
            codes = {e['code'] for e in inspect(root)['errors']}
            self.assertTrue({'duplicate-id', 'duplicate-path', 'registry-coverage'} <= codes)

    def test_registry_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'a.md').write_text('# A', encoding='utf8')
            rows = [{'id': 'A', 'path': 'a.md', 'title': 'A'}]
            (root / 'docs/document-map.json').write_text(json.dumps({'documents': rows}), encoding='utf8')
            self.assertEqual(inspect(root)['result'], 'pass')

    def test_multiple_h1_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.md').write_text('# A\n# B', encoding='utf8')
            self.assertIn('h1-count', {e['code'] for e in inspect(root, False)['errors']})

    def test_unsafe_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.md').write_text('# A\n[x](javascript:alert(1))', encoding='utf8')
            self.assertIn('unsafe-link', {e['code'] for e in inspect(root, False)['errors']})

    def test_encoded_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.md').write_text('# A\n[x](b%20c.md?raw=1#內容)', encoding='utf8')
            (root / 'b c.md').write_text('# 內容', encoding='utf8')
            self.assertEqual(inspect(root, False)['result'], 'pass')


if __name__ == '__main__':
    unittest.main()
