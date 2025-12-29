# Chromatic Mood of Fashion Eras

A comprehensive Python workflow for analyzing how color palettes in fashion runway images evolve over time, using the historical Sanzo Wada color dataset.

## Overview

This project analyzes ~30,000 Vogue runway images spanning from 1988 to 2025, extracting dominant colors using K-Means clustering in the LAB color space and mapping them to the 348 historical color palettes documented by Sanzo Wada in the early 1900s.

## Features

- **Perceptually Accurate Color Extraction**: Uses LAB color space and K-Means clustering for accurate color analysis
- **Historical Color Mapping**: Maps modern fashion colors to Sanzo Wada's traditional Japanese palettes
- **Temporal Analysis**: Tracks evolution of lightness, saturation, and color diversity over decades
- **Rich Visualizations**: Creates publication-ready charts, heatmaps, and dashboards
- **Modular Architecture**: Clean, reusable Python modules for easy extension

## Installation

### Requirements

- Python 3.8 or higher
- pip or conda for package management

### Setup

1. Clone or navigate to the project directory:

```bash
cd "/Users/richienodollar/Desktop/stats master/ws25/css/project_css"
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or using conda:

```bash
conda create -n chromatic python=3.9
conda activate chromatic
pip install -r requirements.txt
```

## Project Structure

```
project_css/
├── chromatic_mood_analysis.ipynb   # Main Jupyter notebook
├── run_analysis.py                 # Standalone script version
├── requirements.txt                # Python dependencies
├── chromatic_utils/                # Core modules
│   ├── __init__.py
│   ├── color_extraction.py         # Color extraction functions
│   ├── sanzo_wada.py              # Palette loading and mapping
│   ├── temporal_analysis.py        # Time-series analysis
│   └── visualizations.py           # Plotting functions
├── vogue_dataset_output/
│   └── vogue_runway_merged_30k.csv # Input dataset
└── chromatic_analysis_output/      # Results directory (created on run)
```

## Usage

### Option 1: Jupyter Notebook (Recommended)

```bash
jupyter notebook chromatic_mood_analysis.ipynb
```

Then run all cells to perform the complete analysis. The notebook includes:
- Interactive parameter configuration
- Step-by-step explanations
- Inline visualizations
- Export functionality

### Option 2: Standalone Script

```bash
python run_analysis.py
```

This runs the complete pipeline and saves all outputs to `chromatic_analysis_output/`.

### Configuration

Edit the configuration section in the notebook or script:

```python
# Processing parameters
IMAGE_RESIZE = 256      # Image size for processing (faster)
N_CLUSTERS = 6          # Number of dominant colors to extract
SAMPLE_SIZE = None      # Set to int (e.g., 1000) for quick testing

# Analysis parameters
MIN_YEAR = 1988
MAX_YEAR = 2025
```

## Output Files

After running the analysis, you'll find:

### Data Files
- `color_analysis_results.csv` - Complete color analysis for all images
- `yearly_statistics.csv` - Aggregated statistics by year
- `decade_distances.csv` - Color distance between decades
- `designer_analysis.csv` - Color preferences by designer
- `seasonal_analysis.csv` - Seasonal color differences

### Visualizations
- `summary_dashboard.png` - 4-panel overview of key trends
- `temporal_trends.png` - Lightness and saturation over time
- `palette_heatmap.png` - Palette frequency heatmap
- `color_diversity.png` - Diversity evolution
- `decade_strips.png` - Dominant palettes per decade
- `top_palettes.png` - Most common palettes
- `lab_distribution.png` - Color space distributions
- `seasonal_comparison.png` - Spring vs Fall colors

## Methodology

### 1. Color Extraction
- Images resized to 256×256 for efficiency
- RGB converted to LAB color space (perceptually uniform)
- K-Means clustering (k=6) identifies dominant colors
- Color proportions weighted by pixel count

### 2. Palette Mapping
- Sanzo Wada dataset: 348 palettes, ~1,400 colors
- Each extracted color mapped using ΔE 2000 (perceptual color difference)
- Image assigned to palette with minimum weighted distance

### 3. Temporal Analysis
- Yearly aggregation of lightness, saturation, diversity
- Decade-to-decade color distance (ΔE 2000)
- Palette frequency tracking
- Designer and seasonal comparisons

## Key Findings

Example insights you can extract:

- **Lightness trends**: Are fashion colors getting lighter or darker?
- **Saturation shifts**: Movement toward vivid or muted palettes
- **Palette evolution**: Which traditional palettes dominate each era?
- **Seasonal patterns**: Spring collections lighter than Fall?
- **Designer signatures**: Color preferences of major designers

## Extending the Project

### Add New Visualizations

```python
from chromatic_utils import visualizations

# Create custom plot
def plot_my_analysis(df_results):
    # Your visualization code
    pass
```

### Analyze Specific Designers

```python
from chromatic_utils import analyze_by_designer

designer_colors = analyze_by_designer(df_results, min_images=100)
```

### Use Different Color Palettes

Replace the Sanzo Wada loader in `chromatic_utils/sanzo_wada.py` with your own palette dataset.

## Dependencies

Core libraries:
- **numpy** & **pandas**: Data manipulation
- **Pillow** & **opencv-python**: Image processing
- **scikit-learn**: K-Means clustering
- **colormath**: Perceptual color science (LAB, ΔE 2000)
- **matplotlib** & **seaborn**: Visualization
- **tqdm**: Progress tracking

## Performance Notes

- **Full dataset** (~30k images): 2-4 hours depending on hardware
- **Sample** (1000 images): ~5-10 minutes
- Use `SAMPLE_SIZE` parameter for quick testing
- Processing time scales linearly with image count

## Troubleshooting

### Import Errors

```bash
# Ensure chromatic_utils is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Memory Issues

Reduce `IMAGE_RESIZE` or process in batches.

### Network Issues (Sanzo Wada)

The code includes a fallback dataset if GitHub is unreachable. You can also manually download palettes from https://github.com/dblodorn/sanzo-wada

## Citation

If you use this code in academic work, please cite:

```
Chromatic Mood of Fashion Eras
URL: [Your repository URL]
Year: 2025
```

Sanzo Wada color data:
```
Wada, Sanzo. "A Dictionary of Color Combinations" (1933)
Digital version: https://github.com/dblodorn/sanzo-wada
```

## License

This project is provided for educational and research purposes.

## Contact

For questions or collaboration:
- Open an issue on GitHub
- Email: [your email]

## Acknowledgments

- Sanzo Wada's timeless color palettes
- Vogue runway image dataset
- The colormath library maintainers

---

**Happy Color Analysis! 🎨**



