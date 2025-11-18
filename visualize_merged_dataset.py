#!/usr/bin/env python3
"""
Script to create visualizations for the merged Vogue Runway dataset (30K images).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

def load_data():
    """Load the merged dataset."""
    csv_path = Path(__file__).parent / "vogue_dataset_output" / "vogue_runway_merged_30k.csv"
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df):,} images")
    return df

def plot_images_per_year(df, output_folder):
    """Plot images distribution by year."""
    plt.figure(figsize=(18, 7))
    year_counts = df['year'].value_counts().sort_index()
    
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(year_counts)))
    bars = plt.bar(year_counts.index, year_counts.values, color=colors, edgecolor='black', alpha=0.8, linewidth=0.5)
    
    # Highlight peak years
    max_year = year_counts.idxmax()
    max_idx = list(year_counts.index).index(max_year)
    bars[max_idx].set_color('crimson')
    bars[max_idx].set_alpha(1.0)
    
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Images', fontsize=14, fontweight='bold')
    plt.title('Vogue Runway Images Distribution by Year (30K Dataset)\nSorted by Year', 
              fontsize=16, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    
    # Add annotation for peak year
    plt.annotate(f'Peak: {max_year}\n({year_counts.max()} images)', 
                xy=(max_year, year_counts.max()),
                xytext=(max_year-5, year_counts.max()+300),
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', color='black', lw=2))
    
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_images_per_year.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_top_designers(df, output_folder):
    """Plot top 20 designers."""
    plt.figure(figsize=(14, 10))
    
    top_designers = df['designer'].value_counts().head(20)
    
    colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(top_designers)))
    bars = plt.barh(range(len(top_designers)), top_designers.values, color=colors, 
                     edgecolor='black', alpha=0.8, linewidth=0.8)
    
    plt.yticks(range(len(top_designers)), top_designers.index, fontsize=11)
    plt.xlabel('Number of Images', fontsize=13, fontweight='bold')
    plt.ylabel('Designer', fontsize=13, fontweight='bold')
    plt.title('Top 20 Designers by Image Count (30K Dataset)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_designers.values)):
        plt.text(value + 5, i, f'{value}', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_top_designers.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_category_distribution(df, output_folder):
    """Plot category distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Bar chart
    category_counts = df['category'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = ax1.bar(range(len(category_counts)), category_counts.values, 
                   color=colors, edgecolor='black', alpha=0.8, linewidth=1)
    ax1.set_xticks(range(len(category_counts)))
    ax1.set_xticklabels(category_counts.index, fontsize=11, fontweight='bold')
    ax1.set_ylabel('Number of Images', fontsize=13, fontweight='bold')
    ax1.set_title('Category Distribution - Bar Chart', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar, value in zip(bars, category_counts.values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}\n({value/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Pie chart
    wedges, texts, autotexts = ax2.pie(category_counts.values, labels=category_counts.index,
                                         colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Category Distribution - Pie Chart', fontsize=14, fontweight='bold', pad=15)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_category_distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_season_distribution(df, output_folder):
    """Plot season distribution."""
    plt.figure(figsize=(14, 7))
    
    season_counts = df['season'].value_counts()
    season_order = ['Spring', 'Resort', 'Fall', 'Pre-Fall']
    season_counts = season_counts.reindex(season_order)
    
    colors = ['#FFB6C1', '#87CEEB', '#FF8C00', '#8B4513']
    bars = plt.bar(range(len(season_counts)), season_counts.values,
                   color=colors, edgecolor='black', alpha=0.8, linewidth=1)
    
    plt.xticks(range(len(season_counts)), season_counts.index, fontsize=12, fontweight='bold')
    plt.ylabel('Number of Images', fontsize=13, fontweight='bold')
    plt.title('Season Distribution (30K Dataset)', fontsize=16, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar, value in zip(bars, season_counts.values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}\n({value/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_season_distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_aesthetic_distribution(df, output_folder):
    """Plot aesthetic score distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Histogram
    ax1.hist(df['aesthetic'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.axvline(df['aesthetic'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["aesthetic"].mean():.2f}')
    ax1.axvline(df['aesthetic'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["aesthetic"].median():.2f}')
    ax1.set_xlabel('Aesthetic Score', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax1.set_title('Aesthetic Score Distribution - Histogram', fontsize=14, fontweight='bold', pad=15)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # Box plot
    box = ax2.boxplot(df['aesthetic'], vert=True, patch_artist=True,
                      boxprops=dict(facecolor='lightblue', color='black', linewidth=1.5),
                      whiskerprops=dict(color='black', linewidth=1.5),
                      capprops=dict(color='black', linewidth=1.5),
                      medianprops=dict(color='red', linewidth=2))
    ax2.set_ylabel('Aesthetic Score', fontsize=13, fontweight='bold')
    ax2.set_title('Aesthetic Score Distribution - Box Plot', fontsize=14, fontweight='bold', pad=15)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add statistics text
    stats_text = f'Min: {df["aesthetic"].min():.2f}\nQ1: {df["aesthetic"].quantile(0.25):.2f}\n' \
                 f'Median: {df["aesthetic"].median():.2f}\nQ3: {df["aesthetic"].quantile(0.75):.2f}\n' \
                 f'Max: {df["aesthetic"].max():.2f}\nMean: {df["aesthetic"].mean():.2f}\nStd: {df["aesthetic"].std():.2f}'
    ax2.text(1.15, df["aesthetic"].median(), stats_text, fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_aesthetic_distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_source_folders(df, output_folder):
    """Plot distribution across source folders."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    folder_counts = df['source_folder'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    
    # Bar chart
    bars = ax1.bar(range(len(folder_counts)), folder_counts.values,
                   color=colors, edgecolor='black', alpha=0.8, linewidth=1)
    ax1.set_xticks(range(len(folder_counts)))
    ax1.set_xticklabels(folder_counts.index, fontsize=11, fontweight='bold')
    ax1.set_ylabel('Number of Images', fontsize=13, fontweight='bold')
    ax1.set_title('Source Folder Distribution - Bar Chart', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars, folder_counts.values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Pie chart
    wedges, texts, autotexts = ax2.pie(folder_counts.values, labels=folder_counts.index,
                                         colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Source Folder Distribution - Pie Chart', fontsize=14, fontweight='bold', pad=15)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_source_folders.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_designer_timeline(df, output_folder, top_n=15):
    """Plot timeline heatmap of top designers."""
    # Get top designers
    top_designers = df['designer'].value_counts().head(top_n).index
    
    # Create pivot table
    designer_year = df[df['designer'].isin(top_designers)].groupby(['designer', 'year']).size().unstack(fill_value=0)
    
    # Create heatmap
    plt.figure(figsize=(20, 10))
    sns.heatmap(designer_year, cmap='YlOrRd', linewidths=0.5, linecolor='gray',
                cbar_kws={'label': 'Number of Images'}, annot=False, fmt='d')
    
    plt.xlabel('Year', fontsize=13, fontweight='bold')
    plt.ylabel('Designer', fontsize=13, fontweight='bold')
    plt.title(f'Top {top_n} Designers Timeline Heatmap (30K Dataset)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    output_path = Path(output_folder) / "merged_designer_timeline.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def main():
    """Generate all visualizations."""
    print("=" * 60)
    print("Generating Visualizations for Merged Dataset (30K)")
    print("=" * 60)
    print()
    
    # Load data
    df = load_data()
    
    # Output folder
    output_folder = Path(__file__).parent / "vogue_dataset_output"
    output_folder.mkdir(exist_ok=True)
    
    print(f"\nGenerating visualizations...")
    print("-" * 60)
    
    # Generate all plots
    plot_images_per_year(df, output_folder)
    plot_top_designers(df, output_folder)
    plot_category_distribution(df, output_folder)
    plot_season_distribution(df, output_folder)
    plot_aesthetic_distribution(df, output_folder)
    plot_source_folders(df, output_folder)
    plot_designer_timeline(df, output_folder, top_n=15)
    
    print("-" * 60)
    print(f"\n✓ All visualizations saved to: {output_folder}")
    print()
    print("Generated files:")
    print("  - merged_images_per_year.png")
    print("  - merged_top_designers.png")
    print("  - merged_category_distribution.png")
    print("  - merged_season_distribution.png")
    print("  - merged_aesthetic_distribution.png")
    print("  - merged_source_folders.png")
    print("  - merged_designer_timeline.png")
    print()
    print("=" * 60)
    print("✓ VISUALIZATION COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()


