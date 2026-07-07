# 🎧 Beats By Dre — Consumer Insights: Data Analytics Externship

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![TextBlob](https://img.shields.io/badge/TextBlob-NLP-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?logo=matplotlib)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4c9fcf)
![NumPy](https://img.shields.io/badge/NumPy-1.24-013243?logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

End-to-end consumer insights analysis for Beats by Dre's wireless speaker line — cleaning and analyzing **5,127 Amazon reviews** across Beats Pill and four competitor products (JBL Flip 6, JBL Charge 5, UE BOOM 3, Sony SRS-XB100). The project covers data cleaning, exploratory data analysis, TextBlob sentiment analysis, and correlation matrix analysis, producing **30+ visualizations** and a competitive intelligence report.

---

## 📁 Project Structure

```
beats-by-dre-analytics/
├── data/
│   ├── raw/                         # Original scraped Amazon review dataset
│   └── processed/                   # Cleaned, analysis-ready CSVs
├── scripts/
│   ├── consumer_insights_eda.py     # Exploratory Data Analysis pipeline
│   ├── consumer_insights_sentiment.py   # TextBlob sentiment analysis
│   ├── consumer_insights_correlation.py # Correlation matrix analysis
│   └── consumer_insights_visualizations.py  # Matplotlib/Seaborn chart generation
├── notebooks/
│   └── beats_by_dre_correlation_matrix.ipynb  # Jupyter notebook walkthrough
├── visualizations/
│   ├── eda/                         # 13 EDA charts
│   ├── sentiment/                   # 10 sentiment analysis charts
│   └── correlation/                 # 7 correlation charts
├── reports/
│   ├── Beats By Dre EDA.docx
│   ├── Beats By Dre Competitive Analysis Report.docx
│   └── Beats By Dre Externship Wrap Up.docx
└── survey/                          # Customer survey data and documentation
```

---

## 🔍 What Was Analyzed

### Dataset
- **5,127 Amazon reviews** across 5 wireless speaker products
- **Products:** Beats Pill (`B0D6WD2QSQ`), JBL Flip 6, JBL Charge 5, UE BOOM 3, Sony SRS-XB100
- **Fields:** review ID, author, product, star rating, review text, timestamp, verified purchase status, helpful votes

### Phase 1 — Data Cleaning
- Filled missing authors with `'Anonymous'`; dropped reviews with no text content
- Removed duplicates on `review_id`; stripped rating prefixes from titles
- Parsed `"Reviewed in the United States on [Date]"` timestamps to `datetime`
- Applied NumPy mean-imputation for any remaining missing ratings; validated 0–5 range
- Added `review_length` (chars) and `review_length_words` (word count) features

### Phase 2 — Exploratory Data Analysis (`consumer_insights_eda.py`)
- Descriptive statistics: mean, median, mode, variance, std deviation for ratings and review length
- Rating distribution across all products and per-brand breakdowns
- IQR-based outlier detection on both ratings and review length
- Time-series trend of average ratings by product
- Word frequency analysis for 5-star reviews

**Key EDA finding:** The Beats Pill averaged **4.47★** vs. a competitor average of **4.33★**, with JBL Charge 5 as the closest rival at **4.46★**.

### Phase 3 — Sentiment Analysis (`consumer_insights_sentiment.py`)
- Applied **TextBlob** `.sentiment.polarity` and `.sentiment.subjectivity` to all reviews
- Categorized reviews: Positive (polarity > 0.2), Negative (polarity < −0.2), Neutral
- Generated polarity histograms, scatter plots, brand-level box plots, and sentiment trend over time
- Word clouds for positive vs. negative review vocabulary
- Quarterly polarity heatmap across all five brands

**Key sentiment finding:** ~68% of all reviews were Positive; Polarity ↔ Star Rating correlation r = +0.82, confirming TextBlob aligns well with explicit star ratings.

### Phase 4 — Correlation Analysis (`consumer_insights_correlation.py`)
- Built full numeric correlation matrix: rating, review length (chars + words), helpful votes, is_verified, normalized rating
- IQR outlier detection on review length with per-product breakdown
- Per-product correlation breakdowns to surface brand-specific patterns
- Scatter plots: review length vs. rating, rating vs. helpful votes, time vs. rating, verified vs. rating

**Key correlation finding:** Review length shows a weak negative correlation with rating (longer reviews tend to accompany lower scores), while verified purchase status shows slight positive correlation with ratings.

### Phase 5 — Competitive Intelligence
- Benchmark comparison of Beats Pill vs. JBL, UE BOOM, and Sony across price, battery, waterproofing, and audio quality dimensions
- Pain point synthesis from negative review clusters
- Strategic recommendations for product and marketing positioning

---

## 📊 Selected Visualizations

| EDA | Sentiment | Correlation |
|---|---|---|
| Rating over time | Polarity histogram | Full heatmap |
| Rating distribution | Polarity vs. subjectivity scatter | Key metrics heatmap |
| Reviews per product | Polarity by brand | Review length vs. rating |
| Avg rating by brand | Sentiment distribution | Rating vs. helpful votes |
| Word clouds | Positive vs. negative word clouds | Per-product correlation |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, transformation |
| `numpy` | Vectorized operations, outlier detection, normalization |
| `textblob` | NLP sentiment polarity and subjectivity scoring |
| `matplotlib` | Chart generation and saving |
| `seaborn` | Statistical visualizations |
| `wordcloud` | Word cloud generation |
| `jupyter` | Interactive notebook for correlation walkthrough |

---

## 🚀 Run the Analysis

```bash
# Install dependencies
pip install pandas numpy textblob matplotlib seaborn wordcloud

# Download TextBlob corpora
python -m textblob.download_corpora

# Run each pipeline in order
python scripts/consumer_insights_eda.py
python scripts/consumer_insights_sentiment.py
python scripts/consumer_insights_correlation.py
python scripts/consumer_insights_visualizations.py
```

> **Note:** Update the file path in `consumer_insights_eda.py` line 18 from `/home/claude/new_reference_data_for_beats.csv` to your local path, e.g. `data/raw/new_reference_data_for_beats.csv`.

---

## 💡 Key Takeaways

1. **Beats Pill leads on ratings** — highest average star rating among the five products analyzed
2. **Sentiment mirrors star ratings** — TextBlob polarity correlates strongly (r = +0.82) with explicit star ratings, validating the NLP approach
3. **Long reviews signal dissatisfaction** — reviewers who leave negative feedback write significantly more words than satisfied customers
4. **Competitor strength areas** — JBL Charge 5 competes closely on rating; UE BOOM 3 and Sony lead on price-value perception in negative reviews
5. **Verified purchases rate higher** — slight positive correlation between verified purchase flag and star rating

---

## 📬 Contact

**Corey Farrow** · coreyfarrow25@gmail.com · [LinkedIn](https://linkedin.com/in/coreyfarrowjr)
