# 📊 Introduction to Statistics with R

![R](https://img.shields.io/badge/R-4.x-276DC3?logo=r&logoColor=white)
![Statistics](https://img.shields.io/badge/Focus-Descriptive%20%26%20Inferential%20Statistics-blue)
![Course](https://img.shields.io/badge/Course-STAT%201601-lightgrey)

Coursework scripts from Introduction to Statistics with R, covering data wrangling, descriptive statistics, data merging, and practical R programming. Scripts apply real-world datasets including Netflix subscriber and revenue data and movie rating data.

---

## 📁 Project Structure

```
intro-stat-with-r/
├── scripts/
│   ├── hw3.R                   # Multi-file data merging & Netflix revenue/membership analysis
│   ├── hw5.R                   # Movie ratings analysis with loops & summary statistics
│   └── calculate_final_grade.R # Weighted grade calculator with R fundamentals
└── docs/
    └── r_cheat_sheet.md        # Personal R reference guide
```

---

## 📝 Scripts Overview

### `hw3.R` — Data Merging & Netflix Analysis
Reads 8 separate CSV files covering Netflix international and US revenue/membership data (2010–2017), resolves column name inconsistencies across files, and uses `rbind()` to build unified data frames for analysis.

**Skills demonstrated:** `rbind()`, `names()` reassignment, multi-file data integration, revenue and membership trend analysis

### `hw5.R` — Movie Ratings Analysis
Loads a movie ratings dataset and uses `substr()` to extract year/month/day components from date strings. Builds a 100-row × 14-column summary data frame with rating counts, proportions, and date ranges per movie — populated via a nested loop.

**Skills demonstrated:** `substr()`, `data.frame()`, `for` loops, `colnames()`, conditional aggregation, rating proportion calculations

### `calculate_final_grade.R` — Weighted Grade Calculator
Calculates a final weighted course grade from raw scores across three categories (Collaborative 40%, Homework 40%, Final Project 20%). Includes `stopifnot()` safety check for mismatched score/points vectors and prints a clean formatted summary.

**Skills demonstrated:** Weighted averages, `stopifnot()`, vector arithmetic, `paste0()`, conditional grade letter assignment

### `docs/r_cheat_sheet.md` — R Reference Guide
Personal reference covering: help functions, assignment and basics, vectors, data frames, reading/writing data, and common statistical functions — built while working through coursework.

---

## 🛠️ Topics Covered

- Reading and combining multi-file datasets (`read.csv`, `rbind`, `merge`)
- Column renaming and type coercion
- Descriptive statistics (`mean`, `median`, `sd`, `var`, `summary`)
- Iteration with `for` loops and index-based access
- Data frame construction and column-level population
- Weighted average calculations and grade normalization
- String parsing with `substr()`

---

## 💡 Key Takeaways

- Column consistency is the #1 friction point when merging real-world multi-file datasets — even datasets from the same source use inconsistent casing and typos (`Membershiip`)
- `stopifnot()` is an underutilized tool for catching data shape mismatches before silent bugs appear downstream
- R's vector arithmetic makes weighted grade calculations clean and readable vs. equivalent Python loops

---

## 📬 Contact

**Corey Farrow** · coreyfarrow25@gmail.com · [LinkedIn](https://linkedin.com/in/coreyfarrowjr)
