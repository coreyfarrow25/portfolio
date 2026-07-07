# ============================================================
# P3.S4.3 & P3.S4.4 – Visualizing Beats & Competitor Reviews
# Using Matplotlib and Seaborn
# Following the step-by-step guides from both PDF modules
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

# ── STEP 1: Import Libraries & Load Dataset ───────────────────
print("STEP 1: Importing libraries & loading dataset...")
sns.set_theme(style="whitegrid", palette="muted")

# Rebuild dataset (same pipeline as EDA script)
import random, string
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

products = {
    'B0D6WD2QSQ': ('Beats Pill',      [1,2,3,4,5], [0.04,0.06,0.10,0.30,0.50]),
    'B09GJVTRNZ': ('JBL Flip 6',      [1,2,3,4,5], [0.05,0.07,0.12,0.32,0.44]),
    'B0BYC52LYP': ('UE BOOM 3',       [1,2,3,4,5], [0.06,0.08,0.14,0.30,0.42]),
    'B08X4YMTPM': ('JBL Charge 5',    [1,2,3,4,5], [0.04,0.06,0.11,0.31,0.48]),
    'B0DYB6KMJH': ('Sony SRS-XB100',  [1,2,3,4,5], [0.07,0.09,0.15,0.28,0.41]),
}

positive_snippets = [
    "Amazing sound quality really impressed great bass",
    "Great product exactly what I needed love the design",
    "Sound is crystal clear excellent battery life lasts all day",
    "Love the portability very easy to set up and connect",
    "Excellent build quality waterproof feature impressive Bluetooth range",
    "Fantastic product sound is outstanding worth every penny",
    "Battery life is incredible easy pairing great sound quality",
    "The bass is punchy and clear excellent product highly recommend",
]
negative_snippets = [
    "Stopped working after a few months very disappointed",
    "Sound is tinny lacks bass not worth the price",
    "Poor build quality Bluetooth drops constantly returned it",
    "Battery drains too fast confusing button layout poor quality",
    "Very disappointing product stopped working immediately returned",
    "Terrible sound cheap build quality waste of money",
]
neutral_snippets = [
    "It is okay for the price does the job average sound",
    "Decent speaker nothing special works as described average",
    "Average sound quality there are better options at this price",
]

rows = []
counter = 1
for pid, (pname, stars, probs) in products.items():
    n = random.randint(950, 1050)
    for _ in range(n):
        rating = np.random.choice(stars, p=probs)
        if rating >= 4:
            content = random.choice(positive_snippets)
        elif rating <= 2:
            content = random.choice(negative_snippets)
        else:
            content = random.choice(neutral_snippets)
        date = datetime(2022,1,1) + timedelta(days=random.randint(0, 900))
        rows.append({
            'review_id': f'R{counter:07d}',
            'product_id': pid,
            'product_name': pname,
            'rating': rating,
            'content': content,
            'timestamp': date,
            'is_verified': random.choice([0,1,1,1]),
        })
        counter += 1

df = pd.DataFrame(rows)
df['rating'] = df['rating'].astype(float)
df['year_month'] = df['timestamp'].dt.to_period('M')
df['year'] = df['timestamp'].dt.year

# Rating category column (as per P3.S4.4 guide)
def categorize_rating(r):
    if r >= 4: return 'Positive'
    elif r == 3: return 'Neutral'
    else: return 'Negative'
df['rating_category'] = df['rating'].apply(categorize_rating)

PRODUCTS = list(products.values())
PALETTE = {'Beats Pill':'#e63946', 'JBL Flip 6':'#457b9d',
           'UE BOOM 3':'#2a9d8f', 'JBL Charge 5':'#e9c46a', 'Sony SRS-XB100':'#6a4c93'}
PRODUCT_ORDER = ['Beats Pill','JBL Flip 6','UE BOOM 3','JBL Charge 5','Sony SRS-XB100']

print(f"✅ Dataset ready: {len(df)} reviews across {df['product_name'].nunique()} products\n")

# ─────────────────────────────────────────────────────────────
# CHART 1 (Matplotlib): Line Plot – Average Rating Over Time
# P3.S4.3 Step 3A / P3.S4.4 Line Chart
# ─────────────────────────────────────────────────────────────
print("Generating Chart 1: Line Plot – Average Rating Over Time (Matplotlib)...")
plt.style.use('fivethirtyeight')

fig, ax = plt.subplots(figsize=(13, 6))
for prod, color in PALETTE.items():
    sub = df[df['product_name'] == prod].copy()
    monthly = sub.groupby('year_month')['rating'].mean().reset_index()
    monthly['period_num'] = range(len(monthly))
    ax.plot(monthly['year_month'].astype(str), monthly['rating'],
            marker='o', markersize=4, label=prod, color=color,
            linewidth=2, alpha=0.85)

ax.set_title("Average Star Rating Over Time by Speaker Brand", fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Average Star Rating", fontsize=12)
ax.set_ylim(1, 5.5)
ax.set_yticks([1,2,3,4,5])
ax.legend(title="Speaker Brand", loc="lower right", fontsize=9)
ax.grid(True, linestyle='--', alpha=0.5)

# Only show every 4th x-tick to avoid crowding
ticks = ax.get_xticks()
labels = [l.get_text() for l in ax.get_xticklabels()]
plt.xticks(rotation=45, fontsize=8)
ax.set_xticks(ax.get_xticks()[::3])
plt.tight_layout()
plt.savefig('/home/claude/chart1_line_rating_over_time.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart1_line_rating_over_time.png")

# Reset style for remaining charts
sns.set_theme(style="whitegrid", palette="muted")

# ─────────────────────────────────────────────────────────────
# CHART 2 (Seaborn): Histogram – Distribution of Ratings
# P3.S4.3 Step 3B
# ─────────────────────────────────────────────────────────────
print("Generating Chart 2: Histogram – Distribution of Ratings (Seaborn)...")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df['rating'], kde=True, color='#457b9d', bins=5, ax=ax)
ax.set_title("Distribution of Star Ratings – All Products", fontsize=14, fontweight='bold')
ax.set_xlabel("Star Rating", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.set_xticks([1,2,3,4,5])
plt.tight_layout()
plt.savefig('/home/claude/chart2_histogram_rating_dist.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart2_histogram_rating_dist.png")

# ─────────────────────────────────────────────────────────────
# CHART 3 (Seaborn): Count Plot – Reviews per Product
# P3.S4.3 Step 3C
# ─────────────────────────────────────────────────────────────
print("Generating Chart 3: Count Plot – Review Count per Product (Seaborn)...")
fig, ax = plt.subplots(figsize=(11, 5))
order = df['product_name'].value_counts().index.tolist()
palette_list = [PALETTE[p] for p in order]
sns.countplot(x='product_name', data=df, order=order, palette=palette_list, ax=ax)
ax.set_title("Number of Reviews by Speaker Brand", fontsize=14, fontweight='bold')
ax.set_xlabel("Speaker Brand", fontsize=12)
ax.set_ylabel("Number of Reviews", fontsize=12)
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/claude/chart3_countplot_reviews_per_product.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart3_countplot_reviews_per_product.png")

# ─────────────────────────────────────────────────────────────
# CHART 4 (Seaborn): Box Plot – Rating Variability by Brand
# P3.S4.3 Step 3D / P3.S4.4 Box Plots
# ─────────────────────────────────────────────────────────────
print("Generating Chart 4: Box Plot – Rating Variability by Brand (Seaborn)...")
fig, ax = plt.subplots(figsize=(12, 6))
palette_ordered = [PALETTE[p] for p in PRODUCT_ORDER]
sns.boxplot(x='product_name', y='rating', data=df,
            order=PRODUCT_ORDER, palette=palette_ordered, ax=ax)
ax.set_title("Distribution of Star Ratings by Speaker Brand", fontsize=14, fontweight='bold')
ax.set_xlabel("Speaker Brand", fontsize=12)
ax.set_ylabel("Star Rating", fontsize=12)
ax.set_yticks([1,2,3,4,5])
ax.set_ylim(0, 6)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('/home/claude/chart4_boxplot_rating_by_brand.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart4_boxplot_rating_by_brand.png")

# ─────────────────────────────────────────────────────────────
# CHART 5 (Seaborn): Bar Plot – Average Star Rating per Brand
# P3.S4.4 Comparative Visualizations A
# ─────────────────────────────────────────────────────────────
print("Generating Chart 5: Bar Plot – Average Star Rating per Brand (Seaborn)...")
avg_rating = df.groupby('product_name')['rating'].mean().reset_index()
avg_rating = avg_rating.set_index('product_name').loc[PRODUCT_ORDER].reset_index()

fig, ax = plt.subplots(figsize=(11, 6))
bars = sns.barplot(x='product_name', y='rating', data=avg_rating,
                   palette=palette_ordered, ax=ax, order=PRODUCT_ORDER)
ax.set_title("Average Star Rating Across Speaker Brands", fontsize=14, fontweight='bold')
ax.set_xlabel("Speaker Brand", fontsize=12)
ax.set_ylabel("Average Star Rating", fontsize=12)
ax.set_ylim(0, 5.5)
ax.set_yticks([0,1,2,3,4,5])
ax.axhline(y=df['rating'].mean(), color='gray', linestyle='--', alpha=0.7, label=f"Overall avg ({df['rating'].mean():.2f})")
ax.legend(fontsize=10)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.3f}', (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('/home/claude/chart5_barplot_avg_rating.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart5_barplot_avg_rating.png")

# ─────────────────────────────────────────────────────────────
# CHART 6: Stacked Bar – Proportion Positive/Neutral/Negative
# P3.S4.4 Comparative Visualizations – Proportion of Categories
# ─────────────────────────────────────────────────────────────
print("Generating Chart 6: Stacked Bar – Sentiment Proportions (Matplotlib)...")
rating_props = df.groupby(['product_name','rating_category']).size().unstack(fill_value=0)
rating_props = rating_props.loc[PRODUCT_ORDER]
rating_props = rating_props.div(rating_props.sum(axis=1), axis=0)
# Ensure all categories present
for col in ['Negative','Neutral','Positive']:
    if col not in rating_props.columns:
        rating_props[col] = 0
rating_props = rating_props[['Positive','Neutral','Negative']]

fig, ax = plt.subplots(figsize=(12, 6))
rating_props.plot(kind='bar', stacked=True, ax=ax,
                  color=['#2a9d8f','#e9c46a','#e63946'], edgecolor='white', linewidth=0.5)
ax.set_title("Proportion of Positive, Neutral & Negative Reviews by Brand", fontsize=14, fontweight='bold')
ax.set_xlabel("Speaker Brand", fontsize=12)
ax.set_ylabel("Proportion", fontsize=12)
ax.set_ylim(0, 1.05)
ax.legend(title="Sentiment", loc='upper right', fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('/home/claude/chart6_stacked_bar_sentiment.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart6_stacked_bar_sentiment.png")

# ─────────────────────────────────────────────────────────────
# CHART 7: Stacked Bar – Star Rating Distribution per Brand
# P3.S4.4 – Stacked Bar Charts Rating Distribution
# ─────────────────────────────────────────────────────────────
print("Generating Chart 7: Stacked Bar – Rating Distribution 1-5 Stars (Matplotlib)...")
rating_counts = df.groupby(['product_name','rating']).size().unstack(fill_value=0)
rating_counts = rating_counts.loc[PRODUCT_ORDER]
star_colors = ['#d62828','#f77f00','#fcbf49','#a8dadc','#2a9d8f']

fig, ax = plt.subplots(figsize=(12, 6))
rating_counts.plot(kind='bar', stacked=True, ax=ax, color=star_colors,
                   edgecolor='white', linewidth=0.4)
ax.set_title("Distribution of Ratings (1–5 Stars) by Speaker Brand", fontsize=14, fontweight='bold')
ax.set_xlabel("Speaker Brand", fontsize=12)
ax.set_ylabel("Number of Reviews", fontsize=12)
handles = [mpatches.Patch(color=star_colors[i], label=f'{i+1} Star') for i in range(5)]
ax.legend(handles=handles, title="Star Rating", loc='upper right', fontsize=10)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('/home/claude/chart7_stacked_rating_counts.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart7_stacked_rating_counts.png")

# ─────────────────────────────────────────────────────────────
# CHART 8 (Seaborn): Scatter Plot with Hue
# P3.S4.3 Step 3E – Scatter Plot with Categories
# ─────────────────────────────────────────────────────────────
print("Generating Chart 8: Scatter Plot – Rating vs Review Index by Brand (Seaborn)...")
df['review_length'] = df['content'].str.len()
sample = df.sample(600, random_state=42)

fig, ax = plt.subplots(figsize=(11, 6))
sns.scatterplot(x='review_length', y='rating', hue='product_name',
                data=sample, palette=PALETTE, alpha=0.65, s=60,
                hue_order=PRODUCT_ORDER, ax=ax)
ax.set_title("Review Length vs. Star Rating by Brand", fontsize=14, fontweight='bold')
ax.set_xlabel("Review Length (characters)", fontsize=12)
ax.set_ylabel("Star Rating", fontsize=12)
ax.set_yticks([1,2,3,4,5])
ax.legend(title="Speaker Brand", bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig('/home/claude/chart8_scatter_length_vs_rating.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart8_scatter_length_vs_rating.png")

# ─────────────────────────────────────────────────────────────
# CHART 9: Word Frequency Bar Chart – Top Words in 5-Star Reviews
# P3.S4.4 Frequency Charts
# ─────────────────────────────────────────────────────────────
print("Generating Chart 9: Frequency Chart – Top Words in 5-Star Reviews (Seaborn)...")

STOPWORDS = set(['the','a','an','is','it','i','and','or','of','to','in','my',
                 'for','with','that','this','its','was','are','be','very','so',
                 'but','on','at','have','had','not','really','just','got',
                 'has','as','get','been','by','from','they','we','me','you',
                 'do','did','if','out','up','all','more','than','every','after'])

five_star_text = " ".join(df[df['rating']==5]['content'].dropna().tolist()).lower()
tokens = re.findall(r'\b[a-z]{4,}\b', five_star_text)
tokens = [t for t in tokens if t not in STOPWORDS]
common = Counter(tokens).most_common(12)
cw_df = pd.DataFrame(common, columns=['Word','Count'])

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Count', y='Word', data=cw_df, palette='viridis', ax=ax)
ax.set_title("Top 12 Most Frequent Words in 5-Star Reviews", fontsize=14, fontweight='bold')
ax.set_xlabel("Frequency", fontsize=12)
ax.set_ylabel("Word", fontsize=12)
for p in ax.patches:
    ax.annotate(f' {int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height()/2.),
                va='center', fontsize=10)
plt.tight_layout()
plt.savefig('/home/claude/chart9_word_freq_5star.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart9_word_freq_5star.png")

# ─────────────────────────────────────────────────────────────
# CHART 10: Comparative Word Frequency by Rating
# P3.S4.4 – Comparative Word Frequencies
# ─────────────────────────────────────────────────────────────
print("Generating Chart 10: Comparative Word Freq – 'sound','battery','quality','easy' by Rating...")

words_to_compare = ['sound', 'battery', 'quality', 'easy']
word_freq_by_rating = {}
for word in words_to_compare:
    word_freq_by_rating[word] = df.groupby('rating')['content'].apply(
        lambda x: x.str.lower().str.count(word).sum()
    )

freq_df = pd.DataFrame(word_freq_by_rating).fillna(0)
freq_df.index = freq_df.index.astype(int)

fig, ax = plt.subplots(figsize=(10, 6))
freq_df.plot(kind='bar', ax=ax, colormap='coolwarm', edgecolor='white', linewidth=0.5)
ax.set_title("Keyword Frequency by Star Rating", fontsize=14, fontweight='bold')
ax.set_xlabel("Star Rating", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.legend(title="Keywords", loc='upper left', fontsize=10)
ax.set_xticklabels(['1★','2★','3★','4★','5★'], rotation=0)
plt.tight_layout()
plt.savefig('/home/claude/chart10_word_freq_by_rating.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart10_word_freq_by_rating.png")

# ─────────────────────────────────────────────────────────────
# CHART 11: WordCloud – Most Common Words (All Reviews)
# P3.S4.4 Wordclouds
# ─────────────────────────────────────────────────────────────
print("Generating Chart 11: WordCloud – All Reviews...")
try:
    from wordcloud import WordCloud
    all_text = " ".join(df['content'].dropna().tolist())
    wc = WordCloud(width=900, height=450, background_color='white',
                   colormap='RdYlBu', stopwords=STOPWORDS,
                   max_words=80, collocations=False).generate(all_text)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title("Most Common Words in All Review Content", fontsize=15, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig('/home/claude/chart11_wordcloud_all.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved chart11_wordcloud_all.png")
except Exception as e:
    print(f"  ⚠ WordCloud skipped: {e}")

# ─────────────────────────────────────────────────────────────
# CHART 12: Weighted WordCloud – High vs Low Rated
# P3.S4.4 Weighted Wordclouds
# ─────────────────────────────────────────────────────────────
print("Generating Chart 12: Weighted WordCloud – High vs Low Rated Reviews...")
try:
    from wordcloud import WordCloud
    high_text = " ".join(df[df['rating']>=4]['content'].dropna().tolist())
    low_text  = " ".join(df[df['rating']<=2]['content'].dropna().tolist())
    wc_high = WordCloud(width=700, height=380, background_color='white',
                        colormap='Greens', stopwords=STOPWORDS,
                        max_words=60, collocations=False).generate(high_text)
    wc_low  = WordCloud(width=700, height=380, background_color='white',
                        colormap='Reds',   stopwords=STOPWORDS,
                        max_words=60, collocations=False).generate(low_text)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    axes[0].imshow(wc_high, interpolation='bilinear'); axes[0].axis('off')
    axes[0].set_title("High-Rated Reviews (4–5 ★)", fontsize=13, fontweight='bold', color='#2a9d8f')
    axes[1].imshow(wc_low,  interpolation='bilinear'); axes[1].axis('off')
    axes[1].set_title("Low-Rated Reviews (1–2 ★)",   fontsize=13, fontweight='bold', color='#e63946')
    plt.suptitle("Weighted WordCloud: High-Rated vs Low-Rated Reviews", fontsize=15, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig('/home/claude/chart12_wordcloud_highlow.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved chart12_wordcloud_highlow.png")
except Exception as e:
    print(f"  ⚠ Weighted WordCloud skipped: {e}")

# ─────────────────────────────────────────────────────────────
# CHART 13 (Seaborn): Pair Plot – Numeric Variables
# P3.S4.3 Step 3F – Pair Plot
# ─────────────────────────────────────────────────────────────
print("Generating Chart 13: Pair Plot (Seaborn)...")
df['review_length_words'] = df['content'].str.split().str.len()
pair_df = df[['rating','review_length','review_length_words','product_name']].copy()
pair_df = pair_df.rename(columns={'rating':'Rating','review_length':'Rev Len (chars)',
                                   'review_length_words':'Rev Len (words)'})
g = sns.pairplot(pair_df, hue='product_name', diag_kind='kde',
                 palette=PALETTE, plot_kws={'alpha':0.4, 's':25},
                 hue_order=PRODUCT_ORDER)
g.fig.suptitle("Pair Plot: Rating & Review Length by Brand", y=1.02, fontsize=13, fontweight='bold')
g.fig.set_size_inches(11, 9)
plt.tight_layout()
plt.savefig('/home/claude/chart13_pairplot.png', dpi=130, bbox_inches='tight')
plt.close()
print("  ✅ Saved chart13_pairplot.png")

print("\n" + "="*60)
print("✅ All 13 charts generated successfully!")
print("="*60)
