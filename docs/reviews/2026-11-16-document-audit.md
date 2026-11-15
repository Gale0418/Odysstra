# AUDIT-20261116｜全文件審查、整理與武器移植記錄

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
| `AGENTS.md` | `dbc3c0eeacf5a9d52b4c0ee00595eea685932724fee35a7001b4ce3ddc00c5d2` | 全文覆核；整理／校正 |
| `README.md` | `5442e8ccd6a3b20c3deff117d167aa1516ddc6f0c8cc595baddac2ff35d3dc09` | 全文覆核；整理／校正 |
| `docs/01-vision-and-worldbuilding.md` | `7fa0081701a4749b57bbbf44d53b709397e15fb988943de7d381ba5ebcd9146d` | 全文覆核；整理／校正 |
| `docs/02-galaxy-map-and-generation.md` | `c3ea9fba67347b7b7528ce5160ba564725dad468274af8c488b10c2e7d95ee82` | 全文覆核；保留 |
| `docs/03-factions-and-war-aftermath.md` | `05a9dd8d5cc35158c8c1a3725f79b4a04c23ffd6fd12701f816379a391ee774a` | 全文覆核；整理／校正 |
| `docs/04-fleet-roster-and-population.md` | `df9fcfc1cf62560d4d9914e7b0931f7c7b0c981c15991024ce7f7eb16d5067d1` | 全文覆核；保留 |
| `docs/05-travel-economy-and-logistics.md` | `13cb7b098358de3378af8718898e3554c030d6eb70e5444831f03fb0ee32a40f` | 全文覆核；保留 |
| `docs/06-combat-and-command.md` | `c1a05445b8722522f18e78fb1ed205ac729599bd55c761d2aa2bdbbd126556eb` | 全文覆核；整理／校正 |
| `docs/07-victor-expansion-and-intelligence.md` | `ac4e4ad368ef61fa193fe8d419eee23398cee697ffaab0ad79daf1709125aeb9` | 全文覆核；保留 |
| `docs/08-events-and-encounters.md` | `cfd31c2c636706750c8d3753c2d8c2d46245af9a40fd75b8e492a4b16b50e71c` | 全文覆核；保留 |
| `docs/09-production-risks-and-prototypes.md` | `39432b641d1c7408ab28c76d310dafec42ce923d6ed97b046f49472da1b89ee1` | 全文覆核；整理／校正 |
| `docs/10-ancient-artifacts-and-easter-eggs.md` | `152f081e4fd6e59d2dc141e719d149412ebe6948a17b7446a984180aa0a5f30a` | 全文覆核；整理／校正 |
| `docs/11-decisions-and-open-questions.md` | `c193da2e3a19247e8e612bca7bc37571537476caed51189a756a38ecbf678333` | 全文覆核；整理／校正 |
| `docs/12-naming-and-tone.md` | `dc8c3f8ff54aa8fc0c33b3b9a9f5a3f0a26fde16e965b8c2b5a5cb4bfefaa98b` | 全文覆核；整理／校正 |
| `docs/13-ui-and-technical-architecture.md` | `004923c8ad8ae2160f77ec9e5c92c7c63a6c8abfa80720dbb87ac387b43fba89` | 全文覆核；整理／校正 |
| `docs/14-gameplay-loops-and-design-tensions.md` | `923ba8d4403c7d3ccb03b242800f3bdbcb13d6654e71fba5f23a9aed9869f9c9` | 全文覆核；整理／校正 |
| `docs/15-star-system-catalog.md` | `c9eef74dae9deb4a3494a53a5132053f3b8e4ec1a718df998aa856e189df22be` | 全文覆核；整理／校正 |
| `docs/16-playability-contracts.md` | `f8cb71b9c5c7c0c37c1b1f3ed84e185b03a7815bc3c46a8c6906b7ff12c3f7b7` | 全文覆核；保留 |
| `docs/17-prototype-test-matrix.md` | `d7bd8466f74016348fa1322d14cedee78087b1f90f530c2b9027c449153ce27f` | 全文覆核；保留 |
| `docs/18-weapons-defense-and-tech-doctrine.md` | `0e0599baf64236cc6d768b79335d7207801b39a7eb3fb0cc7973c65f26892f92` | 全文覆核；整理／校正 |
| `docs/19-edible-worlds-and-food-planet.md` | `13638689eafa009a4e8b6722cb01b2171b18e8a1b945696a3108af8762a66571` | 全文覆核；整理／校正 |
| `docs/20-exotic-energy-and-crystal-technologies.md` | `a20efd5c18fb1d7a114625966598ab8ab050a3141ec29a52df3183902dadb709` | 全文覆核；整理／校正 |
| `docs/20-space-solar-and-ac-architecture.md` | `b903eaa8f86067ab29295335ba5f7af9b35d40354dbe4d10ec88e62e2668dfa0` | 全文覆核；整理／校正 |
| `docs/21-ai-society-and-post-work-futures.md` | `7dcdb990283ce1fb50dbd383e9f23a12926b0b63fc6673193e0ab788a42776b5` | 全文覆核；整理／校正 |
| `docs/21-planetary-mining-and-stellar-destruction.md` | `b389723694704ca9eb25da5016e482bf9ffcb597694c0f375c72f63f991bbd89` | 全文覆核；整理／校正 |
| `docs/22-civilization-endgame-tech-tree.md` | `98cecdaafea7a644250d3f665baa749c6aa098e92e026644f19fb832d8370623` | 全文覆核；整理／校正 |
| `docs/23-simulations-and-creator-ethics.md` | `b1f6101a7859a55a392a105741fceb169fc71fddff5fe0a5f3c1bad32fc2fa74` | 全文覆核；整理／校正 |
| `docs/24-odysstra-civilization-integration.md` | `30a7b1f3319a02d9aaf5657131f19c3501d4eea453ba9ff348f5b79a61ce67d0` | 全文覆核；整理／校正 |
| `docs/README.md` | `38e5c14a6687bf5c295fa6a2b6f66f3c3c3f9d0f6ecebdb8606e1965dc42b4b1` | 全文覆核；整理／校正 |
| `docs/cosmo-01-planetary-civilization-and-arcology.md` | `b78b162e57e4fb4e2e191201c6125a8e88c7e92fc13a2a8a7880bb26797b156a` | 全文覆核；整理／校正 |
| `docs/cosmo-02-pelagic-and-atmospheric-arcologies.md` | `1dafa434688c964361ec96b79db6ce7464d56f27a22e6a823f4ab92ed4b805a0` | 全文覆核；整理／校正 |
| `docs/cosmo-03-stellar-megastructures-and-industrial-economy.md` | `54f63b8728099a8d9a90b9d96656188923c66a011e7e726f1a6e102e77a6108c` | 全文覆核；整理／校正 |
| `docs/cosmo-04-titans-mobile-rings-and-peer-war.md` | `6760bbe5ba6fd5ce18ac9d7bbf00eaf88d6a839f36d797818400358f2c372db0` | 全文覆核；整理／校正 |
| `docs/cosmo-05-ocean-and-cloud-city-visual-briefs.md` | `e622807503f211295158ca176427a4d522a9ee4d28d740c83d3040a99990617f` | 全文覆核；整理／校正 |
| `docs/cosmo-06-engineering-validation-and-decision-matrix.md` | `90ec64872405baec79c0c3920e2ef04ec1b004c5449c5d0a8f774dcd05f38d8d` | 全文覆核；整理／校正 |
| `docs/meetings/2026-11-15-session-archive.md` | `6789443ec3c50caea409a29dde17f7d491d9c7f2df7f76eaf2144203e51ecce4` | 全文覆核；保留 |
| `docs/meetings/2026-11-16-ac-postscarcity-creation-archive.md` | `197fe149e5676b34d6eb855c45f5fd79e64b29a178c1ed0e484cdeac1c6c7256` | 全文覆核；整理／校正 |
| `docs/meetings/2026-11-16-civilization-and-megastructures.md` | `0e76519b87b187a2aed3b62583b29aaabcbcaf3b2af38804904166296d8c3416` | 全文覆核；整理／校正 |
| `docs/meetings/2026-11-16-energy-and-planetary-mining.md` | `61f9b3f41cae57cc4932754c962317e0056952f4df89be39323ba13701c8be7a` | 全文覆核；整理／校正 |
| `docs/meetings/2026-11-16-six-systems-reconstruction.md` | `76a89578b4aca990bf19b309dc27b44ca082a27e36bbe9362a649a0d422bce06` | 全文覆核；整理／校正 |
| `docs/warfare-defenses.md` | `3a61bfba0595dba844736474ef16c339313582c9e69ae7bb8d9275ba90853dae` | 全文覆核；整理／校正 |
| `docs/warfare-doctrines.md` | `be2f839b8bf697d896a7bc96812499d80466459c75c804af8c6ac814a0e0e013` | 全文覆核；整理／校正 |
| `docs/warfare-exotic-fleets.md` | `a42c033d24cb703f4c0d447d95938b2e8d5483840896774c909ce2b4a2efbc43` | 全文覆核；整理／校正 |
| `docs/warfare-prototype-tests.md` | `772692a09d62057f243d1bf8feff857bc513859380ad80f1f2457199219de276` | 全文覆核；保留 |
| `docs/warfare-rule-modules.md` | `fb91662586a4d032efb6b2be5f48385b1588e9eb093dc4e31feab84edf64fb62` | 全文覆核；整理／校正 |
| `docs/warfare-weapons.md` | `15a43d8ca7fa0781b188eefab6a069173ed97b1a64998d7b07be39e703c547d2` | 全文覆核；整理／校正 |
