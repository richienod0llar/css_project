# Vogue Runway Merged Dataset (30K Images)

## Overview

This repository contains a merged dataset of **30,000 Vogue Runway images** with comprehensive metadata, sorted by year. The dataset combines three source folders into one unified collection.

### Dataset Statistics

- **Total Images:** 30,000
- **Year Range:** 1988 - 2023
- **All Images:** ✓ Complete with files
- **Format:** CSV with JSON metadata

### Source Folders

- `vogue_runway_030`: 10,000 images
- `vogue_runway_065`: 10,000 images
- `vogue_runway_124`: 10,000 images

---

## Key Statistics

### Categories

| Category | Count | Percentage |
|----------|-------|------------|
| Ready-to-Wear | 19,507 | 65.0% |
| Menswear | 4,692 | 15.6% |
| Couture | 1,435 | 4.8% |
| Bridal | 74 | 0.2% |

### Seasons

| Season | Count | Percentage |
|--------|-------|------------|
| Spring | 13,278 | 44.3% |
| Fall | 13,047 | 43.5% |
| Resort | 2,039 | 6.8% |
| Pre-Fall | 1,636 | 5.5% |

### Top 10 Designers

| Rank | Designer | Image Count |
|------|----------|-------------|
| 1 | Chanel | 530 |
| 2 | Valentino | 486 |
| 3 | Christian Dior | 451 |
| 4 | Dolce & Gabbana | 376 |
| 5 | Versace | 356 |
| 6 | Givenchy | 346 |
| 7 | Giorgio Armani | 325 |
| 8 | Gucci | 309 |
| 9 | Louis Vuitton | 298 |
| 10 | Prada | 293 |

### Aesthetic Scores

- **Mean:** 4.93
- **Median:** 4.93
- **Range:** 2.27 - 7.54
- **Standard Deviation:** 0.63

### Peak Years

| Year | Image Count |
|------|-------------|
| 2016 | 3,347 (Peak) |
| 2017 | 2,140 |
| 2019 | 2,109 |
| 2015 | 2,040 |
| 2020 | 1,974 |

---

## Files in This Repository

### Main Dataset Files

- **`vogue_runway_merged_30k.csv`** - Complete merged dataset (30K entries)
- **`merged_dataset_summary.txt`** - Detailed summary statistics

### Python Scripts

1. **`create_merged_dataset.py`** - Script that creates the merged dataset
   - Loads metadata from all three folders
   - Merges into single dataset
   - Sorts by year and season
   - Generates comprehensive summary

2. **`load_merged_dataset.py`** - Helper functions to work with the dataset
   - Load and filter data
   - Query by designer, year, category, season, aesthetic
   - Export filtered datasets
   - Statistical summaries

3. **`visualize_merged_dataset.py`** - Generate visualizations
   - Images per year distribution
   - Top designers chart
   - Category/season distributions
   - Aesthetic score analysis
   - Designer timeline heatmap
   - Source folder distribution

### Visualizations (PNG Files)

- `merged_images_per_year.png` - Timeline showing image distribution by year
- `merged_top_designers.png` - Top 20 designers by image count
- `merged_category_distribution.png` - Category breakdown (bar + pie)
- `merged_season_distribution.png` - Season breakdown
- `merged_aesthetic_distribution.png` - Aesthetic score distribution
- `merged_source_folders.png` - Distribution across source folders
- `merged_designer_timeline.png` - Heatmap of top designers over time

---

## How to Use

### 1. Load the Dataset

```python
import pandas as pd

# Load the merged dataset
df = pd.read_csv('vogue_dataset_output/vogue_runway_merged_30k.csv')

print(f"Loaded {len(df):,} images")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
```

### 2. Using the Helper Script

```python
from load_merged_dataset import (
    load_merged_dataset, 
    filter_by_year, 
    filter_by_designer,
    filter_by_aesthetic,
    get_stats_summary
)

# Load dataset
df = load_merged_dataset()

# Get comprehensive statistics
get_stats_summary(df)

# Filter by year range
recent = filter_by_year(df, start_year=2020, end_year=2023)
print(f"Found {len(recent):,} images from 2020-2023")

# Filter by designer
chanel = filter_by_designer(df, "Chanel")
print(f"Found {len(chanel):,} Chanel images")

# Filter by high aesthetic scores
high_quality = filter_by_aesthetic(df, min_score=6.0)
print(f"Found {len(high_quality):,} high-quality images")

# Complex filtering
spring_2022_rtw = df[
    (df['year'] == 2022) & 
    (df['season'] == 'Spring') & 
    (df['category'] == 'Ready-to-Wear')
]
```

### 3. Access Image Paths

```python
# Iterate through filtered results
for idx, row in spring_2022_rtw.iterrows():
    print(f"{row['designer']} - {row['season']} {row['year']}")
    print(f"  Image: {row['image_path']}")
    print(f"  Aesthetic: {row['aesthetic']}")
    print(f"  Tags: {row['tags']}")
    print()
```

### 4. Export Filtered Data

```python
from load_merged_dataset import export_by_year

# Export separate CSV files for each year
export_by_year(df, output_folder='output_by_year')
```

---

## Dataset Schema

Each row in the CSV contains:

| Column | Type | Description |
|--------|------|-------------|
| `key` | string | Unique identifier |
| `designer` | string | Designer/brand name |
| `season` | string | Spring, Fall, Resort, Pre-Fall |
| `year` | integer | Year of collection |
| `category` | string | Ready-to-Wear, Menswear, Couture, Bridal |
| `city` | string | Fashion week city (if available) |
| `section` | string | Collection, Details, Beauty, etc. |
| `width` | integer | Image width in pixels |
| `height` | integer | Image height in pixels |
| `size` | integer | File size in bytes |
| `aesthetic` | float | Aesthetic quality score (2.27-7.54) |
| `tags` | list | List of image tags/labels |
| `url` | string | Original Vogue URL |
| `filename` | string | Image filename |
| `json_path` | string | Path to JSON metadata file |
| `image_path` | string | Path to JPG image file |
| `has_image` | boolean | Whether image file exists |
| `source_folder` | string | Origin folder (030/065/124) |

---

## Example Queries

### Find all Versace collections from 2015-2020
```python
versace_2015_2020 = df[
    (df['designer'] == 'Versace') & 
    (df['year'] >= 2015) & 
    (df['year'] <= 2020)
]
print(f"Found {len(versace_2015_2020)} images")
```

### Get all Couture collections
```python
couture = df[df['category'] == 'Couture']
top_couture_designers = couture['designer'].value_counts().head(10)
print(top_couture_designers)
```

### Find high aesthetic Spring collections
```python
spring_high_quality = df[
    (df['season'] == 'Spring') & 
    (df['aesthetic'] > 5.5)
]
print(f"Found {len(spring_high_quality)} high-quality Spring images")
```

### Track a designer over time
```python
dior = df[df['designer'] == 'Christian Dior']
dior_timeline = dior.groupby('year').size()
print(dior_timeline)
```

---

## Regenerating the Dataset

If you need to regenerate the merged dataset:

```bash
# Create the merged dataset
python3 create_merged_dataset.py

# Generate visualizations
python3 visualize_merged_dataset.py

# Test with examples
python3 load_merged_dataset.py
```

---

## Dataset Features

✅ **Sorted by Year** - All entries chronologically ordered (1988-2023)  
✅ **No Missing Images** - All 30,000 images have corresponding files  
✅ **Rich Metadata** - Designer, season, category, tags, aesthetic scores  
✅ **Three Sources** - Merged from vogue_runway_030, 065, and 124  
✅ **Easy Filtering** - Helper functions for common queries  
✅ **Comprehensive Stats** - Detailed summaries and visualizations  
✅ **Well Documented** - Clear schema and examples  

---

## Timeline Highlights

- **1988-1999:** Early years (< 500 images total)
- **2000-2009:** Growing coverage (305 → 992 images/year)
- **2010-2015:** Rapid expansion (1,265 → 2,040 images/year)
- **2016:** 🔥 Peak year with 3,347 images
- **2017-2023:** Sustained high coverage (843-2,140 images/year)

---

## Common Use Cases

### Fashion Analysis
- Track designer evolution over time
- Analyze seasonal trends
- Compare aesthetic quality across brands

### Machine Learning
- Train image classification models
- Build recommendation systems
- Develop style recognition algorithms

### Data Science
- Temporal trend analysis
- Statistical pattern discovery
- Visual data mining

### Research
- Fashion history studies
- Cultural trend analysis
- Brand positioning research

---

## Support

For questions or issues with the dataset:

1. Check the summary file: `merged_dataset_summary.txt`
2. Run the example script: `python3 load_merged_dataset.py`
3. Review visualizations in `vogue_dataset_output/`

---

## License & Attribution

This dataset is derived from Vogue Runway. Please respect copyright and usage terms.  
Images remain property of their respective rights holders.

---

**Dataset Version:** 1.0  
**Created:** November 2025  
**Total Images:** 30,000  
**Format:** CSV + JSON + JPG  

---

*"Fashion is the armor to survive the reality of everyday life." - Bill Cunningham*


