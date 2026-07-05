# Consumer Sentiment Pipeline: NLP Analysis of 5,127 Wireless Speaker Reviews

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![TextBlob](https://img.shields.io/badge/TextBlob-NLP-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-4c9fcf)

---

## Problem

Beats by Dre needed to understand how their wireless speaker line performed against JBL, UE BOOM, and Sony — not just on star ratings, but on the specific language customers used to describe sound quality, battery life, and build quality. Raw review data existed but had no structure for competitive comparison. The ask: turn 5,000+ unstructured Amazon reviews into a decision-ready competitive analysis.

---

## What It Does

A three-stage Python pipeline that processes raw Amazon review data into competitive intelligence:

1. **EDA** — Cleans 5,127 reviews across 5 products, surfaces rating distributions, review volume trends, and outlier detection using IQR. Produces 13 charts.
2. **Sentiment Analysis** — Applies TextBlob to score every review for polarity (−1 to +1) and subjectivity. Classifies reviews as Positive/Neutral/Negative and compares distributions across brands. Produces 10 charts including word clouds and a quarterly polarity heatmap.
3. **Correlation Analysis** — Builds a full numeric correlation matrix across rating, review length, helpful votes, and verified purchase status. Breaks down per-product to surface brand-specific patterns. Produces 7 charts.

```
data/raw/           → original dataset (5,127 reviews, 5 products)
scripts/            → eda.py, sentiment.py, correlation.py, visualizations.py
data/processed/     → cleaned CSVs output by each stage
visualizations/     → 30 charts organized by analysis type
reports/            → competitive analysis doc, EDA writeup
```

---

## Product Decisions & Tradeoffs

**Why TextBlob over VADER or a fine-tuned model?** TextBlob is interpretable without ML infrastructure — the polarity score is a direct lexicon lookup, which means a product or marketing stakeholder can audit why a review scored −0.4 without needing to trust a black box. VADER would have been stronger for short, informal text, but the priority here was explainability over precision. A v2 would benchmark both against a hand-labeled sample.

**Why separate EDA, sentiment, and correlation into three scripts instead of one?** Each stage produces its own output CSV that can be independently validated before the next stage runs. This mirrors a real data pipeline where you'd want a checkpoint before passing data downstream. The tradeoff is more files to manage, but the debugging benefit outweighs it at this scale.

**Why keep the raw data in the repo?** The raw CSV is 2.3 MB — small enough to commit without LFS, and keeping it means anyone can reproduce every output from scratch without needing access to an external data source. Larger datasets would go behind LFS or a data catalog reference.

**What the data can't answer:** Amazon reviews self-select for strong opinions — 5-star and 1-star clusters are overrepresented relative to actual purchase satisfaction. The sentiment pipeline reflects review language, not a random sample of customer sentiment. This was documented in the competitive analysis report to prevent misuse of the findings.

**Key finding that changed the competitive framing:** Beats Pill led on average star rating (4.47★) but JBL Charge 5 was within 0.01 stars. The real differentiation came from sentiment: Beats reviews concentrated positive language on "bass" and "sound quality," while JBL reviews concentrated on "battery" and "durability." That's a different positioning story than ratings alone — it reframed the analysis from "Beats is winning" to "Beats and JBL are winning on different dimensions."

---

## Tech

| Tool | Purpose |
|---|---|
| `pandas` | Data cleaning, transformation, groupby aggregations |
| `numpy` | IQR outlier detection, normalization, vectorized ops |
| `textblob` | Polarity and subjectivity scoring |
| `matplotlib` / `seaborn` | All 30 charts |
| `wordcloud` | Positive vs. negative vocabulary clouds |

---

## How to Run

```bash
pip install pandas numpy textblob matplotlib seaborn wordcloud
python -m textblob.download_corpora

# Update the data path on line 18 of each script:
# df = pd.read_csv('data/raw/new_reference_data_for_beats.csv')

python scripts/consumer_insights_eda.py
python scripts/consumer_insights_sentiment.py
python scripts/consumer_insights_correlation.py
python scripts/consumer_insights_visualizations.py
```

Each script prints a summary of findings and saves outputs to `data/processed/` and `visualizations/`.
