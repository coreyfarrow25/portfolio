# ============================================================
# P3.S4.1 - Exploratory Data Analysis with Pandas
# Beats by Dre & Competitors – Amazon Wireless Speaker Reviews
# Following the step-by-step guide from the PDF module
# ============================================================

import pandas as pd
import numpy as np

print("=" * 65)
print("  BEATS & COMPETITORS – EXPLORATORY DATA ANALYSIS WITH PANDAS")
print("=" * 65)

# ─────────────────────────────────────────────────────────────
# STEP 1: LOAD THE DATASET
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 1 — LOAD THE DATASET")
print("─" * 65)

df_raw = pd.read_csv('/home/claude/new_reference_data_for_beats.csv')

# --- Apply the cleaning pipeline from copy_of_consumer_insights_cleaning.py ---
df = df_raw.copy()

# Fill missing authors
df['author'] = df['author'].fillna('Anonymous')
# Drop missing content
df = df.dropna(subset=['content'])
# Fill missing product_attributes
df['product_attributes'] = df['product_attributes'].fillna('Not Specified')
# Remove duplicates
df = df.drop_duplicates()
df = df.drop_duplicates(subset=['review_id'])
# Clean title
df['title'] = df['title'].str.replace(
    r'^\d+(\.\d+)?\s+out of \d+\s+stars\s+', '', regex=True).str.strip()
# Parse timestamp
df['timestamp'] = df['timestamp'].str.replace(
    r'^Reviewed in the United States\s+', '', regex=True).str.strip()
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%B %d, %Y', errors='coerce')
# Fix types
df['rating'] = df['rating'].astype(int)
df['is_verified'] = df['is_verified'].astype(int)
for col in ['review_id', 'author', 'title', 'content', 'profile_id']:
    df[col] = df[col].str.strip()
df['review_length'] = df['content'].str.len()

# Map product names
product_mapping = {
    'B0D6WD2QSQ': 'Beats Pill',
    'B09GJVTRNZ': 'JBL Flip 6',
    'B0BYC52LYP': 'UE BOOM 3',
    'B08X4YMTPM': 'JBL Charge 5',
    'B0DYB6KMJH': 'Sony SRS-XB100',
}
df['product_name'] = df['product_id'].map(product_mapping).fillna('Other')

# Apply NumPy preparation (from scraping_preparation script)
ratings = df['rating'].values.astype(float)
mean_rating = np.nanmean(ratings)
ratings = np.where(np.isnan(ratings), mean_rating, ratings)
df['rating'] = ratings
valid_mask = (df['rating'] >= 0) & (df['rating'] <= 5)
df = df[valid_mask].reset_index(drop=True)
review_lengths_words = np.array([len(str(r).split()) for r in df['content']])
df['review_length_words'] = review_lengths_words
min_r, max_r = np.min(ratings), np.max(ratings)
df['normalized_rating'] = (df['rating'] - min_r) / (max_r - min_r)
df['rating'] = df['rating'].astype(np.float64)

print(f"\n✅ Dataset loaded and cleaned successfully.")
print(f"   File: new_reference_data_for_beats.csv")
print(f"   Total reviews: {len(df)}")

# ─────────────────────────────────────────────────────────────
# STEP 2: DISPLAY THE DATA
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 2 — DISPLAY THE DATA")
print("─" * 65)

print("\n📋 First 5 rows (df.head()):")
print(df[['review_id','product_name','author','rating','title','review_length_words']].head())

print("\n📋 Last 5 rows (df.tail()):")
print(df[['review_id','product_name','author','rating','title','review_length_words']].tail())

print(f"\n📐 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"   Columns: {df.columns.tolist()}")

# ─────────────────────────────────────────────────────────────
# STEP 3: DESCRIPTIVE STATISTICS
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 3 — DESCRIPTIVE STATISTICS")
print("─" * 65)

print("\n📊 Full describe() for numeric columns:")
print(df[['rating', 'review_length', 'review_length_words', 'normalized_rating', 'is_verified']].describe().round(3))

print("\n⭐ Rating Statistics (ratings column):")
print(f"   Mean:               {df['rating'].mean():.4f}")
print(f"   Median:             {df['rating'].median():.1f}")
print(f"   Mode:               {int(df['rating'].mode()[0])}")
print(f"   Variance:           {df['rating'].var():.4f}")
print(f"   Standard Deviation: {df['rating'].std():.4f}")

print("\n📝 Review Length (characters) Statistics:")
print(f"   Mean:               {df['review_length'].mean():.1f} chars")
print(f"   Median:             {df['review_length'].median():.0f} chars")
print(f"   Variance:           {df['review_length'].var():.1f}")
print(f"   Standard Deviation: {df['review_length'].std():.1f} chars")

print("\n📝 Review Length (words) Statistics:")
print(f"   Mean:               {df['review_length_words'].mean():.1f} words")
print(f"   Median:             {df['review_length_words'].median():.0f} words")
print(f"   Min:                {df['review_length_words'].min()} words")
print(f"   Max:                {df['review_length_words'].max()} words")
print(f"   Std Deviation:      {df['review_length_words'].std():.1f} words")

print("\n📦 Reviews per Product:")
print(df['product_name'].value_counts().to_string())

print("\n⭐ Rating Distribution (all products):")
print(df['rating'].value_counts().sort_index().to_string())

print("\n⭐ Average Rating per Product:")
avg_by_product = df.groupby('product_name')['rating'].mean().sort_values(ascending=False)
for prod, avg in avg_by_product.items():
    print(f"   {prod:<30} {avg:.3f}")

# ─────────────────────────────────────────────────────────────
# STEP 4: IDENTIFY MISSING VALUES
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 4 — IDENTIFY MISSING VALUES")
print("─" * 65)

missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
print("\n🔎 Missing values per column:")
print(missing_df[missing_df['Missing Count'] > 0].to_string() if missing_df['Missing Count'].sum() > 0 
      else "   ✅ No missing values — dataset is complete after cleaning!")

# ─────────────────────────────────────────────────────────────
# STEP 5: HANDLE MISSING VALUES (already done; document strategy)
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 5 — HANDLING MISSING VALUES (Strategy Applied)")
print("─" * 65)
print("""
   Strategy used during cleaning:
   • 'author'             → fillna('Anonymous')      [df['author'].fillna(...)]
   • 'content'            → dropna(subset=['content'])  [reviews without text removed]
   • 'product_attributes' → fillna('Not Specified')   [supplementary info]
   • 'rating'             → np.nanmean imputation     [NumPy mean fill]

   Result: 0 missing values remain in the analysis-ready dataset.
""")

# ─────────────────────────────────────────────────────────────
# STEP 6: CHECKING FOR OUTLIERS (IQR Method)
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 6 — CHECKING FOR OUTLIERS (IQR Method)")
print("─" * 65)

# ── Outliers in RATING ──
Q1_r = df['rating'].quantile(0.25)
Q3_r = df['rating'].quantile(0.75)
IQR_r = Q3_r - Q1_r
rating_outliers = df[(df['rating'] < (Q1_r - 1.5 * IQR_r)) | (df['rating'] > (Q3_r + 1.5 * IQR_r))]

print(f"\n  Rating column — IQR Analysis:")
print(f"   Q1 (25th percentile):  {Q1_r:.1f}")
print(f"   Q3 (75th percentile):  {Q3_r:.1f}")
print(f"   IQR:                   {IQR_r:.1f}")
print(f"   Lower fence:           {Q1_r - 1.5*IQR_r:.1f}")
print(f"   Upper fence:           {Q3_r + 1.5*IQR_r:.1f}")
print(f"   Outliers detected:     {len(rating_outliers)}")
if len(rating_outliers) > 0:
    print(f"   Note: These outliers have already been filtered (valid range 0–5 stars).")

# ── Outliers in REVIEW LENGTH ──
Q1_l = df['review_length_words'].quantile(0.25)
Q3_l = df['review_length_words'].quantile(0.75)
IQR_l = Q3_l - Q1_l
length_outliers = df[
    (df['review_length_words'] < (Q1_l - 1.5 * IQR_l)) |
    (df['review_length_words'] > (Q3_l + 1.5 * IQR_l))
]

print(f"\n  Review Length (words) — IQR Analysis:")
print(f"   Q1 (25th percentile):  {Q1_l:.1f} words")
print(f"   Q3 (75th percentile):  {Q3_l:.1f} words")
print(f"   IQR:                   {IQR_l:.1f} words")
print(f"   Lower fence:           {Q1_l - 1.5*IQR_l:.1f} words")
print(f"   Upper fence:           {Q3_l + 1.5*IQR_l:.1f} words")
print(f"   Outlier reviews found: {len(length_outliers)}")
if len(length_outliers) > 0:
    print(f"\n   📌 Note: Outlier reviews aren't necessarily 'bad' — long reviews may")
    print(f"   contain richer sentiment data. They are flagged, not removed.")
    print(f"\n   Sample outlier reviews (longest):")
    print(length_outliers.nlargest(3, 'review_length_words')[
        ['review_id','product_name','rating','review_length_words']
    ].to_string(index=False))

# ── Per-product outlier summary ──
print(f"\n  Outliers by Product:")
for prod in df['product_name'].unique():
    sub = df[df['product_name'] == prod]['review_length_words']
    q1, q3 = sub.quantile(0.25), sub.quantile(0.75)
    iqr = q3 - q1
    out = sub[(sub < q1 - 1.5*iqr) | (sub > q3 + 1.5*iqr)]
    pct = len(out)/len(sub)*100
    print(f"   {prod:<30} {len(out):>4} outliers ({pct:.1f}%)")

# ─────────────────────────────────────────────────────────────
# STEP 7: SAVE THE CLEANED + EDA-READY DATASET
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 7 — SAVE THE CLEANED EDA DATASET")
print("─" * 65)

output_path = '/mnt/user-data/outputs/beats_eda_complete.csv'
df.to_csv(output_path, index=False)
print(f"\n✅ EDA-ready dataset saved → beats_eda_complete.csv")
print(f"   Rows: {len(df)}  |  Columns: {len(df.columns)}")
print(f"   Columns: {df.columns.tolist()}")

# ─────────────────────────────────────────────────────────────
# BONUS: KEY INSIGHTS SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  KEY INSIGHTS FROM EDA")
print("=" * 65)

total = len(df)
beats_df = df[df['product_id'] == 'B0D6WD2QSQ']
beats_avg = beats_df['rating'].mean()
comp_avg = df[df['product_id'] != 'B0D6WD2QSQ']['rating'].mean()
five_star_pct = (df[df['rating'] == 5].shape[0] / total) * 100
verified_pct = (df['is_verified'].sum() / total) * 100

print(f"""
  1. Dataset Size:        {total} cleaned reviews across 5 products
  2. Beats Pill avg ⭐:   {beats_avg:.3f} vs competitor avg: {comp_avg:.3f}
  3. 5-star reviews:      {five_star_pct:.1f}% of all reviews
  4. Verified purchases:  {verified_pct:.1f}% of all reviews
  5. Avg review length:   {df['review_length_words'].mean():.1f} words per review
  6. Rating std dev:      {df['rating'].std():.3f} (spread across products)
  7. Highest rated:       {avg_by_product.index[0]} ({avg_by_product.iloc[0]:.3f} avg ⭐)
  8. Most reviews:        {df['product_name'].value_counts().index[0]} ({df['product_name'].value_counts().iloc[0]} reviews)
""")

print("=" * 65)
print("✅ EDA Complete! All 7 steps from P3.S4.1 guide executed.")
print("=" * 65)
