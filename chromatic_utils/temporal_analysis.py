"""
Temporal Analysis Module

Functions for analyzing color trends over time, by decade, designer, and season.
"""

import pandas as pd
import numpy as np
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000


def aggregate_by_year(df_results):
    """
    Aggregate color statistics by year.
    
    Args:
        df_results: DataFrame with color analysis results
    
    Returns:
        DataFrame with yearly statistics
    """
    yearly_stats = df_results.groupby('year').agg({
        'mean_lightness': 'mean',
        'mean_saturation': 'mean',
        'color_diversity': 'mean',
        'palette_distance': 'mean',
        'key': 'count'
    }).rename(columns={'key': 'n_images'})
    
    return yearly_stats


def aggregate_by_decade(df_results):
    """
    Aggregate color statistics by decade.
    
    Args:
        df_results: DataFrame with color analysis results
    
    Returns:
        DataFrame with decade statistics
    """
    df_with_decade = df_results.copy()
    df_with_decade['decade'] = (df_with_decade['year'] // 10) * 10
    
    decade_stats = df_with_decade.groupby('decade').agg({
        'mean_lightness': 'mean',
        'mean_saturation': 'mean',
        'color_diversity': 'mean',
        'key': 'count'
    }).rename(columns={'key': 'n_images'})
    
    return decade_stats


def get_palette_frequency_by_year(df_results):
    """
    Calculate palette frequency by year.
    
    Args:
        df_results: DataFrame with color analysis results
    
    Returns:
        DataFrame with palette frequencies
    """
    palette_by_year = df_results.groupby(
        ['year', 'palette_id', 'palette_name']
    ).size().reset_index(name='count')
    
    palette_by_year['percentage'] = palette_by_year.groupby('year')['count'].transform(
        lambda x: 100 * x / x.sum()
    )
    
    return palette_by_year


def compute_decade_color_distance(df_results):
    """
    Compute color distance (Delta E) between consecutive decades.
    
    Args:
        df_results: DataFrame with color analysis results
    
    Returns:
        DataFrame with decade-to-decade color distances
    """
    df_with_decade = df_results.copy()
    df_with_decade['decade'] = (df_with_decade['year'] // 10) * 10
    
    decades = sorted(df_with_decade['decade'].unique())
    distances = []
    
    for i in range(len(decades) - 1):
        decade1 = decades[i]
        decade2 = decades[i + 1]
        
        d1_data = df_with_decade[df_with_decade['decade'] == decade1]
        d2_data = df_with_decade[df_with_decade['decade'] == decade2]
        
        # Compare mean LAB values
        lab1 = LabColor(
            d1_data['mean_lightness'].mean() * 100 / 255,
            d1_data['mean_a'].mean() - 128,
            d1_data['mean_b'].mean() - 128
        )
        lab2 = LabColor(
            d2_data['mean_lightness'].mean() * 100 / 255,
            d2_data['mean_a'].mean() - 128,
            d2_data['mean_b'].mean() - 128
        )
        
        delta_e = delta_e_cie2000(lab1, lab2)
        
        distances.append({
            'decade1': decade1,
            'decade2': decade2,
            'transition': f"{decade1}s → {decade2}s",
            'color_distance': delta_e
        })
    
    return pd.DataFrame(distances)


def analyze_by_designer(df_results, min_images=50):
    """
    Analyze color preferences by designer.
    
    Args:
        df_results: DataFrame with color analysis results
        min_images: Minimum number of images required
    
    Returns:
        DataFrame with designer color statistics
    """
    designer_stats = df_results.groupby('designer').agg({
        'mean_lightness': 'mean',
        'mean_saturation': 'mean',
        'color_diversity': 'mean',
        'key': 'count'
    }).rename(columns={'key': 'n_images'})
    
    designer_stats = designer_stats[designer_stats['n_images'] >= min_images]
    designer_stats = designer_stats.sort_values('n_images', ascending=False)
    
    return designer_stats


def analyze_by_season(df_results):
    """
    Analyze color differences between Spring and Fall collections.
    
    Args:
        df_results: DataFrame with color analysis results
    
    Returns:
        DataFrame with seasonal color statistics
    """
    season_stats = df_results.groupby('season').agg({
        'mean_lightness': 'mean',
        'mean_saturation': 'mean',
        'color_diversity': 'mean',
        'key': 'count'
    }).rename(columns={'key': 'n_images'})
    
    return season_stats


def get_top_palettes(df_results, n=10):
    """
    Get the most common palettes overall.
    
    Args:
        df_results: DataFrame with color analysis results
        n: Number of top palettes to return
    
    Returns:
        Series with palette counts
    """
    return df_results['palette_id'].value_counts().head(n)


def get_dominant_palette_per_decade(df_results, df_sanzo):
    """
    Get the most common palette for each decade.
    
    Args:
        df_results: DataFrame with color analysis results
        df_sanzo: DataFrame with Sanzo Wada palettes
    
    Returns:
        DataFrame with decade and dominant palette info
    """
    df_with_decade = df_results.copy()
    df_with_decade['decade'] = (df_with_decade['year'] // 10) * 10
    
    decade_palettes = []
    
    for decade in sorted(df_with_decade['decade'].unique()):
        decade_data = df_with_decade[df_with_decade['decade'] == decade]
        top_palette_id = decade_data['palette_id'].value_counts().index[0]
        top_palette_name = decade_data[
            decade_data['palette_id'] == top_palette_id
        ]['palette_name'].iloc[0]
        
        count = decade_data[decade_data['palette_id'] == top_palette_id].shape[0]
        percentage = 100 * count / len(decade_data)
        
        # Get colors for this palette
        palette_colors = df_sanzo[df_sanzo['palette_id'] == top_palette_id]['hex'].tolist()
        
        decade_palettes.append({
            'decade': decade,
            'palette_id': top_palette_id,
            'palette_name': top_palette_name,
            'count': count,
            'percentage': percentage,
            'n_images': len(decade_data),
            'colors': palette_colors
        })
    
    return pd.DataFrame(decade_palettes)



