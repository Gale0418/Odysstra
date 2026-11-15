#!/usr/bin/env python3
"""One-time, guarded documentation curation; executed after manual full review."""
from pathlib import Path
import hashlib
import json
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
original = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8')
            for p in root.rglob('*.md') if '.git' not in p.parts and p.name != 'warfare-modular-blueprints.md' and 'reviews' not in p.parts}
if len(original) != 46:
    raise SystemExit(f'Expected the reviewed 46-file baseline; found {len(original)}. Reconcile first.')
if '## M. 2026-11-16｜整體文件整併與武器藍圖' in original['docs/11-decisions-and-open-questions.md']:
    raise SystemExit('Curation already applied; do not run twice.')

fingerprint = hashlib.sha256()
for path, content in sorted(original.items()):
    fingerprint.update(path.encode()); fingerprint.update(b'\0')
    fingerprint.update(content.encode()); fingerprint.update(b'\0')
if fingerprint.hexdigest() != '6b90bd28cba932b78ad6a41617633e0c1c099bd9962dd06c6cd5d89d44e84ce9':
    raise SystemExit('Reviewed content changed; stop and reconcile instead of overwriting.')
texts = dict(original)

def replace(path, old, new):
    if texts[path].count(old) != 1:
        raise ValueError(f'Expected exactly one target in {path}: {old[:90]}')
    texts[path] = texts[path].replace(old, new, 1)

def append(path, text):
    texts[path] = texts[path].rstrip() + '\n\n' + text.strip() + '\n'

# Unique logical IDs, without changing existing repository URLs.
ids = {
 'docs/19-edible-worlds-and-food-planet.md': 'WORLD-01',
 'docs/20-exotic-energy-and-crystal-technologies.md': 'ENERGY-01',
 'docs/21-planetary-mining-and-stellar-destruction.md': 'ENERGY-02',
 'docs/20-space-solar-and-ac-architecture.md': 'CIV-01',
 'docs/21-ai-society-and-post-work-futures.md': 'CIV-02',
 'docs/22-civilization-endgame-tech-tree.md': 'CIV-03',
 'docs/23-simulations-and-creator-ethics.md': 'CIV-04',
 'docs/24-odysstra-civilization-integration.md': 'CIV-05',
}
for path, ident in ids.items():
    texts[path] = re.sub(r'^# \d+｜', f'# {ident}｜', texts[path], count=1)

# Human-readable cross-references follow target IDs, not duplicate legacy chapter numbers.
link_ids = {Path(p).name: i for p, i in ids.items()}
for name, ident in [('warfare-weapons.md','W01'), ('warfare-defenses.md','W02'),
 ('warfare-doctrines.md','W03'), ('warfare-rule-modules.md','W04'),
 ('warfare-exotic-fleets.md','W05'), ('warfare-prototype-tests.md','W06')]:
    link_ids[name] = ident
for path in original:
    if '/cosmo-' in path:
        link_ids[Path(path).name] = re.search(r'cosmo-(\d+)', path).group(0).upper()

def fix_label(match):
    label, dest = match.group(1), match.group(2)
    name = dest.split('#')[0].split('/')[-1]
    ident = link_ids.get(name)
    if not ident:
        return match.group(0)
    fixed = re.sub(r'^(?:第\s*)?\d+\s*(?:章)?', ident, label)
    return f'[{fixed}]({dest})'

for path in texts:
    texts[path] = re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)', fix_label, texts[path])

replace('docs/11-decisions-and-open-questions.md', 'README.md#戰鬥專題-w2026-11-16-六系補全', 'README.md#weapons')
replace('docs/12-naming-and-tone.md', '\n# ODYSSTRA\n', '\n### ODYSSTRA\n')
replace('docs/warfare-rule-modules.md', '\n# **存在抹殺炮**\n', '\n### 存在抹殺炮\n')
replace('docs/14-gameplay-loops-and-design-tensions.md', '## 以三種不同玩家路線驗證自由度【提案】', '## 以五種不同玩家路線驗證自由度【提案】')
replace('docs/cosmo-06-engineering-validation-and-decision-matrix.md', '**七道約束', '**八道約束')
replace('docs/22-civilization-endgame-tech-tree.md', '的十二階科技樹', '的十三個科技階段（T0–T12）')

# Current canon overrides tentative historical interpretations without deleting history.
append('docs/01-vision-and-worldbuilding.md', '''## 2026-11-16｜神仙打架的明確尺度【使用者確認】

前宗主國與戰勝國**雙方實際使用規則級科技互相作戰**，不只是收藏尚未啟動的傳說武器。材料／能量／自律軍備仍是附庸軍團能理解的日常戰爭語言；兩個霸權能在更高層次攻防，並有同級反制。具體戰敗原因、每種神級裝置的頻率與作用範圍未定，不能因為一方有抹殺炮就說它不可能輸。

使用者以「彈指、啪一下變成灰」說明**抹殺炮的當前消滅效果**；不據此推導歷史、記憶或已造成的因果全部被刪除。歷史構想中「從未存在」的存在抹殺另列於 [W04](warfare-rule-modules.md)。神級戰爭是已確認背景；玩家能否取得、如何操作及何時實裝仍是提案／待決。''')
append('docs/03-factions-and-war-aftermath.md', '''## 與最新戰爭尺度的對接

**【使用者確認】**兩個遠古霸權都在用規則級裝置互扁；前宗主國不是因為完全不會使用神級科技才戰敗。軍備供應、反制、決策與部署等是可用解釋候選，不指定唯一敗因。戰後回收與接管因此可涉及仍能運作的高位軍備，而非僅有傳說。

「玩家位置被看見」與「玩家啟動的神器被識別、被提高處理優先度」不同。舊軍籍、通訊廣播與交易留下的紀錄可以提高後者；不因此推翻戰勝國已具備的全圖艦隊監視。''')
append('docs/10-ancient-artifacts-and-easter-eggs.md', '''## 最新使用邊界：不是只有神話，也不是人人都能用

**【2026-11-16 使用者確認】**前宗主國和戰勝國確實以神級規則科技交戰。上文「奇觀／傳聞／難以理解」描述的是**玩家接觸方式**，不是否定霸權曾實際使用。裝置可在戰後失去操作者、權限、網路或維修，但不需要把全部神器一律寫成半成品。

抹殺炮化灰採 [W04 的最新區分](warfare-rule-modules.md#erasure-scope)：消滅當前目標不自動等於刪除它的歷史。老軍圖若記得一個消失據點，首先可能只是正常保存的舊紀錄，不必額外發明「宇宙唯一不受因果改寫的地圖」。''')

replace('docs/06-combat-and-command.md',
'5. 「能否戰前換旗艦」「旗艦重傷但司令逃生是否算 GG」仍**待決**；使用者已明確說原則是**旗艦沉＝GG**，不要自行改成整支艦隊全滅才敗。',
'5. **旗艦被擊沉＝Game Over 已確認**；不能把司令自動逃生／轉生當成默認例外。「能否在戰前換旗艦」及其條件仍待決；重傷但尚未沉沒不等於已觸發敗北。')
append('docs/06-combat-and-command.md', '''## 武器組合與少量指揮的接點【提案】

[W07｜模組化武器藍圖](warfare-modular-blueprints.md) 借用 Beyond Kronos 的組合語法，讓戰前的配裝與編隊產生有辨識度的戰法。研究主幹仍是三門共用攻防科技；可編輯的藍圖與批次 Doctrine 皆待測，不強制玩家手操每枚導彈，也不採用來源專案的下潛母艦／四船體規則。''')

replace('docs/15-star-system-catalog.md', '高價燃料、古代設施、可隱藏但不保證絕對安全', '高價燃料、古代設施、局部火控可受環境影響，但不遮斷戰勝國全圖艦隊監視')
replace('docs/warfare-exotic-fleets.md', '打撈與避開戰勝國掃描間選擇', '打撈、避開現場巡邏與避免提高戰勝國處理優先度間選擇（不取消全圖監視）')
replace('docs/18-weapons-defense-and-tech-doctrine.md',
'保留使用者的三類名稱與三條科技分工，不混入別的專案砲塔清單。',
'保留使用者三類名稱與三條科技分工；其他專案只在明確授權後另標來源與對接提案，不改寫歷史名錄。本次授權的 Beyond Kronos 組合方式見 W07。')
append('docs/18-weapons-defense-and-tech-doctrine.md', '''## 2026-11-16 整併後的閱讀入口

上文的名稱摘錄保留歷史回查狀態；完整原名以 W01/W02 為準，不再把本章較短的摘錄當成缺名清單。武器配方語法見 [W07](warfare-modular-blueprints.md)，它不新增第七門科技，也不替仍待決的傷害倍率與解鎖公式拍板。''')
append('docs/13-ui-and-technical-architecture.md', '''## 武器資料與介面的補充【提案】

武器藍圖需另存版本、有限觸發圖、每段投送類別與資源預算；艦隊 Doctrine 指向既有版本，不因編輯模板就免費改裝全軍。詳見 [W07](warfare-modular-blueprints.md)。裝配介面先解釋行為與最壞事件數，再考慮複雜視覺編輯器。

文件檢查工具只驗證本倉庫的 Markdown 路徑、錨點、標題和唯一 ID；不能證明遊戲可玩、引擎已選或數值正確。''')
append('docs/09-production-risks-and-prototypes.md', '''## 整併後的原型範圍閘門

五個測試星系中的「出口」只是切片完成點，不把正式終點改成撤離星門。最低玩法優先序不變；W01～W07 是可挑選的戰鬥素材，不要求把所有科技階段和配方做完。

模組武器可先只試一個有限分裂導彈配方、一個貫穿實彈、一個脈衝射線，加上既有點防。若它們不改變玩家戰術，只增加選單工作，應縮小語法。具體組合、觸發預算和學說批次配裝見 [W07](warfare-modular-blueprints.md)，新增 WB 案例全未執行。

本倉庫自動文件檢查和其單元測試屬於**文件品質工具**，與 QA／WD／WB 的遊戲驗收分開計數；CI 綠燈不等於 P-001 已完成。''')

# Rule-level weapons: preserve history, define the correction without inventing mechanics.
p = 'docs/warfare-rule-modules.md'
replace(p, '> **重要：本章屬【歷史腦洞設定／內容庫】。**', '> **重要：本章包含【已確認戰爭背景】、【歷史腦洞設定】與【對接提案／內容庫】。**')
replace(p, '世界觀可以存在古代不可思議科技，不代表海盜與返鄉軍團能量產它們。',
'最新使用者已確認前宗主國與戰勝國都曾用規則級科技交戰；海盜、返鄉軍團是否能使用或量產是另一個未決問題。')
replace(p,
'| **存在抹殺** | 敵人**從來沒有存在過**；單體技能 | 不能等同高傷害炮，也不能等同只是當前瞬間消滅 |',
'| **存在抹殺（歷史版本）** | 原始構想為敵人**從來沒有存在過**；單體技能 | 保存原概念；**不得直接當成最新抹殺炮化灰效果的必然因果規則**，見下方作用域區分 |')
replace(p, '例：直死（必死）+ 輪迴轉生', '僅就歷史候選規則舉例：直死（必死）+ 輪迴轉生')
replace(p, '## 4. 要塞炮應該與艦載炮切開尺度', '''<a id="erasure-scope"></a>
## 3.3 最新釐清：化灰、消失與「從未存在」不是一件事

**【使用者確認】**「抹殺炮就是彈指，啪一下變成灰」確立其當前消滅的觀感與結果。對應本作先記為**當前目標被抹殺／化灰**，不是用極高普通 HP 傷害冒充神級效果；但是否穿越所有防禦、能否復活、灰的物性或殘留量均未被這句話完整定義。

| 語義 | 當前地位 | 不可自行推論 |
|---|---|---|
| 當前抹殺／化灰 | 最新使用者描述 | 不代表記憶、歷史、全部戰果同步消失，也不代表毫無灰塵或能量殘留 |
| 因果／歷史抹除 | 舊「從未存在」構想保留為另一效果候選 | 不因武器叫抹殺就默認包含它；是否同技術不同模式／級別待決 |
| 跨世界線整體消除 | 舊要塞級延伸提案 | 不能自動升成兩方每次射擊皆改寫多重宇宙 |

**【已確認背景】**兩方真的用這類規則科技互相作戰，故不是「老闆有神器卻沒用過」。**【提案】**使用前置條件、部署、反制與作用範圍解釋同級攻防；不能只按名字喊「絕對無敵」並抹掉所有戰略。

原型若將來加入規則事件，需先定義選定目標、作用域、事件順序、反制、結算與紀錄；不得讓遊戲修改磁碟存檔、程式算術或玩家勝利條件來模擬「萬象修改」。旗艦真正被摧毀仍按核心規則判敗；轉生／時間還原不能未經決策就取消它。玩家是否能取得規則裝置仍待決，第一切片不要求實裝。

## 4. 要塞炮應該與艦載炮切開尺度''')
replace(p,
'**【提案】存在抹殺炮與單體存在抹殺模組的分級：**模組按單一具體目標處理；要塞炮可透過宇宙級定位同一身份跨多世界線實例處理。',
'**【保留的歷史分級提案，非最新定案】**曾設想模組按單一目標處理，要塞炮可定位同一身份的跨世界線實例；最新使用者描述的是化灰效果，並未同時採納這套跨宇宙抹除範圍。')
replace(p,
'神級模組／要塞炮可用於**前宗主國殘存遺產、禁區事件、歷史記錄、少量不可掌握威脅**。',
'神級模組／要塞炮是**兩個遠古霸權交戰的背景軍備**；玩家旅途中可透過殘存遺產、禁區、記錄與少量現役高位威脅接觸。背景確認不等於指定每一局出現頻率或每種裝置均可操控。')

# Decision log keeps all original histories, resolves duplicate section identities.
p = 'docs/11-decisions-and-open-questions.md'
replace(p, '## A. 已確認的核心決策（截至 2026-11-15）', '## A. 已確認核心決策（11 月 15 日基線；後續更正見最新摘要）')
replace(p, '## J. 2026-11-16｜AC、後稀缺與創世倫理研究：', '## L. 2026-11-16｜AC、後稀缺與創世倫理研究：')
replace(p, '## COSMO｜2026-11-16 行星理想城、巨構與泰坦研究的決策邊界', '## K. 2026-11-16｜COSMO 行星理想城、巨構與泰坦研究的決策邊界')
latest = '''<a id="current-baseline"></a>
## 最新摘要｜2026-11-16 優先閱讀

以下區分「設定已確認」與「實作未定」。舊紀錄保留於後文，不以章號先後取代最新使用者的直接更正。

| ID | 狀態 | 當前結論 |
|---|---|---|
| CANON-PEER-WAR | 已確認背景 | 前宗主國與戰勝國**雙方實際用神級規則科技互扁**；不是單方神器傳說，也不是前老闆沒做完所以輸 |
| CANON-ERASURE | 已確認效果描述 | 抹殺炮讓當前目標像彈指般化灰；**不自動附帶歷史／記憶／因果抹除**。舊「從未存在」另存為歷史概念 |
| CANON-SCIENCE | 已確認參考 | 材料＝實彈＋裝甲、能量＝射線＋護盾、自律＝導彈＋點防；不是六門獨立科技 |
| CANON-CORE | 維持 | 完整返鄉軍團、同一母星 Happy End、旗艦沉即敗、自由回頭／發展、停更真軍圖、勝方全圖監視與有限調度 |
| AUTH-BK-WEAPONS | 借用授權 | 可參考 Beyond Kronos 的武器組合；來源中的船體、母艦與土星深潛規則**不隨之移植** |
| PROP-BLUEPRINT | 提案／待測 | 有限分裂、追蹤、貫穿、觸發與艦隊學說等對接見 W07；不代表全部首版必做 |

**仍待決：**完整戰鬥操作、傷害公式、每局普通星系數、玩家科技研究與改裝規則、神級裝備准入、引擎／平台與正式數值。文件整理不替這些問題拍板。

'''
texts[p] = texts[p].replace('## A.', latest + '## A.', 1)
append(p, '''## M. 2026-11-16｜整體文件整併與武器藍圖

本輪授權對 Odysstra 全份文件審查整理，並參考 Beyond Kronos 的武器組合。整理保留既有檔案路徑、研究與歷史名稱，使用唯一系列 ID 取代重複的 20／21 章與誤用的武器章號。

[W07](warfare-modular-blueprints.md) 的來源語法、八個配方和 WB-01～12 是**對接提案／未執行測試**。自推進子彈按導彈處理，不繼承父實彈的點防通則；真空不套用土星的風場／壓力；群組學說避免百艦逐艘配置。來源私人倉庫只讀、不整庫搬運。

新增自動文件檢查的通過結果僅代表所檢查的文件結構，不是 QA／WD／WB 遊戲測試通過。完整覆核範圍、限制與未決事項見 [本輪審查報告](reviews/2026-11-16-document-audit.md)。''')

# Research is a comparison layer, not an accidental rejection of fictional canon.
research = list(ids) + [p for p in texts if '/cosmo-' in p]
for path in research:
    lines = texts[path].splitlines()
    lines[1:1] = ['', '> **整併閱讀註（2026-11-16）：**本篇的原作考據／已知物理用於區分證據與創作，不覆蓋[最新本作決策](11-decisions-and-open-questions.md#current-baseline)。兩個霸權使用規則級科技已是背景設定；具體機制、玩家准入與本文工程方案仍須分項確認。數值估算不是性能實測；外部資料的版本與適用條件按原文日期保留。', '']
    texts[path] = '\n'.join(lines) + '\n'
append('docs/19-edible-worlds-and-food-planet.md', '''## 種族與取樣範圍補註

本文以人類生化作可食性研究參照，不把它自動定義為所有飛昇同鄉的生理。落到遊戲需驗證「對本軍團成員確實可食」，不推論所有外星族群都能吃。一次大規模採集的影響取決於採集地、補充速度與局部生態，不能僅由十萬人數量推得必定毀掉整顆行星；也不藉此新增強制道德懲罰。''')

append('AGENTS.md', '''## 文件整併後的工作入口

- [文件總覽](docs/README.md) 按核心、W 武器、世界研究、歷史歸檔分層；唯一 ID 與實際路徑見 `docs/document-map.json`。不再以「第 20 章」之類重複舊編號指路。
- 優先讀決策紀錄的 `current-baseline`：兩方均使用神級科技；抹殺炮化灰不默認抹掉歷史。
- 跨專案借武器先讀 [W07](docs/warfare-modular-blueprints.md)。遵守來源授權範圍，不搬私人對話、秘密或無關設定；Beyond Kronos 的土星環境和母艦模式不是本作規格。
- 本輪新增 `python3 tools/check_docs.py --root .` 與 `python3 -m unittest discover -s tools -p 'test_*.py'`。這兩個命令只驗證**文件工具**；不代表已有遊戲測試、已完成百艦戰鬥或已選引擎。
- 新增文件要同步唯一 ID、索引及狀態。變更既有長篇研究時保留來源／假設；需要調整原設定就記更正，不偷偷用新提案覆寫歷史原名。''')

for path, text in texts.items():
    (root / path).write_text(text, encoding='utf-8')

# Preserve paths; replace a sprawling append-only landing page with a stable entry point.
(root / 'README.md').write_text('''# ODYSSTRA｜銀河歸途

> **The war is over. Bring them home.**  
> 帝國倒了，軍團還在。帶他們回家。

**一支完整遠征軍、一份停止更新的軍用星圖，以及半個銀河的歸途。**

第三次銀河大戰結束。前宗主國與戰勝國以神級規則科技交鋒，前宗主國敗亡；玩家帶著仍有作戰能力的約百艘星艦、十萬名同鄉，穿越昔日友軍的內戰、海盜與逐步接管的戰勝國，返回共同出生的母星。

這是 **2D 太空艦隊沙盒的設計資料庫**，不是已完成遊戲。引擎、戰鬥操作、正式數值與可執行版本尚未定案／實作；文件檢查通過不等於玩法驗收。

## 從這裡開始

| 想看什麼 | 入口 |
|---|---|
| 完整閱讀地圖 | [分層文件索引](docs/README.md) |
| 目前到底拍板什麼 | [最新決策摘要](docs/11-decisions-and-open-questions.md#current-baseline) |
| 要先做出什麼 | [P-001、風險與範圍](docs/09-production-risks-and-prototypes.md) |
| 武器怎麼配才好玩 | [三攻三防總論](docs/18-weapons-defense-and-tech-doctrine.md) → [W07 模組藍圖](docs/warfare-modular-blueprints.md) |
| 前老闆與敵人在互扁什麼 | [W04 規則級科技與抹殺炮](docs/warfare-rule-modules.md) |
| 這輪整理改了什麼 | [全文件審查報告](docs/reviews/2026-11-16-document-audit.md) |
| 開發者／AI 交接 | [AGENTS.md](AGENTS.md) |

## 核心不能做歪

| 項目 | 基線 |
|---|---|
| 軍團 | 約十萬同鄉、百艘左右完整軍團；開局配船可調，少後勤艦可少帶人，不強制全面殘血 |
| 目標與失敗 | 共同母星抵達即 Happy End；玩家旗艦被擊沉即 Game Over，不自動加最後 Boss 或轉生免敗 |
| 自由度 | 探索、回頭、停留、採礦、回收、交易、搶劫、維修、造船；不是單向關卡或道德考卷 |
| 星圖 | 精密歷史軍圖停更，不是故意騙人；30 個命名地標，另有低價值程序星系。「70 種」不等於已定每局100顆 |
| 戰勝國 | 有全圖艦隊監視；依遊戲時間、威脅、距離與可用部隊接管，不無理由全圖瞬移 |
| 後勤 | 食物列印＋抽象原料；燃料可買或恆星採集；人口聚合記帳，不做十萬個 NPC |
| 科研 | 材料→實彈＋裝甲；能量→射線＋護盾；自律→導彈＋點防。三門可偏科 |
| 戰鬥／藍圖 | 自動交戰與少量指令是候選，具體操作未定；Beyond Kronos 組合語法已獲借用授權，對接配方仍待測 |
| 超文明 | 雙方確實使用神級科技；玩家取得與使用條件另論。抹殺炮化灰不自動等於歷史抹除 |

## 文件分層與名稱

核心 01–18 保留玩法方向；**W01–W07** 管武器與戰法；**WORLD／ENERGY／CIV／COSMO** 保存奇觀、工程與跨作品研究；會議歸檔保存演變，不當開發待辦。全部原有長篇研究保留在原路徑，閱讀以唯一 ID 為準，避免舊 20／21 章混淆。

Odysstra 由 **Odyssey × Astra** 融合造詞，中文《銀河歸途》。[名稱與文案](docs/12-naming-and-tone.md)；商標、網域與商店獨占性尚未完成正式查核。

**優先序：最新使用者決定 → 決策紀錄 → 對應系統章節 → 提案／研究／歷史。** 歸檔授權不等於全數採納；新點子先標提案，遊戲測試未執行就標 Not run。

## 文件品質檢查

```sh
python3 tools/check_docs.py --root .
python3 -m unittest discover -s tools -p 'test_*.py'
```

以上是無網路、無第三方依賴的文件路徑／錨點／ID 檢查及其測試，不驗證外部科學事實，也不執行遊戲。沒有預設部署、收費 API 或離線追殺機制。GitHub 文件 CI 僅產生短期審查報告與文件快照。
''', encoding='utf-8')

# Registry also drives the index. Every Markdown file is catalogued exactly once.
entries = []
for path in sorted(p.relative_to(root).as_posix() for p in root.rglob('*.md') if '.git' not in p.parts and 'reviews' not in p.parts):
    title = (root / path).read_text(encoding='utf-8').splitlines()[0][2:]
    if path == 'README.md': ident, group, state = 'HOME', 'governance', '入口'
    elif path == 'AGENTS.md': ident, group, state = 'GUIDE', 'governance', '維護指引'
    elif path == 'docs/README.md': ident, group, state = 'INDEX', 'governance', '索引'
    elif path in ids: ident, group, state = ids[path], 'research', '研究／提案；個別已確認背景另標'
    elif '/warfare-' in path:
        ident, group, state = title.split('｜')[0], 'warfare', '歷史設定／對接提案；遊戲測試未執行'
    elif '/cosmo-' in path:
        ident, group, state = title.split('｜')[0], 'research', '研究／提案／視覺要求'
    elif '/meetings/' in path:
        ident, group, state = 'HIST-' + Path(path).stem, 'history', '摘要歸檔，非逐字稿'
    else: ident, group, state = 'C' + Path(path).name[:2], 'core', '已確認基線與提案分開標記'
    entries.append({'id': ident, 'path': path, 'title': title, 'category': group, 'status': state})
report_path = 'docs/reviews/2026-11-16-document-audit.md'
report_title = 'AUDIT-20261116｜全文件審查、整理與武器移植記錄'
entries.append({'id': 'AUDIT-20261116', 'path': report_path, 'title': report_title, 'category': 'governance', 'status': '文件審查記錄，非遊戲驗收'})
# Index title is replaced below; keep registry consistent.
for row in entries:
    if row['id'] == 'INDEX': row['title'] = 'ODYSSTRA｜分層文件索引與狀態'

index = '''# ODYSSTRA｜分層文件索引與狀態

> 整理日：2026-11-16。所有既有文件路徑保留；**唯一系列 ID** 取代重複的研究章號。數字、範例、完整清單與文件篇幅都不代表功能已完成。

## 建議閱讀順序

先讀 [最新決策](11-decisions-and-open-questions.md#current-baseline) → [世界觀](01-vision-and-worldbuilding.md) → [P-001](09-production-risks-and-prototypes.md)。設計武器時讀 18 → W01/W02/W03 → W07；需要理解霸權戰爭才讀 W04 和 COSMO。研究與歷史不是一次實作的工作清單。

## 狀態與證據

| 標記 | 意義 |
|---|---|
| 已確認 | 使用者親自決定的背景、意圖或規則；仍須區分背景存在與玩家可用 |
| 歷史設定／指定參考 | 過去創作保留，若後來更正以最新決策為準 |
| 方向／提案／內容庫 | 候選解法、配方、事件與世界素材，不是開發承諾 |
| 待決／測試預設 | 未知保留未知；原型暫定數字不當正式數值 |
| 研究／條件演算 | 原作資料、現行物理與明示假設；不代替本作虛構規則 |
| Not run | 遊戲驗收案例尚未執行；文件 CI 成功不改變它 |

**最新使用者決策 > 決策紀錄 > 系統章節 > 提案／研究／歷史。** 軍團返鄉核心、全圖監視、三門共用攻防與母星 Happy End 不因跨作品研究變更。化灰抹殺和歷史抹除分開。
'''
for group, heading in [('core','核心企劃 01–18'), ('warfare','武器與艦隊專題 W'), ('research','世界觀與研究 WORLD／ENERGY／CIV／COSMO'), ('history','歷史會議摘要'), ('governance','維護、索引與審查')]:
    index += ('\n<a id="weapons"></a>\n' if group == 'warfare' else '')
    index += f'\n## {heading}\n\n| ID | 文件 | 狀態 |\n|---|---|---|\n'
    for row in sorted(entries, key=lambda r: r['id']):
        if row['category'] != group: continue
        path = row['path']
        link = path[5:] if path.startswith('docs/') else '../' + path
        index += f"| {row['id']} | [{row['title']}]({link}) | {row['status']} |\n"
index += '''
## 同步與查核

機器可讀清單為 [document-map.json](document-map.json)，每個 Markdown 路徑僅一筆。新增文件時同時維護此索引與清單。原本的第 19 章美食世界現為 WORLD-01；兩組 20／21 章分屬 ENERGY 與 CIV；W/COSMO 引用不再冒用普通章號。歷史檔名保留以保護既有連結。

[AGENTS.md](../AGENTS.md) 記錄協作規則；[本次審查](reviews/2026-11-16-document-audit.md) 記錄範圍、修正與限制。外部來源保留原文日期；未對每一個外部網站逐頁重做查證，不把原作研究誤稱成已驗證本作數值。
'''
(root / 'docs/README.md').write_text(index, encoding='utf-8')
(root / 'docs/document-map.json').write_text(json.dumps({'schema_version': 1, 'updated': '2026-11-16', 'documents': entries}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

report = f'''# {report_title}

> 審查日：2026-11-16。工作性質：全文設計覆核、文件整併與受控借用。**不是遊戲實作、數值驗證或法律／科學全項認證。**

## 範圍與來源

Odysstra 覆核基線 `c4d5582d3eb0d1b9bb62da769c9dd006a3b18730`：46 份 Markdown、519,646 bytes，逐份讀取。為本次審查新增的唯讀 CI 快照提交 `7f1f5143acc2c5226cebe3a07b5af8091d7a306d` 不改這46份正文。下方列出每份覆核路徑與基線 SHA-256，可與 Git 歷史及快照比對。

Beyond Kronos 只讀指定武器／配裝／防禦文件及相關正典界線，來源快照 `d345eccbf5885f0bd706b8a81d36c65a4a5c55bd`。使用者授權借武器設計，不代表公開整個私人倉庫；本次僅以 W07 原創化轉述相關設計，不搬無關世界觀或私人聊天。

## 發現與處理

| ID | 問題 | 處理 |
|---|---|---|
| DOC-01 | 不同研究共用20／21章、索引同一文件重複、W專題被叫19～24 | 使用 WORLD／ENERGY／CIV／COSMO／W 唯一 ID；原路徑保留，重寫導航與目標標籤 |
| DOC-02 | 決策紀錄重複J節、入口長篇追加、歷史與最新決策混讀 | 統一J/K/L/M，置頂最新摘要，AGENTS與索引提供分層入口 |
| DOC-03 | 名稱章與要塞炮章各多一個H1 | 降為子標題；單篇一主題標題 |
| CANON-01 | God級軍備仍只被描述成傳聞／遺物 | 明寫兩方曾實際使用；玩家准入與原型仍待決，不能把範圍控制誤寫成削弱世界觀 |
| CANON-02 | 舊存在抹殺＝從未存在，被直接套到最新抹殺炮 | 化灰是當前效果；歷史／因果刪除另存舊構想，無自動宇宙重算或地圖免疫 |
| CANON-03 | 旗艦沉即敗旁還留「逃生是否GG」疑問 | 維持擊沉即敗；只有戰前換旗艦等條件待決，不默認轉生免敗 |
| CANON-04 | 部分殘骸／隱蔽文案暗示可躲掉戰勝國全圖監視 | 改為局部巡邏、火控品質與戰略優先度，不修改監控前提 |
| SCOPE-01 | 研究的現行物理邊界可能被當成否定虛構神級科技 | 研究篇增加解讀註；觀測、條件演算、原創規則與玩家可用性分層 |
| SCOPE-02 | 完整武器名單、32QA、21WD、70普通組合被誤當首版工作量 | 交叉參照最新完整名錄，保留Not run及P-001切片；70單位仍待決 |
| EDIT-01 | 五種玩家風格標三種；T0–T12卻稱十二階；八條約束稱七條 | 校正文字計數，不改內容與正式數值 |
| PORT-01 | 模組分裂／追蹤可能穿透三攻三防分類 | 按每段投送分類，主動子彈是導彈；加入觸發、資源與事件預算 |
| PORT-02 | 土星流場與深度限制可能誤進太空 | W07明列真空改寫、不移植CSG／十層下潛／四船體；學說批次配裝是提案 |

## 新增內容，不偷換採納狀態

W07 提供一套七段可讀語法、八個配方候選及 WB-01～12 案例。新鮮感在分裂／穿透／觸發／編隊互補，不在新建第七門科研。所有配方、區域細節和資料欄位仍待測，沒有製作可執行武器。

現有46份路徑全部保留；長篇研究未被刪章縮成摘要。根入口和索引重整是導航去重，正文的原名／研究／歷史仍在原文件或Git基線中可追溯。新系列名稱只改邏輯編號，不改來源作品與作者意思。

## 驗證及限制

- 新增 `tools/check_docs.py` 檢查所支援 Markdown 語法的本機連結、錨點、H1與唯一登錄；不連線探測外站，也不是完整 CommonMark 渲染器。
- 新增18個文件工具單元測試；實際輸出應查本次執行日誌／GitHub工作流，不把這18個計入遊戲測試通過數。
- 原基線工具掃描發現2個多H1問題；誤導的章號、重複索引及語義矛盾是人工覆核發現，不假稱全由lint抓到。
- QA 32項、WD-01～21和新增WB-01～12仍未執行；沒有遊戲可玩性、效能、百艦60FPS或數值平衡實測。
- 外部資料採**選點核查＋保留來源**，不是所有原作與科學論文重新全面驗證。此次核對官方Nomads推出資訊與4.5.4公告，僅支持該版本／日期陳述，不為其餘具體機制背書。所有公式仍要看原假設。
- 官方版本對照入口：[Paradox發行公告](https://www.paradoxinteractive.com/media/press-releases/paradox-interactive/paradox-interactive-launches-major-expansion-and-free-update-for-stellaris)、[Nomads官方頁](https://www.paradoxinteractive.com/games/stellaris/add-ons/stellaris-nomads)、[官方Steam公告頁](https://steamcommunity.com/app/281990/allnews/)。不把不斷變動的公告入口當作遊戲規格。

## 仍應留白，不用再開一場設定內戰

戰鬥自動化程度／同場部署量、普通星系每局數、研究與裝備解鎖、旗艦戰前轉乘、合法藍圖與耗時／成本、超文明規則作用域及玩家准入、引擎／平台與目標效能。下一步仍是五個測試星系與小型戰鬥，不是先做整個宇宙的規則編譯器。

## 全文覆核清冊（基線，不是新版本雜湊）

| 原有路徑 | 基線 SHA-256 | 本輪處置 |
|---|---|---|
'''
for path, old in sorted(original.items()):
    digest = hashlib.sha256(old.encode('utf-8')).hexdigest()
    new = (root / path).read_text(encoding='utf-8')
    status = '全文覆核；整理／校正' if new != old else '全文覆核；保留'
    report += f'| `{path}` | `{digest}` | {status} |\n'
(root / report_path).parent.mkdir(parents=True, exist_ok=True)
(root / report_path).write_text(report, encoding='utf-8')
print('Curated reviewed documentation; gameplay remains unimplemented.')
