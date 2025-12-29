#!/usr/bin/env python3
"""
Helper script to load and explore the merged Vogue Runway dataset (30K images).
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def load_merged_dataset(csv_path=None):
    """
    Load the merged Vogue Runway dataset (30K images).
    
    Args:
        csv_path: Path to the CSV file. If None, uses default location.
        
    Returns:
        Pandas DataFrame
    """
    if csv_path is None:
        csv_path = Path(__file__).parent / "vogue_dataset_output" / "vogue_runway_merged_30k.csv"
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df):,} images")
    print(f"Years: {df['year'].min()} - {df['year'].max()}")
    print(f"Source folders: {', '.join(df['source_folder'].unique())}")
    return df


def filter_by_year(df, start_year=None, end_year=None):
    """
    Filter dataset by year range.
    
    Args:
        df: DataFrame to filter
        start_year: Minimum year (inclusive)
        end_year: Maximum year (inclusive)
        
    Returns:
        Filtered DataFrame
    """
    if start_year is not None:
        df = df[df['year'] >= start_year]
    if end_year is not None:
        df = df[df['year'] <= end_year]
    return df


def filter_by_designer(df, designer):
    """
    Filter dataset by designer name.
    
    Args:
        df: DataFrame to filter
        designer: Designer name (case-insensitive, partial match)
        
    Returns:
        Filtered DataFrame
    """
    return df[df['designer'].str.contains(designer, case=False, na=False)]


def filter_by_category(df, category):
    """
    Filter dataset by category.
    
    Args:
        df: DataFrame to filter
        category: Category name ('Ready-to-Wear', 'Menswear', 'Couture', 'Bridal')
        
    Returns:
        Filtered DataFrame
    """
    return df[df['category'] == category]


def filter_by_season(df, season):
    """
    Filter dataset by season.
    
    Args:
        df: DataFrame to filter
        season: Season name ('Spring', 'Fall', 'Resort', 'Pre-Fall')
        
    Returns:
        Filtered DataFrame
    """
    return df[df['season'] == season]


def filter_by_aesthetic(df, min_score=None, max_score=None):
    """
    Filter dataset by aesthetic score range.
    
    Args:
        df: DataFrame to filter
        min_score: Minimum aesthetic score (inclusive)
        max_score: Maximum aesthetic score (inclusive)
        
    Returns:
        Filtered DataFrame
    """
    if min_score is not None:
        df = df[df['aesthetic'] >= min_score]
    if max_score is not None:
        df = df[df['aesthetic'] <= max_score]
    return df


def get_images_by_year(df):
    """
    Get count of images per year.
    
    Args:
        df: DataFrame
        
    Returns:
        Series with year as index and count as values
    """
    return df['year'].value_counts().sort_index()


def get_top_designers(df, n=20):
    """
    Get top N designers by image count.
    
    Args:
        df: DataFrame
        n: Number of top designers to return
        
    Returns:
        Series with designer names and counts
    """
    return df['designer'].value_counts().head(n)


def get_stats_summary(df):
    """
    Print a comprehensive summary of the dataset.
    
    Args:
        df: DataFrame
    """
    print("\n" + "=" * 60)
    print("DATASET STATISTICS")
    print("=" * 60)
    
    print(f"\nTotal images: {len(df):,}")
    print(f"Images with files: {df['has_image'].sum():,}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    
    print(f"\nSource folders:")
    for folder, count in df['source_folder'].value_counts().items():
        print(f"  {folder}: {count:,} images")
    
    print(f"\nCategories:")
    for category, count in df['category'].value_counts().items():
        print(f"  {category}: {count:,} images")
    
    print(f"\nSeasons:")
    for season, count in df['season'].value_counts().items():
        print(f"  {season}: {count:,} images")
    
    print(f"\nAesthetic scores:")
    if 'aesthetic' in df.columns:
        print(f"  Mean: {df['aesthetic'].mean():.2f}")
        print(f"  Median: {df['aesthetic'].median():.2f}")
        print(f"  Min: {df['aesthetic'].min():.2f}")
        print(f"  Max: {df['aesthetic'].max():.2f}")
        print(f"  Std: {df['aesthetic'].std():.2f}")


def plot_images_per_year(df, save_path=None):
    """
    Plot the distribution of images per year.
    
    Args:
        df: DataFrame
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=(16, 6))
    year_counts = df['year'].value_counts().sort_index()
    
    plt.bar(year_counts.index, year_counts.values, color='steelblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Images', fontsize=12)
    plt.title('Vogue Runway Images Distribution by Year (30K Dataset)', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()


def export_by_year(df, output_folder):
    """
    Export CSV files organized by year.
    
    Args:
        df: DataFrame
        output_folder: Path to create year-based CSV files
    """
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    
    years = sorted(df['year'].unique())
    
    print(f"Exporting {len(years)} year-based CSV files...")
    
    for year in years:
        year_df = df[df['year'] == year]
        year_csv = output_path / f"vogue_{year}.csv"
        year_df.to_csv(year_csv, index=False)
        print(f"  {year}: {len(year_df)} images -> {year_csv.name}")
    
    print(f"\n✓ Export complete! Files saved in {output_folder}")


def main():
    """Example usage of the helper functions."""
    # Load the merged dataset
    df = load_merged_dataset()
    
    # Print comprehensive statistics
    get_stats_summary(df)
    
    print("\n" + "=" * 60)
    print("EXAMPLE QUERIES")
    print("=" * 60)
    
    # Example 1: Filter by year range
    print("\n1. Images from 2020-2023:")
    recent = filter_by_year(df, start_year=2020, end_year=2023)
    print(f"   Found {len(recent):,} images")
    
    # Example 2: Filter by designer
    print("\n2. Chanel images:")
    chanel = filter_by_designer(df, "Chanel")
    print(f"   Found {len(chanel):,} images")
    print(f"   Years: {chanel['year'].min()} - {chanel['year'].max()}")
    
    # Example 3: Top designers
    print("\n3. Top 10 designers:")
    top_designers = get_top_designers(df, n=10)
    for i, (designer, count) in enumerate(top_designers.items(), 1):
        print(f"   {i}. {designer}: {count:,} images")
    
    # Example 4: Filter by category and season
    print("\n4. Spring Ready-to-Wear collections:")
    spring_rtw = df[(df['season'] == 'Spring') & (df['category'] == 'Ready-to-Wear')]
    print(f"   Found {len(spring_rtw):,} images")
    
    # Example 5: High aesthetic score images
    print("\n5. Images with aesthetic score > 6.0:")
    high_aesthetic = filter_by_aesthetic(df, min_score=6.0)
    print(f"   Found {len(high_aesthetic):,} images ({len(high_aesthetic)/len(df)*100:.1f}%)")
    
    # Example 6: Designer timeline
    print("\n6. Christian Dior collections over time:")
    dior = filter_by_designer(df, "Christian Dior")
    dior_years = dior['year'].value_counts().sort_index()
    print(f"   Total: {len(dior):,} images from {dior['year'].min()} to {dior['year'].max()}")
    print(f"   Peak year: {dior_years.idxmax()} with {dior_years.max()} images")
    
    print("\n" + "=" * 60)
    print("USAGE IN YOUR CODE")
    print("=" * 60)
    print("""
from load_merged_dataset import load_merged_dataset, filter_by_year, filter_by_designer

# Load dataset
df = load_merged_dataset()

# Complex filtering
recent_chanel = df[(df['designer'] == 'Chanel') & 
                   (df['year'] >= 2020) & 
                   (df['aesthetic'] > 5.5)]

# Access image paths
for idx, row in recent_chanel.iterrows():
    image_path = row['image_path']
    print(f"{row['designer']} {row['season']} {row['year']}: {image_path}")
    """)


if __name__ == "__main__":
    main()




