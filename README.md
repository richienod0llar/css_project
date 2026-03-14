# Chromatic Mood of Fashion Eras

**CSS WS25-26 Project** — Analyzing color palettes in Vogue runway images (1988–2025) using Sanzo Wada color theory.

## Overview

This project extracts dominant colors from ~30,000 Vogue runway photographs, maps them to [Sanzo Wada's](https://sanzo-wada.dmbk.io/) historical color palettes using perceptual color distance (ΔE 2000), and investigates how fashion's chromatic identity has shifted across decades, designers, and seasons.

The analysis pipeline feeds into an interactive scrollytelling web dashboard built with D3.js.

## Project Structure

```
project_css/
│
├── chromatic_utils/                        # Core Python package
│   ├── __init__.py
│   ├── color_extraction.py                 # K-Means clustering in CIELAB space
│   ├── sanzo_wada.py                       # Palette loading & ΔE 2000 mapping
│   ├── temporal_analysis.py                # Time-series aggregation
│   └── visualizations.py                   # Publication-ready plots
│
├── chromatic_analysis_output/              # Generated analysis results
│   ├── color_analysis_results.csv          # Per-image color extraction results
│   ├── yearly_statistics.csv               # Year-level aggregates
│   ├── decade_statistics.csv               # Decade-level aggregates
│   ├── decade_distances.csv                # Decade-to-decade color distances
│   ├── palette_by_year.csv                 # Palette frequency over time
│   ├── designer_analysis.csv               # Designer color preferences
│   ├── seasonal_analysis.csv               # Seasonal patterns
│   ├── hypothesis_results.csv              # Statistical hypothesis tests
│   ├── top_correlations.csv                # Feature correlations
│   ├── model_coefficients.csv              # Regression model coefficients
│   ├── event_effects_model.csv             # Historical event effects model
│   ├── event_period_summary.csv            # Event period summary statistics
│   ├── category_group_means.csv            # Category group means
│   ├── season_group_means.csv              # Season group means
│   ├── tag_effects_top.csv                 # Top tag effects
│   └── *.png                               # Visualization figures
│
├── interactive_viz/                        # Scrollytelling web dashboard
│   ├── index.html                          # Main HTML page
│   ├── styles.css                          # Stylesheet
│   ├── main.js                             # Compiled JS entry point
│   ├── src/
│   │   └── main.ts                         # TypeScript source
│   ├── chromatic_analysis_output/          # Data copy served to the browser
│   ├── package.json
│   ├── tsconfig.json
│   ├── .gitignore
│   ├── README.md
│   ├── GETTING_STARTED.md
│   └── PROJECT_STRUCTURE.md
│
├── vogue_dataset_output/                   # Merged dataset & summary plots
│   ├── vogue_runway_merged_30k.csv         # Combined Vogue metadata (30k rows)
│   ├── merged_dataset_summary.txt
│   └── *.png                               # Dataset distribution plots
│
├── vogue_runway_030/                       # Raw image datasets (gitignored)
├── vogue_runway_065/                       # ~60,000 runway images total
├── vogue_runway_124/
│
├── chromatic_mood_analysis.ipynb           # Main Jupyter notebook (interactive)
├── run_analysis.py                         # Batch color extraction pipeline
├── run_statistical_analysis.py             # Hypothesis testing & effects models
├── create_merged_dataset.py                # Merge raw CSVs into unified dataset
├── load_merged_dataset.py                  # Quick-load helper for merged data
├── visualize_merged_dataset.py             # Exploratory dataset visualizations
├── translate_palette_names.py              # Japanese → English palette names
├── requirements.txt                        # Python dependencies
├── WORKFLOW_SUMMARY.txt                    # Detailed pipeline description
└── .gitignore
```

## Tech Stack

| Layer | Tools |
|---|---|
| Color science | CIELAB color space, K-Means clustering, ΔE 2000 perceptual distance |
| Python | NumPy, Pandas, scikit-learn, colormath, Pillow, OpenCV, Matplotlib, Seaborn |
| Statistics | SciPy (hypothesis tests), OLS regression, effect-size analysis |
| Web | D3.js, Scrollama.js, TypeScript, HTML/CSS |

## Getting Started

### Prerequisites

- Python 3.8+
- (Optional) Node.js for TypeScript compilation

### Installation

```bash
pip install -r requirements.txt
```

### Running the Analysis

**Interactive (Jupyter):**
```bash
jupyter notebook chromatic_mood_analysis.ipynb
```

**Batch (command line):**
```bash
# Full run on all images
python run_analysis.py

# Quick test on 1,000 images
python run_analysis.py --sample 1000

# Statistical hypothesis testing (requires color_analysis_results.csv)
python run_statistical_analysis.py
```

Results are saved to `chromatic_analysis_output/`.

### Running the Web Dashboard

```bash
cd interactive_viz
python3 -m http.server 8000
# Open http://localhost:8000
```

## Pipeline

1. **Data preparation** — merge three Vogue runway CSV sources into a single dataset (`create_merged_dataset.py`)
2. **Color extraction** — resize each image to 256×256, convert to CIELAB, run K-Means (k=6) to find dominant colors (`run_analysis.py`)
3. **Palette mapping** — match extracted colors to Sanzo Wada's 348 palettes via ΔE 2000 distance
4. **Aggregation** — compute statistics by year, decade, designer, and season
5. **Hypothesis testing** — run statistical tests on temporal trends, category differences, and event effects (`run_statistical_analysis.py`)
6. **Visualization** — generate static plots and an interactive scrollytelling dashboard

## Key Parameters

| Parameter | Default | Description |
|---|---|---|
| `IMAGE_RESIZE` | 256 | Image dimension for processing |
| `N_CLUSTERS` | 6 | Dominant colors per image |
| `SAMPLE_SIZE` | None | Number of images (None = all ~30k) |
| `MIN_YEAR` | 1988 | Start year |
| `MAX_YEAR` | 2025 | End year |
