#!/usr/bin/env python3
"""
Script to create a merged dataset from all three Vogue Runway folders:
- vogue_runway_030 (10k images)
- vogue_runway_065 (10k images)  
- vogue_runway_124 (10k images)

Total: 30k images, sorted by year.
"""

import json
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict
import shutil

def load_metadata_from_folder(folder_path: str) -> List[Dict]:
    """
    Load all JSON metadata files from a folder.
    
    Args:
        folder_path: Path to the vogue_runway folder
        
    Returns:
        List of metadata dictionaries
    """
    folder = Path(folder_path)
    metadata_list = []
    
    if not folder.exists():
        print(f"Warning: Folder {folder} does not exist!")
        return metadata_list
    
    # Find all JSON files
    json_files = list(folder.glob("*.json"))
    print(f"  Found {len(json_files)} JSON metadata files in {folder.name}")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Add the file paths
                data['json_path'] = str(json_file)
                data['source_folder'] = folder.name
                
                # Check if corresponding image exists
                image_path = json_file.with_suffix('.jpg')
                if image_path.exists():
                    data['image_path'] = str(image_path)
                    data['has_image'] = True
                else:
                    data['image_path'] = None
                    data['has_image'] = False
                
                metadata_list.append(data)
                
        except Exception as e:
            print(f"    Error reading {json_file.name}: {e}")
            continue
    
    return metadata_list


def load_all_folders(base_folder: Path, folder_names: List[str]) -> List[Dict]:
    """
    Load metadata from multiple folders.
    
    Args:
        base_folder: Base directory containing the folders
        folder_names: List of folder names to process
        
    Returns:
        Combined list of all metadata dictionaries
    """
    all_metadata = []
    
    print("Loading metadata from all folders...")
    print("-" * 60)
    
    for folder_name in folder_names:
        folder_path = base_folder / folder_name
        print(f"\nProcessing: {folder_name}")
        metadata = load_metadata_from_folder(folder_path)
        all_metadata.extend(metadata)
        print(f"  Loaded: {len(metadata)} entries")
    
    print("-" * 60)
    print(f"\nTotal metadata entries loaded: {len(all_metadata)}")
    
    return all_metadata


def create_sorted_dataset(metadata_list: List[Dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the metadata list, sorted by year.
    
    Args:
        metadata_list: List of metadata dictionaries
        
    Returns:
        Pandas DataFrame sorted by year and season
    """
    df = pd.DataFrame(metadata_list)
    
    # Sort by year (and season within year for better organization)
    # Map seasons to numeric values for sorting
    season_order = {'Spring': 1, 'Resort': 2, 'Fall': 3, 'Pre-Fall': 4}
    df['season_order'] = df['season'].map(season_order).fillna(5)
    
    # Sort by year (ascending), then by season, then by designer
    df = df.sort_values(['year', 'season_order', 'designer']).reset_index(drop=True)
    
    # Drop the temporary sorting column
    df = df.drop('season_order', axis=1)
    
    return df


def save_merged_dataset(df: pd.DataFrame, output_folder: str):
    """
    Save the merged dataset to CSV and create a summary.
    
    Args:
        df: DataFrame containing the dataset
        output_folder: Path to save the output files
    """
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    
    # Save complete dataset as CSV
    csv_path = output_path / "vogue_runway_merged_30k.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\n✓ Merged dataset saved to: {csv_path}")
    print(f"  Total entries: {len(df)}")
    
    # Create summary statistics
    summary_path = output_path / "merged_dataset_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("VOGUE RUNWAY MERGED DATASET SUMMARY (30K)\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Total images: {len(df)}\n")
        f.write(f"Images with files: {df['has_image'].sum()}\n")
        f.write(f"Missing images: {(~df['has_image']).sum()}\n\n")
        
        f.write(f"Year range: {df['year'].min()} - {df['year'].max()}\n\n")
        
        f.write("Source folders:\n")
        folder_counts = df['source_folder'].value_counts()
        for folder, count in folder_counts.items():
            f.write(f"  {folder}: {count} images\n")
        f.write("\n")
        
        f.write("Images per year:\n")
        year_counts = df['year'].value_counts().sort_index()
        for year, count in year_counts.items():
            f.write(f"  {year}: {count}\n")
        f.write("\n")
        
        f.write("Top 20 designers by image count:\n")
        designer_counts = df['designer'].value_counts().head(20)
        for designer, count in designer_counts.items():
            f.write(f"  {designer}: {count}\n")
        f.write("\n")
        
        f.write("Categories:\n")
        category_counts = df['category'].value_counts()
        for category, count in category_counts.items():
            f.write(f"  {category}: {count}\n")
        f.write("\n")
        
        f.write("Seasons:\n")
        season_counts = df['season'].value_counts()
        for season, count in season_counts.items():
            f.write(f"  {season}: {count}\n")
        f.write("\n")
        
        f.write("Aesthetic score statistics:\n")
        if 'aesthetic' in df.columns:
            f.write(f"  Mean: {df['aesthetic'].mean():.2f}\n")
            f.write(f"  Median: {df['aesthetic'].median():.2f}\n")
            f.write(f"  Min: {df['aesthetic'].min():.2f}\n")
            f.write(f"  Max: {df['aesthetic'].max():.2f}\n")
    
    print(f"✓ Summary saved to: {summary_path}")
    
    # Display summary to console
    print("\n" + "=" * 60)
    print("MERGED DATASET SUMMARY")
    print("=" * 60)
    print(f"Total images: {len(df)}")
    print(f"Images with files: {df['has_image'].sum()}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    
    print(f"\nSource folders:")
    for folder, count in folder_counts.items():
        print(f"  {folder}: {count} images")
    
    print(f"\nTop 10 years with most images:")
    top_years = df['year'].value_counts().head(10)
    for year, count in top_years.items():
        print(f"  {year}: {count} images")
    
    print(f"\nTop 10 designers:")
    top_designers = df['designer'].value_counts().head(10)
    for designer, count in top_designers.items():
        print(f"  {designer}: {count} images")
    
    print(f"\nFirst 5 entries (oldest):")
    print(df[['key', 'designer', 'season', 'year', 'category', 'source_folder']].head().to_string())
    
    print(f"\nLast 5 entries (newest):")
    print(df[['key', 'designer', 'season', 'year', 'category', 'source_folder']].tail().to_string())


def main():
    """Main function to create the merged sorted dataset."""
    # Set paths
    base_folder = Path(__file__).parent
    output_folder = base_folder / "vogue_dataset_output"
    
    # Define the three folders to merge
    folders_to_process = [
        "vogue_runway_030",
        "vogue_runway_065",
        "vogue_runway_124"
    ]
    
    print("=" * 60)
    print("Creating Merged Vogue Runway Dataset (30K)")
    print("=" * 60)
    print(f"\nSource folders:")
    for folder in folders_to_process:
        print(f"  - {folder}")
    print(f"\nOutput folder: {output_folder}")
    print()
    
    # Load metadata from all folders
    all_metadata = load_all_folders(base_folder, folders_to_process)
    
    if not all_metadata:
        print("\n❌ Error: No metadata found in any folder!")
        return
    
    # Create sorted dataset
    print("\nCreating and sorting merged dataset...")
    df = create_sorted_dataset(all_metadata)
    
    # Save merged dataset
    save_merged_dataset(df, output_folder)
    
    print("\n" + "=" * 60)
    print("✓ MERGED DATASET CREATION COMPLETE!")
    print("=" * 60)
    print(f"\nYou can now access:")
    print(f"  - CSV file: {output_folder}/vogue_runway_merged_30k.csv")
    print(f"  - Summary: {output_folder}/merged_dataset_summary.txt")
    print(f"\nTo load this dataset in your code:")
    print(f"  import pandas as pd")
    print(f"  df = pd.read_csv('{output_folder}/vogue_runway_merged_30k.csv')")
    print()


if __name__ == "__main__":
    main()




