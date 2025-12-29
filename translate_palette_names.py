"""
Script to translate Japanese palette names to English in existing CSV files.
"""

import pandas as pd
from pathlib import Path

# Japanese to English translation mapping (same as in sanzo_wada.py)
PALETTE_NAME_TRANSLATIONS = {
    "紅梅鼠": "Plum Mouse Gray",
    "海老茶": "Shrimp Brown",
    "深川鼠": "Fukagawa Mouse Gray",
    "桜鼠": "Cherry Mouse Gray",
    "藍鼠": "Indigo Mouse Gray",
    "柳鼠": "Willow Mouse Gray",
    "鴬茶": "Nightingale Brown",
    "海松茶": "Seaweed Brown",
    "紺青": "Navy Blue",
    "臙脂": "Crimson",
    "鶯色": "Nightingale Green",
    "鶸茶": "Siskin Brown",
    "青磁色": "Celadon",
    "小豆色": "Azuki Bean Red",
    "水色": "Water Blue",
    "芥子色": "Mustard",
    "牡丹色": "Peony Pink",
    "青緑": "Blue-Green",
    "山吹色": "Yamabuki Yellow",
    "桃色": "Peach",
    "露草色": "Dayflower Blue",
    "萌黄": "Spring Green",
    "浅葱色": "Light Indigo",
    "紅色": "Crimson Red",
    "紫": "Purple",
    "鼠色": "Mouse Gray",
    "墨色": "Ink Black",
    "白群": "Pale Blue-Green",
    "若草色": "Young Grass Green",
    "桜色": "Cherry Blossom Pink"
}

def translate_palette_name(japanese_name):
    """Translate Japanese palette name to English."""
    return PALETTE_NAME_TRANSLATIONS.get(japanese_name, japanese_name)

def update_csv_file(file_path):
    """Update palette names in a CSV file."""
    print(f"\nProcessing: {file_path}")
    
    # Read the CSV
    df = pd.read_csv(file_path)
    
    # Check if palette_name column exists
    if 'palette_name' not in df.columns:
        print(f"  ⚠️  No 'palette_name' column found, skipping")
        return
    
    # Count original Japanese names
    japanese_count = df['palette_name'].apply(
        lambda x: x in PALETTE_NAME_TRANSLATIONS
    ).sum()
    
    # Translate the names
    df['palette_name'] = df['palette_name'].apply(translate_palette_name)
    
    # Save back to CSV
    df.to_csv(file_path, index=False)
    
    print(f"  ✓ Translated {japanese_count} palette names")
    print(f"  ✓ Updated {len(df)} rows")

def main():
    """Main function to update all CSV files."""
    print("="*60)
    print("Translating Palette Names: Japanese → English")
    print("="*60)
    
    # Define output directory
    output_dir = Path("chromatic_analysis_output")
    
    # List of CSV files to update
    csv_files = [
        output_dir / "palette_by_year.csv",
        output_dir / "color_analysis_results.csv",
        output_dir / "seasonal_analysis.csv",
        output_dir / "designer_analysis.csv",
    ]
    
    # Update each file
    total_processed = 0
    for csv_file in csv_files:
        if csv_file.exists():
            update_csv_file(csv_file)
            total_processed += 1
        else:
            print(f"\n⚠️  File not found: {csv_file}")
    
    print("\n" + "="*60)
    print(f"✓ Translation complete! Processed {total_processed} files.")
    print("="*60)
    
    # Show sample of updated data
    print("\nSample from palette_by_year.csv:")
    palette_by_year = output_dir / "palette_by_year.csv"
    if palette_by_year.exists():
        df = pd.read_csv(palette_by_year)
        print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()



