"""
Chromatic Mood Analysis Utilities

A comprehensive toolkit for analyzing color trends in fashion imagery.
"""

__version__ = "1.0.0"
__author__ = "Chromatic Mood Project"

from .color_extraction import (
    load_and_preprocess_image,
    rgb_to_lab,
    extract_dominant_colors_lab,
    lab_to_rgb,
    lab_opencv_to_colormath,
    calculate_color_statistics
)

from .sanzo_wada import (
    load_sanzo_wada_palettes,
    find_closest_wada_palette,
    translate_palette_name,
    PALETTE_NAME_TRANSLATIONS
)

from .temporal_analysis import (
    aggregate_by_year,
    aggregate_by_decade,
    get_palette_frequency_by_year,
    get_dominant_palette_per_decade,
    compute_decade_color_distance,
    analyze_by_designer,
    analyze_by_season
)

from .visualizations import (
    plot_temporal_trends,
    plot_palette_heatmap,
    plot_color_diversity,
    plot_decade_color_strips,
    plot_top_palettes,
    plot_lab_distribution,
    plot_seasonal_comparison,
    create_summary_visualization
)

__all__ = [
    # Color extraction
    'load_and_preprocess_image',
    'rgb_to_lab',
    'extract_dominant_colors_lab',
    'lab_to_rgb',
    'lab_opencv_to_colormath',
    'calculate_color_statistics',
    
    # Sanzo Wada
    'load_sanzo_wada_palettes',
    'find_closest_wada_palette',
    'translate_palette_name',
    'PALETTE_NAME_TRANSLATIONS',
    
    # Temporal analysis
    'aggregate_by_year',
    'aggregate_by_decade',
    'get_palette_frequency_by_year',
    'get_dominant_palette_per_decade',
    'compute_decade_color_distance',
    'analyze_by_designer',
    'analyze_by_season',
    
    # Visualizations
    'plot_temporal_trends',
    'plot_palette_heatmap',
    'plot_color_diversity',
    'plot_decade_color_strips',
    'plot_top_palettes',
    'plot_lab_distribution',
    'plot_seasonal_comparison',
    'create_summary_visualization'
]

