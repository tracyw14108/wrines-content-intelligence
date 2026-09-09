# W.RINES Content Intelligence

W.RINES 的長期社群內容情報庫。這個 repository 不取代 Google Sheets，而是保存「規則、版本、基準、每週快照與分析程式」，讓 Content Intelligence 可以持續迭代、追溯與復原。

## 系統角色

- **Metricool**：W.RINES 自有帳號成效
- **Sociality.io**：競品公開內容、統計與 promoted/organic 判讀
- **Make**：自動收集與寫入
- **Google Sheets**：主資料庫與日常檢視
- **GitHub**：規則版本化、歷史快照、Winner 邏輯與報告程式

## Panel v1.0

| 類別 | 帳號 |
|---|---|
| Owned | @w.rines_ |
| A｜同 Funnel | @yuchuan_0318, @faezhouwu |
| B｜同 Content | @vanessa_style_advisor, @muronginlove, @yuanslook |
| C｜同產業 | @n.2twin, @vacanza_accessory |
| D｜合作延伸 | @mako_artist_, @omikao_makeup |

## Winner 規則

以「每個帳號跟自己的近期基準比」為原則：

- `< 2×` Normal
- `>= 2×` Watch
- `>= 3×` Winner
- `>= 5×` Breakout

Reels 優先以 Views 中位數為基準；Carousel / Photo 優先以 Engagement 中位數為基準。若公開 Views 不完整，改用可取得的 Engagement / Comments / Reposts。Promoted/paid 內容不得直接視為自然 Winner。

## W.RINES 四大內容支柱

1. 第一印象：別人第一眼怎麼感受到我？
2. 氣質：為什麼有些人就是有存在感？
3. 個人風格：我適合什麼？為什麼照抄別人還是不對？
4. 自我表達：我想讓別人看到怎樣的我？

## 目錄

```text
config/                 帳號池、內容支柱、Winner 門檻、分類法
docs/                   系統與資料流程文件
data/baselines/         Baseline 版本
data/weekly-snapshots/  每週原始快照
data/winners/           每週 Winner 報告
data/patterns/          Pattern Library 版本
scripts/                正規化、Winner 判定、週報產生器
.github/workflows/       GitHub Actions
```

## 使用方式

1. Make / Sociality / Metricool 更新 Google Sheets。
2. 將每週快照存成 CSV 到 `data/weekly-snapshots/`（後續可由 Make 直接推送 GitHub）。
3. 執行：

```bash
python scripts/build_weekly_report.py
```

4. 產出的報告會寫入 `data/winners/`。

## 原則

- 不複製競品腳本，只抽象化可學習的 Pattern。
- 不用單一 raw views 判斷跨帳號輸贏。
- promoted / organic 分開看。
- 資料缺失必須標記，不以 0 當作真實低表現。
- 最終目的不是監控競品，而是回答：**市場正在對什麼問題產生反應，而 W.RINES 可以用自己的角度重新回答什麼？**
