# Consumer Sentiment Pipeline: Data-Informed Competitive Positioning for Beats by Dre

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![TextBlob](https://img.shields.io/badge/TextBlob-NLP-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)

> **Role context:** Data analytics externship — built and operated the analysis pipeline, synthesized findings into a competitive positioning recommendation.

---

## Problem

Beats by Dre had star rating data for their Pill speaker and four competitors (JBL Flip 6, JBL Charge 5, UE BOOM 3, Sony SRS-XB100), but star ratings don't tell you *why* customers feel the way they do or which product attributes actually drive satisfaction. The question: where is Beats outperforming competitors in customer language, and where are competitors building stronger associations that could threaten Beats' positioning?

This is a product question dressed as a data question. The analysis was the method; the deliverable was a positioning recommendation.

---

## Approach

Built a three-stage Python pipeline on 5,127 Amazon reviews:

**Stage 1 — EDA:** Cleaned and structured raw review data. Surfaced rating distributions, review volume by product, verification rates, and review length patterns. IQR outlier detection on both ratings and review length.

**Stage 2 — Sentiment Analysis:** Applied TextBlob NLP to score every review for polarity (−1 to +1) and subjectivity. Classified reviews as Positive/Neutral/Negative. Compared sentiment distributions across brands and tracked polarity trends over time.

**Stage 3 — Correlation Analysis:** Built a full numeric correlation matrix across rating, review length, helpful votes, and verified purchase status. Broke down per-product to surface brand-specific patterns. Generated word frequency analysis to identify which specific attributes each brand "owned" in customer language.

---

## Product Decisions (as the analyst)

**Why TextBlob over a fine-tuned model?** The audience for this analysis was a product and marketing team, not a data science team. TextBlob's polarity scores are auditable — a stakeholder can look at a specific review and understand why it scored −0.4 without trusting a black box. Interpretability > precision for a findings presentation.

**Why stage the pipeline instead of one script?** Each stage outputs a validated CSV before the next stage runs. This mirrors how you'd structure a real data pipeline where a downstream team might consume Stage 1 output independently (e.g., marketing using the EDA data for a different analysis).

---

## Outcome: What the Data Changed

Star ratings alone suggested Beats Pill was leading (4.47★ vs. 4.46★ for JBL Charge 5 — effectively tied). Sentiment and word frequency analysis told a different story:

- **Beats "owned" sound quality and bass** in positive review language — strong emotional association with audio performance
- **JBL owned battery and durability** — customers chose JBL language when talking about reliability and longevity
- **Implication:** Beats' competitive risk isn't a better-sounding speaker — it's JBL building a "lasts longer, works everywhere" positioning that appeals to a different buyer motivation entirely

The competitive analysis report reframed the recommendation from "maintain audio quality messaging" to "address the durability perception gap before it becomes a retention problem."

---

## Artifacts

```
scripts/consumer_insights_eda.py
scripts/consumer_insights_sentiment.py
scripts/consumer_insights_correlation.py
scripts/consumer_insights_visualizations.py
data/processed/          → cleaned CSVs from each stage
visualizations/eda/      → 13 EDA charts
visualizations/sentiment/→ 10 sentiment charts
visualizations/correlation/ → 7 correlation charts
reports/                 → competitive analysis report, EDA writeup
```

**How to run:**
```bash
pip install pandas numpy textblob matplotlib seaborn wordcloud
python -m textblob.download_corpora
python scripts/consumer_insights_eda.py
python scripts/consumer_insights_sentiment.py
python scripts/consumer_insights_correlation.py
```
