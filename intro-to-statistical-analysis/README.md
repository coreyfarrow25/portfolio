# 📐 Introduction to Statistical Analysis (STAT 2120)

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Statsmodels](https://img.shields.io/badge/Statsmodels-Regression-4c9fcf)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-4c9fcf)
![Course](https://img.shields.io/badge/Course-STAT%202120-lightgrey)

Python and Jupyter notebook coursework from Introduction to Statistical Analysis (STAT 2120), covering probability, regression, correlation, and inferential statistics. Includes a capstone GSS (General Social Survey) analysis project.

---

## 📁 Project Structure

```
intro-to-statistical-analysis/
├── notebooks/
│   ├── HW2 - HW3.ipynb              # Regression, correlation, probability
│   ├── Lab 2.1 - 2.2.ipynb          # Lab exercises — descriptive stats & distributions
│   ├── Stat 2120 - HW5-6.ipynb      # Inferential statistics
│   ├── Stat 2120 - Lab 4.3.ipynb    # Hypothesis testing lab
│   └── Stat 2120 HW9 and 10.ipynb   # Advanced topics
├── gss_analysis.xlsx                # GSS dataset analysis (Excel)
├── gss_paper.docx                   # Written capstone report on GSS findings
└── docs/
    └── STAT2120_Reference.docx      # Course reference guide
```

---

## 📝 Notebooks Overview

### `HW2 - HW3.ipynb` — Regression & Probability
**HW2:** Correlation and simple linear regression on a fast food / obesity dataset using `seaborn.regplot()` and `statsmodels.OLS`. Computed Pearson r, regression equation (ŷ = b₀ + b₁x), and R².

**HW3:** Probability calculations for discrete sample spaces — free throw scenarios (P(HH), P(at least one miss), P(first miss on 3rd attempt)) using Python as a calculator for exact probability arithmetic.

**Skills:** `sm.OLS`, `regplot`, correlation matrices, complement rule, sample space enumeration

### `Lab 2.1 - 2.2.ipynb` — Descriptive Statistics & Distributions
Lab exercises applying descriptive statistics and distribution analysis to real datasets. Covers measures of center, spread, and shape using `pandas` and `seaborn`.

### `Stat 2120 - HW5-6.ipynb` — Inferential Statistics
Homework covering confidence intervals and hypothesis testing. Applies z-tests and t-tests to sample data, interprets p-values, and draws conclusions about population parameters.

### `Stat 2120 - Lab 4.3.ipynb` — Hypothesis Testing
Structured lab applying one-sample and two-sample hypothesis tests. Includes test statistic calculation, critical value comparison, and interpretation of results at α = 0.05.

### `Stat 2120 HW9 and 10.ipynb` — Advanced Topics
Final homework assignments covering more advanced statistical methods including multiple regression and categorical analysis.

---

## 📊 GSS Capstone Project

The General Social Survey (GSS) analysis project applies course concepts to real sociological survey data. The analysis (`gss_analysis.xlsx`) examines relationships between demographic variables and survey responses, while `gss_paper.docx` presents findings in a written report format including hypotheses, methodology, results, and interpretation.

---

## 🛠️ Topics Covered

- Simple and multiple linear regression (`statsmodels.OLS`)
- Pearson correlation coefficient and R²
- Probability and sample spaces (discrete)
- Confidence intervals and margin of error
- Hypothesis testing (z-test, t-test, p-values)
- Descriptive statistics: mean, median, standard deviation, IQR
- Data visualization with Seaborn and Matplotlib
- GSS survey data analysis

---

## 💡 Key Takeaways

- R² alone doesn't tell you if a regression is useful — checking residuals and considering confounders is essential
- Probability problems become more tractable when you enumerate the sample space explicitly before computing
- The fast food / obesity regression found a statistically significant positive correlation, but association ≠ causation — geographic confounders (income, food access) are more likely drivers

---

## 📬 Contact

**Corey Farrow** · coreyfarrow25@gmail.com · [LinkedIn](https://linkedin.com/in/coreyfarrowjr)
