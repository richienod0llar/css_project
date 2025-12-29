# Quick Start Guide: Chromatic Mood Analysis

Get started analyzing fashion color trends in 5 minutes!

## Installation (2 minutes)

```bash
# Navigate to project
cd "/Users/richienodollar/Desktop/stats master/ws25/css/project_css"

# Install dependencies
pip install -r requirements.txt
```

## Run Analysis (Choose One)

### Option A: Jupyter Notebook (Interactive)

```bash
jupyter notebook chromatic_mood_analysis.ipynb
```

Then click "Run All" in the Cell menu.

### Option B: Standalone Script

```bash
# Full dataset (~2-4 hours)
python run_analysis.py

# Quick test with 1000 images (~5 minutes)
python run_analysis.py --sample 1000
```

## Results

Find all outputs in `chromatic_analysis_output/`:

**Data Files:**
- `color_analysis_results.csv` - Main results
- `yearly_statistics.csv` - Trends over time
- `designer_analysis.csv` - Designer color preferences

**Visualizations:**
- `summary_dashboard.png` - Overview
- `temporal_trends.png` - Lightness/saturation evolution
- `palette_heatmap.png` - Palette frequencies
- `decade_strips.png` - Dominant colors by decade

## Key Parameters

Edit in notebook or use command-line flags:

```python
SAMPLE_SIZE = 1000    # For testing (None = all images)
N_CLUSTERS = 6        # Dominant colors per image
IMAGE_RESIZE = 256    # Processing size
```

Command line:
```bash
python run_analysis.py --sample 1000 --clusters 6 --resize 256
```

## Example Output

```
CHROMATIC MOOD OF FASHION ERAS
================================================================================

Dataset Summary:
  - Images analyzed: 29,847
  - Year range: 1988-2025
  - Designers: 1,247
  - Unique palettes matched: 30

Color Trends:
  - Mean lightness: 142.35
  - Mean saturation: 45.67
  - Mean diversity: 38.21

Top 3 Palettes:
  1. 紅梅鼠 (001): 2,847 images (9.5%)
  2. 深川鼠 (003): 2,156 images (7.2%)
  3. 桜鼠 (004): 1,923 images (6.4%)
```

## Troubleshooting

**Module not found?**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Out of memory?**
```python
IMAGE_RESIZE = 128  # Smaller size
SAMPLE_SIZE = 5000  # Process fewer images
```

**Missing images?**
Check that image paths in CSV are correct and images exist.

## Next Steps

1. **Explore Results**: Open generated PNG files and CSV data
2. **Customize Analysis**: Modify parameters in notebook
3. **Add Visualizations**: Use functions in `chromatic_utils/`
4. **Filter Data**: Analyze specific designers, years, or seasons

## Need Help?

- Read full documentation: `README_CHROMATIC_MOOD.md`
- Check module docs: `chromatic_utils/`
- Review example notebook cells

**Happy analyzing! 🎨**



