"""
Visualization Module

Functions for creating compelling visualizations of color trends over time.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np


def plot_temporal_trends(yearly_stats, output_path=None):
    """
    Plot lightness and saturation trends over time.
    
    Args:
        yearly_stats: DataFrame with yearly statistics
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Lightness over time
    ax1.plot(yearly_stats.index, yearly_stats['mean_lightness'], 
             linewidth=2.5, color='#2E86AB', marker='o', markersize=4)
    ax1.fill_between(yearly_stats.index, yearly_stats['mean_lightness'], 
                      alpha=0.3, color='#2E86AB')
    ax1.set_ylabel('Mean Lightness (L*)', fontsize=12, fontweight='bold')
    ax1.set_title('Evolution of Color Lightness in Fashion', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(alpha=0.3)
    
    # Saturation over time
    ax2.plot(yearly_stats.index, yearly_stats['mean_saturation'], 
             linewidth=2.5, color='#E63946', marker='o', markersize=4)
    ax2.fill_between(yearly_stats.index, yearly_stats['mean_saturation'], 
                      alpha=0.3, color='#E63946')
    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Mean Saturation (Chroma)', fontsize=12, fontweight='bold')
    ax2.set_title('Evolution of Color Saturation in Fashion', 
                  fontsize=14, fontweight='bold', pad=20)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def plot_palette_heatmap(palette_by_year, top_palettes, output_path=None):
    """
    Create a heatmap of palette frequencies over time.
    
    Args:
        palette_by_year: DataFrame with palette frequencies by year
        top_palettes: List of palette IDs to include
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    # Create pivot table for heatmap
    palette_pivot = palette_by_year[
        palette_by_year['palette_id'].isin(top_palettes)
    ].pivot_table(
        index='palette_name',
        columns='year',
        values='percentage',
        fill_value=0
    )
    
    # Plot heatmap
    fig = plt.figure(figsize=(16, 10))
    sns.heatmap(palette_pivot, cmap='YlOrRd', 
                cbar_kws={'label': 'Percentage of Images (%)'}, 
                linewidths=0.5, linecolor='white', annot=False)
    plt.title('Sanzo Wada Palette Frequency Over Time\n(Top Palettes)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Sanzo Wada Palette', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def plot_color_diversity(yearly_stats, output_path=None):
    """
    Plot color diversity over time.
    
    Args:
        yearly_stats: DataFrame with yearly statistics
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    fig = plt.figure(figsize=(14, 6))
    plt.plot(yearly_stats.index, yearly_stats['color_diversity'], 
             linewidth=2.5, color='#06A77D', marker='o', markersize=5)
    plt.fill_between(yearly_stats.index, yearly_stats['color_diversity'], 
                      alpha=0.3, color='#06A77D')
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Color Diversity Index', fontsize=12, fontweight='bold')
    plt.title('Color Palette Diversity in Fashion Over Time', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def plot_decade_color_strips(decade_palettes_df, output_path=None):
    """
    Create color strips showing dominant palette for each decade.
    
    Args:
        decade_palettes_df: DataFrame with decade palette information
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    decades = decade_palettes_df['decade'].values
    n_decades = len(decades)
    
    fig, axes = plt.subplots(n_decades, 1, figsize=(14, n_decades * 1.5))
    if n_decades == 1:
        axes = [axes]
    
    for idx, row in decade_palettes_df.iterrows():
        decade = row['decade']
        palette_name = row['palette_name']
        palette_id = row['palette_id']
        n_images = row['n_images']
        percentage = row['percentage']
        colors_hex = row['colors']
        
        # Create color strip
        ax = axes[idx]
        for i, color in enumerate(colors_hex):
            ax.add_patch(mpatches.Rectangle(
                (i, 0), 1, 1, 
                facecolor=color, 
                edgecolor='white', 
                linewidth=2
            ))
        
        ax.set_xlim(0, len(colors_hex))
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add decade label
        ax.text(-0.5, 0.5, f"{decade}s\n({n_images} images)", 
                fontsize=11, fontweight='bold', va='center', ha='right')
        ax.text(len(colors_hex) + 0.5, 0.5, 
                f"{palette_name}\n({percentage:.1f}%)", 
                fontsize=10, va='center', ha='left', style='italic')
    
    plt.suptitle('Dominant Sanzo Wada Palettes by Decade', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def plot_top_palettes(df_results, n=10, output_path=None):
    """
    Plot bar chart of most common palettes.
    
    Args:
        df_results: DataFrame with color analysis results
        n: Number of top palettes to show
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    top_palettes = df_results['palette_id'].value_counts().head(n)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get palette names
    palette_names = []
    for pid in top_palettes.index:
        name = df_results[df_results['palette_id'] == pid]['palette_name'].iloc[0]
        palette_names.append(f"{name}\n({pid})")
    
    bars = ax.barh(palette_names, top_palettes.values, color='#457B9D')
    ax.set_xlabel('Number of Images', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {n} Most Common Sanzo Wada Palettes in Fashion Images', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(top_palettes.values) * 0.01, 
                bar.get_y() + bar.get_height()/2, 
                f'{int(width):,}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def plot_lab_distribution(df_results, output_path=None):
    """
    Plot LAB color space distribution.
    
    Args:
        df_results: DataFrame with color analysis results
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # A vs B (hue)
    scatter = axes[0].scatter(
        df_results['mean_a'], df_results['mean_b'], 
        c=df_results['year'], cmap='viridis', 
        alpha=0.5, s=20, edgecolors='none'
    )
    axes[0].set_xlabel('A* (Green ← → Red)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('B* (Blue ← → Yellow)', fontsize=11, fontweight='bold')
    axes[0].set_title('Color Distribution in LAB Space', fontsize=12, fontweight='bold')
    axes[0].axhline(y=128, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    axes[0].axvline(x=128, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    axes[0].grid(alpha=0.3)
    plt.colorbar(scatter, ax=axes[0], label='Year')
    
    # Lightness vs Saturation
    scatter2 = axes[1].scatter(
        df_results['mean_lightness'], df_results['mean_saturation'], 
        c=df_results['year'], cmap='viridis', 
        alpha=0.5, s=20, edgecolors='none'
    )
    axes[1].set_xlabel('Lightness (L*)', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Saturation (Chroma)', fontsize=11, fontweight='bold')
    axes[1].set_title('Lightness vs Saturation', fontsize=12, fontweight='bold')
    axes[1].grid(alpha=0.3)
    plt.colorbar(scatter2, ax=axes[1], label='Year')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def plot_seasonal_comparison(season_stats, output_path=None):
    """
    Compare color characteristics between seasons.
    
    Args:
        season_stats: DataFrame with seasonal statistics
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    seasons = season_stats.index
    metrics = ['mean_lightness', 'mean_saturation', 'color_diversity']
    titles = ['Lightness', 'Saturation', 'Color Diversity']
    colors = ['#2E86AB', '#E63946', '#06A77D']
    
    for i, (metric, title, color) in enumerate(zip(metrics, titles, colors)):
        axes[i].bar(seasons, season_stats[metric], color=color, alpha=0.7)
        axes[i].set_title(title, fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Season', fontsize=10)
        axes[i].set_ylabel('Value', fontsize=10)
        axes[i].grid(axis='y', alpha=0.3)
    
    plt.suptitle('Color Characteristics by Season', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig


def create_summary_visualization(yearly_stats, output_path=None):
    """
    Create a comprehensive 4-panel summary visualization.
    
    Args:
        yearly_stats: DataFrame with yearly statistics
        output_path: Optional path to save the figure
    
    Returns:
        matplotlib figure
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Panel 1: Lightness
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(yearly_stats.index, yearly_stats['mean_lightness'], 
             linewidth=2, color='#2E86AB', marker='o', markersize=3)
    ax1.fill_between(yearly_stats.index, yearly_stats['mean_lightness'], 
                      alpha=0.3, color='#2E86AB')
    ax1.set_xlabel('Year', fontweight='bold')
    ax1.set_ylabel('Mean Lightness', fontweight='bold')
    ax1.set_title('Lightness Trend', fontsize=13, fontweight='bold')
    ax1.grid(alpha=0.3)
    
    # Panel 2: Saturation
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(yearly_stats.index, yearly_stats['mean_saturation'], 
             linewidth=2, color='#E63946', marker='o', markersize=3)
    ax2.fill_between(yearly_stats.index, yearly_stats['mean_saturation'], 
                      alpha=0.3, color='#E63946')
    ax2.set_xlabel('Year', fontweight='bold')
    ax2.set_ylabel('Mean Saturation', fontweight='bold')
    ax2.set_title('Saturation Trend', fontsize=13, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # Panel 3: Diversity
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(yearly_stats.index, yearly_stats['color_diversity'], 
             linewidth=2, color='#06A77D', marker='o', markersize=3)
    ax3.fill_between(yearly_stats.index, yearly_stats['color_diversity'], 
                      alpha=0.3, color='#06A77D')
    ax3.set_xlabel('Year', fontweight='bold')
    ax3.set_ylabel('Color Diversity', fontweight='bold')
    ax3.set_title('Diversity Trend', fontsize=13, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # Panel 4: Image count
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.bar(yearly_stats.index, yearly_stats['n_images'], 
            color='#457B9D', alpha=0.7)
    ax4.set_xlabel('Year', fontweight='bold')
    ax4.set_ylabel('Number of Images', fontweight='bold')
    ax4.set_title('Dataset Coverage', fontsize=13, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Chromatic Mood of Fashion: Summary Dashboard', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {output_path}")
    
    return fig

