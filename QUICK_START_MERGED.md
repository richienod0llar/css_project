# Quick Start Guide - Merged 30K Dataset

## ✅ What Was Created

You now have a **merged dataset with 30,000 Vogue Runway images** from three folders, sorted chronologically by year (1988-2023).

---

## 📁 Key Files Created

### Dataset Files
- **`vogue_runway_merged_30k.csv`** (18 MB) - Main dataset with all 30K images
- **`merged_dataset_summary.txt`** - Detailed statistics

### Python Scripts
- **`create_merged_dataset.py`** - Creates the merged dataset
- **`load_merged_dataset.py`** - Helper functions to query the data
- **`visualize_merged_dataset.py`** - Generate visualizations

### Visualizations (7 PNG files)
- `merged_images_per_year.png` - Timeline distribution
- `merged_top_designers.png` - Top 20 designers
- `merged_category_distribution.png` - Category breakdown
- `merged_season_distribution.png` - Season breakdown
- `merged_aesthetic_distribution.png` - Quality scores
- `merged_source_folders.png` - Source distribution
- `merged_designer_timeline.png` - Designer timeline heatmap

### Documentation
- **`README_MERGED_30K.md`** - Complete documentation
- **`QUICK_START_MERGED.md`** - This guide

---

## 🚀 Quick Start in 30 Seconds

```python
import pandas as pd

# Load the merged dataset
df = pd.read_csv('vogue_dataset_output/vogue_runway_merged_30k.csv')

# Basic info
print(f"Total images: {len(df):,}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
print(f"Designers: {df['designer'].nunique()}")

# Top 5 designers
print("\nTop 5 Designers:")
print(df['designer'].value_counts().head())
```

---

## 📊 Dataset Quick Facts

| Metric | Value |
|--------|-------|
| **Total Images** | 30,000 |
| **Year Range** | 1988 - 2023 |
| **Peak Year** | 2016 (3,347 images) |
| **Top Designer** | Chanel (530 images) |
| **Categories** | Ready-to-Wear (65%), Menswear (15.6%), Couture (4.8%), Bridal (0.2%) |
| **Seasons** | Spring (44.3%), Fall (43.5%), Resort (6.8%), Pre-Fall (5.5%) |
| **File Size** | 18 MB (CSV) |
| **Sorting** | ✅ Sorted by year (ascending) |

---

## 🎯 Common Tasks

### 1. Load with Helper Functions

```python
from load_merged_dataset import load_merged_dataset, get_stats_summary

df = load_merged_dataset()
get_stats_summary(df)
```

### 2. Filter by Year

```python
from load_merged_dataset import filter_by_year

# Get recent collections (2020-2023)
recent = filter_by_year(df, start_year=2020, end_year=2023)
print(f"Found {len(recent):,} images")  # 5,756 images
```

### 3. Filter by Designer

```python
from load_merged_dataset import filter_by_designer

chanel = filter_by_designer(df, "Chanel")
print(f"Chanel: {len(chanel)} images from {chanel['year'].min()} to {chanel['year'].max()}")
```

### 4. Complex Filtering

```python
# Spring 2022 Ready-to-Wear with high aesthetic scores
spring_2022_rtw = df[
    (df['year'] == 2022) & 
    (df['season'] == 'Spring') & 
    (df['category'] == 'Ready-to-Wear') &
    (df['aesthetic'] > 5.0)
]

print(f"Found {len(spring_2022_rtw)} high-quality Spring 2022 RTW images")

# Top designers in this subset
print(spring_2022_rtw['designer'].value_counts().head())
```

### 5. Access Image Paths

```python
# Iterate through results
for idx, row in spring_2022_rtw.head(10).iterrows():
    print(f"{row['designer']} - {row['season']} {row['year']}")
    print(f"  Image: {row['image_path']}")
    print(f"  Aesthetic: {row['aesthetic']:.2f}")
    print()
```

### 6. Statistical Analysis

```python
# Images per decade
for decade in range(1980, 2030, 10):
    decade_df = df[(df['year'] >= decade) & (df['year'] < decade + 10)]
    print(f"{decade}s: {len(decade_df):,} images")

# Designer evolution over time
designer_timeline = df.groupby(['designer', 'year']).size().unstack(fill_value=0)
print(designer_timeline.loc['Christian Dior'])
```

---

## 🔍 Example Queries

### Find All Versace from 2015-2020

```python
versace = df[
    (df['designer'] == 'Versace') & 
    (df['year'] >= 2015) & 
    (df['year'] <= 2020)
]
print(f"Found {len(versace)} Versace images")
```

### Get High-Quality Couture Collections

```python
couture_high_quality = df[
    (df['category'] == 'Couture') & 
    (df['aesthetic'] > 5.5)
]
print(f"Found {len(couture_high_quality)} high-quality couture images")
```

### Track Designer Over Time

```python
dior = df[df['designer'] == 'Christian Dior']
dior_by_year = dior.groupby('year').size()

print(f"Christian Dior: {len(dior)} total images")
print(f"Peak year: {dior_by_year.idxmax()} with {dior_by_year.max()} images")
```

### Compare Seasons for a Designer

```python
chanel = df[df['designer'] == 'Chanel']
season_counts = chanel['season'].value_counts()
print("Chanel by season:")
print(season_counts)
```

---

## 📈 Generate Visualizations

Run this to create all visualizations:

```bash
python3 visualize_merged_dataset.py
```

This creates 7 PNG files in `vogue_dataset_output/`:
- Distribution charts
- Timeline visualizations  
- Heatmaps
- Statistical plots

---

## 🔄 Regenerate Dataset

If you need to recreate the merged dataset:

```bash
# Merge all three folders again
python3 create_merged_dataset.py

# Generate new visualizations
python3 visualize_merged_dataset.py

# Test with examples
python3 load_merged_dataset.py
```

---

## 📚 CSV Schema (17 columns)

| Column | Type | Description |
|--------|------|-------------|
| key | string | Unique ID |
| designer | string | Designer/brand |
| season | string | Spring/Fall/Resort/Pre-Fall |
| year | int | Collection year |
| category | string | Ready-to-Wear/Menswear/Couture/Bridal |
| city | string | Fashion week city |
| section | string | Collection/Details/Beauty |
| width | int | Image width (px) |
| height | int | Image height (px) |
| size | int | File size (bytes) |
| aesthetic | float | Quality score (2.27-7.54) |
| tags | list | Image tags |
| url | string | Vogue URL |
| filename | string | Image filename |
| json_path | string | Metadata path |
| image_path | string | Image file path |
| has_image | bool | File exists |
| source_folder | string | Origin folder (030/065/124) |

---

## 💡 Tips

### Performance
- Use pandas query() for complex filters
- Filter early to reduce data size
- Use .loc for explicit row/column selection

### Data Quality
- All 30,000 images have `has_image=True`
- No missing image files
- Aesthetic scores range 2.27-7.54 (mean: 4.93)

### Year Distribution
- **1988-1999:** Sparse (< 500 total)
- **2000-2009:** Growing (305-992/year)
- **2010-2015:** Expanding (1,265-2,040/year)
- **2016:** 🔥 Peak (3,347 images)
- **2017-2023:** Sustained (843-2,140/year)

---

## 🎨 Use Cases

### Fashion Analysis
```python
# Track designer evolution
designer_timeline = df[df['designer'] == 'Chanel'].groupby('year').size()
designer_timeline.plot(title='Chanel Collections Over Time')
```

### Machine Learning
```python
# Get training data with high aesthetic scores
training_data = df[df['aesthetic'] > 5.0]
image_paths = training_data['image_path'].tolist()
labels = training_data['designer'].tolist()
```

### Trend Analysis
```python
# Analyze seasonal preferences by decade
for decade in [2000, 2010, 2020]:
    decade_df = df[(df['year'] >= decade) & (df['year'] < decade + 10)]
    print(f"\n{decade}s:")
    print(decade_df['season'].value_counts(normalize=True) * 100)
```

---

## ❓ Need Help?

1. **Full Documentation:** See `README_MERGED_30K.md`
2. **Statistics:** Check `merged_dataset_summary.txt`
3. **Examples:** Run `python3 load_merged_dataset.py`
4. **Visualizations:** View PNG files in `vogue_dataset_output/`

---

## ✨ Summary

You now have:
- ✅ **30,000 images** from 3 folders merged
- ✅ **Sorted by year** (1988-2023)
- ✅ **Complete metadata** (17 columns)
- ✅ **Helper scripts** for easy access
- ✅ **7 visualizations** showing distributions
- ✅ **Full documentation** with examples

**Main File:** `vogue_dataset_output/vogue_runway_merged_30k.csv` (18 MB)

---

**Ready to explore fashion history from 1988 to 2023!** 🚀👗✨


