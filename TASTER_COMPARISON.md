# Single-Taster Models: Comparison

*Team Rioja, DATA 4401 Project 3. Last updated 2026-11-08.*

Each of us trained location models on reviews from **one taster only**. Holding the taster fixed tests whether the text still shows where a wine comes from once each taster's writing style is no longer a giveaway. This file puts the four notebooks side by side.

| Notebook | Taster | Main countries covered |
|---|---|---|
| [`Schachner_model.ipynb`](Schachner_model.ipynb) | Michael Schachner | Spain 43%, Chile 29%, Argentina 25% |
| [`anna_lee_c_iijima_model.ipynb`](anna_lee_c_iijima_model.ipynb) | Anna Lee C. Iijima | US (New York) 56%, Germany 39%, Eastern Europe |
| [`Roger_Voss_model.ipynb`](Roger_Voss_model.ipynb) | Roger Voss | France 73%, Portugal 22%, Austria 4.5% |
| [`Anne_MW_model.ipynb`](Anne_MW_model.ipynb) | Anne Krebiehl MW | Austria 60%, France 38%, England 2% |

---

## 1. Setup

| | Schachner | Iijima | Voss | Krebiehl |
|---|---|---|---|---|
| **Data** | Team's shared **train** split only | Team's shared train / val / test splits | New 70/15/15 split of the full cleaned data | New 70/15/15 split of the full cleaned data |
| **Reviews** | 9,838 in total. The 3-country model uses 9,536, split 80/20 (7,628 / 1,908) | 2,838 / 578 / 601 | 16,489 / 3,533 / 3,534 | 2,301 / 493 / 494 |
| **Targets** | Country (Spain / Chile / Argentina) | Country, province, region_1 | Country, province, region_1 | Country, province, region_1 |
| **Classes kept** | 3 main countries | At least 20 training reviews (5 countries, 9 provinces, 8 regions) | All (min = 0) | All (min = 0) |
| **Features** | TF-IDF, single words, 10k | TF-IDF, 1–2 word phrases, min_df=3 | TF-IDF, 1–2 word phrases, 20k | TF-IDF, 1–2 word phrases, 20k |
| **Models** | Logistic regression (C=10, balanced) | Logistic regression, tuned over C × class weight; also the all-tasters model | Dummy, logistic regression (C=10), decision tree | Dummy, logistic regression (C=10), decision tree |
| **Test set used?** | No (internal hold-out) | Yes | Yes | No (validation only) |

**Important:** Voss and Krebiehl re-split the full dataset, so their test sets include reviews from the team's shared **training** split. Their scores are fine on their own terms, but they are not on the same held-out set as the Schachner and Iijima results or `tfidf_baselines.ipynb`.

---

## 2. Country results

Each taster's most common country has a very different share (44% to 73%), so raw accuracy can't be compared across tasters. The **gain over always guessing the most common country** is the fairer number.

| Taster | Evaluated on | Always guess most common | Logistic regression | **Gain** | Macro F1 |
|---|---|---|---|---|---|
| Schachner | Internal hold-out | 44.3% (Spain) | 64.9% | **+20.6** | 0.633 |
| Schachner, names removed | Internal hold-out | 44.3% | 53.4% | **+9.1** | 0.521 |
| Iijima | Test | 54.5% (US) | 76.9% | **+22.4** | 0.310 (0.360 with balanced classes) |
| Voss | Test | 72.8% (France) | 83.4% | **+10.6** | 0.439 |
| Krebiehl | Validation | 59.9% (Austria) | 85.1% | **+25.2** | 0.566 |

- Logistic regression beat the decision tree for every taster and target where both were run, as in the all-tasters baselines. The one exception is Krebiehl's 2-class region target (see section 3).
- Iijima's notebook also checked the **all-tasters model** on Iijima's reviews. The single-taster model does slightly better: 76.9% vs 72.9% on test. Training on one taster doesn't lose anything.
- Every model overfits heavily: training accuracy is 97–100% against validation 83–85% for Voss and Krebiehl.

## 3. Province and region results

| Taster | Province accuracy (dummy → model) | Region accuracy (dummy → model) | Notes |
|---|---|---|---|
| Iijima (test) | 55.1% → 64.6% | 53.9% → 57.5% | Regions are nested (Seneca Lake sits inside Finger Lakes, inside New York), and 44% of reviews have no region |
| Voss (test) | 23.5% → 54.9% | 8.0% → 33.1% | 82 provinces and 322 regions, many with very few reviews |
| Krebiehl (val) | 38.3% → 50.9% | 85.6% → 92.0% | ⚠️ Only 2 regions left and 62% of rows missing, so the region number is not meaningful |
| Schachner | Not modeled | Not modeled | |

---

## 4. What the words show

| Taster | Words that point to each country |
|---|---|
| **Schachner** (place and grape names removed) | **Chile:** *olive, herbal, green, bell pepper, vegetal, eucalyptus, coastal, cool*. **Argentina:** *blackberry, jammy, extracted, sweet, heavy*. **Spain:** *yeasty, leesy, bready, brut* (Cava), *nectarine, mature, raisin* |
| **Iijima** | **Germany:** *riesling, kabinett, spätlese, mineral, "drink now through"*. **US:** *chardonnay, cabernet franc, apple*. **Hungary:** *tokaji*. **Romania:** *romanian* |
| **Voss** | **France:** *champagne, château, cru, bordeaux, malbec* (Cahors). **Portugal:** *douro, alentejo, port, quinta*. **Austria:** *grüner, zweigelt, blaufränkisch, screwcap* |
| **Krebiehl** | **Austria:** *grüner, slender, spritz, zesty*. **France:** *dry, residual, sweet* (Alsace sweetness wording). **England:** *mousse, autolysis, bubbles* (sparkling) |

For all four tasters, the strongest clues are **grape names, place names and label terms** (*kabinett*, *quinta*, *château*, *crianza*), not descriptions of how the wine tastes.

---

## 5. Holding the grape fixed too

Two notebooks compared the **same grape from different countries**, with the same taster. This is the cleanest test of origin we have.

| Taster | Comparison | Result |
|---|---|---|
| Schachner | Cabernet Sauvignon, Chile (509) vs Argentina (352) | Only *olive* clearly leans Chile (z ≈ 3.4). Every other word has \|z\| < 2 |
| Schachner | Malbec, Argentina (991) vs Chile (87) | No word reaches \|z\| > 1.5 |
| Iijima | Riesling, Germany vs New York | Riesling-only model gets **73.5%** vs **69.1%** for always guessing Germany (**+4 pts**). The useful words are mostly label terms (*kabinett, spätlese, semidry*) |

**Both analyses agree:** once both taster and grape are fixed, very little origin signal is left in the flavor language.

---

## 6. Overall findings

1. **Within one taster, country is still predictable, but the gain is modest:** 11–25 points over always guessing the most common country.
2. **Most of that gain comes from words that name the answer:** grapes, places and label terms. With those removed (Schachner), the gain falls from 21 to 9 points.
3. **With the grape held fixed too, the gain mostly disappears** (Schachner: Cabernet and Malbec; Iijima: Riesling, +4 points).
4. The 85.8% country accuracy of the all-tasters baseline therefore **overstates real origin signal**. Much of it is taster identity (one taster per region) and grape mix.
5. The clearest real style difference we found is Chile's "green" profile (*olive, herbal, bell pepper, eucalyptus*) in Schachner's reviews.

---

## 7. Issues to fix before the final report

1. **⚠️ `Anne_MW_model.ipynb`, cell 5, overwrites the shared split files** (`data_clean/splits/train|val|test.parquet`) with Krebiehl-only data. Running it breaks `tfidf_baselines.ipynb`, `Schachner_model.ipynb` and `anna_lee_c_iijima_model.ipynb`, and nothing warns you. **Delete that cell.** The Voss notebook already removed its copy. If you ran it, restore the files with `git checkout -- data_clean/splits/`.
2. **Use one data split everywhere.** Voss and Krebiehl should filter the shared splits (as the Schachner and Iijima notebooks do), so every single-taster result is on the same held-out reviews.
3. **Report gain over always guessing the most common country**, not raw accuracy, when comparing tasters.
4. **Krebiehl's region result (92%) shouldn't be presented.** With 2 classes and 62% of rows missing, it means almost nothing.
5. **Krebiehl's notebook has no explanations or conclusions,** and Voss's has setup notes only. Both need a short findings section for the report.
6. **Optional, to make results line up:**
   - Run the name-removal check on Voss, Krebiehl and Iijima, using the name-list approach in `Schachner_model.ipynb` section 5.
   - Add a same-grape comparison for Voss and Krebiehl, for example Voss's Portuguese vs French reds, or Krebiehl's Austrian vs Alsace Riesling.
