#!/usr/bin/env python3
"""
Chromatic Mood of Fashion Eras - Standalone Script

This script runs the complete color analysis pipeline without requiring Jupyter.
Results are saved to the chromatic_analysis_output/ directory.

Usage:
    python run_analysis.py

For testing with a smaller sample:
    python run_analysis.py --sample 1000
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# Import our custom modules
from chromatic_utils import (
    extract_dominant_colors_lab,
    calculate_color_statistics,
    load_sanzo_wada_palettes,
    find_closest_wada_palette,
    aggregate_by_year,
    aggregate_by_decade,
    get_palette_frequency_by_year,
    get_dominant_palette_per_decade,
    compute_decade_color_distance,
    analyze_by_designer,
    analyze_by_season,
    plot_temporal_trends,
    plot_palette_heatmap,
    plot_color_diversity,
    plot_decade_color_strips,
    plot_top_palettes,
    plot_lab_distribution,
    plot_seasonal_comparison,
    create_summary_visualization
)


def main():
    """Main analysis pipeline"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run chromatic mood analysis')
    parser.add_argument('--sample', type=int, default=None,
                      help='Sample size for testing (e.g., 1000)')
    parser.add_argument('--clusters', type=int, default=6,
                      help='Number of color clusters (default: 6)')
    parser.add_argument('--resize', type=int, default=256,
                      help='Image resize dimension (default: 256)')
    args = parser.parse_args()
    
    print("=" * 80)
    print("CHROMATIC MOOD OF FASHION ERAS")
    print("=" * 80)
    print()
    
    # Configuration
    DATA_CSV = Path('vogue_dataset_output/vogue_runway_merged_30k.csv')
    OUTPUT_DIR = Path('chromatic_analysis_output')
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    IMAGE_RESIZE = args.resize
    N_CLUSTERS = args.clusters
    SAMPLE_SIZE = args.sample
    MIN_YEAR = 1988
    MAX_YEAR = 2025
    
    print(f"Configuration:")
    print(f"  - Output directory: {OUTPUT_DIR.absolute()}")
    print(f"  - Image resize: {IMAGE_RESIZE}px")
    print(f"  - Color clusters: {N_CLUSTERS}")
    print(f"  - Sample size: {SAMPLE_SIZE or 'All images'}")
    print()
    
    # Step 1: Load data
    print("Step 1: Loading dataset...")
    try:
        df = pd.read_csv(DATA_CSV)
        print(f"  ✓ Loaded {len(df):,} images")
    except FileNotFoundError:
        print(f"  ✗ Error: Could not find {DATA_CSV}")
        print("  Please ensure the CSV file exists in vogue_dataset_output/")
        sys.exit(1)
    
    # Filter and clean
    df = df[(df['year'] >= MIN_YEAR) & (df['year'] <= MAX_YEAR)].copy()
    df = df[df['has_image'] == True].copy()
    df = df.dropna(subset=['image_path', 'year'])
    
    if SAMPLE_SIZE:
        df = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=42)
        print(f"  ✓ Sampled to {len(df):,} images")
    
    df = df.reset_index(drop=True)
    print(f"  ✓ Filtered: {len(df):,} images ({df['year'].min()}-{df['year'].max()})")
    print()
    
    # Step 2: Load Sanzo Wada palettes
    print("Step 2: Loading Sanzo Wada palettes...")
    df_sanzo = load_sanzo_wada_palettes()
    print()
    
    # Step 3: Extract colors and map to palettes
    print("Step 3: Extracting colors and mapping to palettes...")
    print("  (This may take several minutes...)")
    
    results = []
    errors = 0
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="  Processing"):
        image_path = row['image_path']
        
        # Extract colors
        color_data = extract_dominant_colors_lab(
            image_path, 
            n_colors=N_CLUSTERS, 
            target_size=IMAGE_RESIZE
        )
        
        if color_data is None:
            errors += 1
            continue
        
        # Map to Sanzo Wada
        wada_match = find_closest_wada_palette(
            color_data['colors_lab'],
            df_sanzo,
            weights=color_data['proportions']
        )
        
        # Calculate statistics
        stats = calculate_color_statistics(
            color_data['colors_lab'], 
            color_data['proportions']
        )
        
        results.append({
            'key': row['key'],
            'designer': row['designer'],
            'year': row['year'],
            'season': row['season'],
            'category': row['category'],
            'image_path': image_path,
            'palette_id': wada_match['palette_id'],
            'palette_name': wada_match['palette_name'],
            'palette_distance': wada_match['mean_distance'],
            **stats
        })
    
    df_results = pd.DataFrame(results)
    print(f"  ✓ Successfully processed {len(df_results):,} images")
    if errors > 0:
        print(f"  ⚠ Skipped {errors} images due to errors")
    
    # Save results
    results_path = OUTPUT_DIR / 'color_analysis_results.csv'
    df_results.to_csv(results_path, index=False)
    print(f"  ✓ Saved results to {results_path}")
    print()
    
    # Step 4: Temporal analysis
    print("Step 4: Computing temporal statistics...")
    
    yearly_stats = aggregate_by_year(df_results)
    decade_stats = aggregate_by_decade(df_results)
    palette_by_year = get_palette_frequency_by_year(df_results)
    decade_palettes = get_dominant_palette_per_decade(df_results, df_sanzo)
    decade_distances = compute_decade_color_distance(df_results)
    
    # Save analysis results
    yearly_stats.to_csv(OUTPUT_DIR / 'yearly_statistics.csv')
    decade_stats.to_csv(OUTPUT_DIR / 'decade_statistics.csv')
    palette_by_year.to_csv(OUTPUT_DIR / 'palette_by_year.csv', index=False)
    decade_distances.to_csv(OUTPUT_DIR / 'decade_distances.csv', index=False)
    
    print(f"  ✓ Analyzed {len(yearly_stats)} years")
    print(f"  ✓ Analyzed {len(decade_stats)} decades")
    print()
    
    # Step 5: Additional analyses
    print("Step 5: Computing additional analyses...")
    
    season_stats = analyze_by_season(df_results)
    designer_stats = analyze_by_designer(df_results, min_images=50)
    
    season_stats.to_csv(OUTPUT_DIR / 'seasonal_analysis.csv')
    designer_stats.to_csv(OUTPUT_DIR / 'designer_analysis.csv')
    
    print(f"  ✓ Seasonal analysis complete")
    print(f"  ✓ Designer analysis complete ({len(designer_stats)} designers)")
    print()
    
    # Step 6: Generate visualizations
    print("Step 6: Generating visualizations...")
    
    top_palettes = df_results['palette_id'].value_counts().head(15).index.tolist()
    
    viz_tasks = [
        ('Summary dashboard', lambda: create_summary_visualization(
            yearly_stats, OUTPUT_DIR / 'summary_dashboard.png')),
        ('Temporal trends', lambda: plot_temporal_trends(
            yearly_stats, OUTPUT_DIR / 'temporal_trends.png')),
        ('Palette heatmap', lambda: plot_palette_heatmap(
            palette_by_year, top_palettes, OUTPUT_DIR / 'palette_heatmap.png')),
        ('Color diversity', lambda: plot_color_diversity(
            yearly_stats, OUTPUT_DIR / 'color_diversity.png')),
        ('Decade color strips', lambda: plot_decade_color_strips(
            decade_palettes, OUTPUT_DIR / 'decade_strips.png')),
        ('Top palettes', lambda: plot_top_palettes(
            df_results, n=10, output_path=OUTPUT_DIR / 'top_palettes.png')),
        ('LAB distribution', lambda: plot_lab_distribution(
            df_results, OUTPUT_DIR / 'lab_distribution.png')),
        ('Seasonal comparison', lambda: plot_seasonal_comparison(
            season_stats, OUTPUT_DIR / 'seasonal_comparison.png')),
    ]
    
    for name, func in viz_tasks:
        try:
            func()
            plt.close('all')  # Clean up
        except Exception as e:
            print(f"  ⚠ Error creating {name}: {e}")
    
    print()
    
    # Summary report
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print(f"Dataset Summary:")
    print(f"  - Images analyzed: {len(df_results):,}")
    print(f"  - Year range: {df_results['year'].min()}-{df_results['year'].max()}")
    print(f"  - Designers: {df_results['designer'].nunique():,}")
    print(f"  - Unique palettes matched: {df_results['palette_id'].nunique()}")
    print()
    print(f"Color Trends:")
    print(f"  - Mean lightness: {df_results['mean_lightness'].mean():.2f}")
    print(f"  - Mean saturation: {df_results['mean_saturation'].mean():.2f}")
    print(f"  - Mean diversity: {df_results['color_diversity'].mean():.2f}")
    print()
    print(f"Top 3 Palettes:")
    for i, (pid, count) in enumerate(df_results['palette_id'].value_counts().head(3).items(), 1):
        name = df_results[df_results['palette_id'] == pid]['palette_name'].iloc[0]
        pct = 100 * count / len(df_results)
        print(f"  {i}. {name} ({pid}): {count:,} images ({pct:.1f}%)")
    print()
    print(f"All results saved to: {OUTPUT_DIR.absolute()}")
    print()
    print("Output files:")
    for f in sorted(OUTPUT_DIR.glob('*')):
        print(f"  - {f.name}")
    print()
    print("=" * 80)
    print("✓ Analysis pipeline completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()

