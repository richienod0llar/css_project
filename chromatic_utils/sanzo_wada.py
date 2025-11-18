"""
Sanzo Wada Palette Module

Functions for loading and mapping colors to the historical Sanzo Wada color palettes.
"""

import pandas as pd
import numpy as np
import requests
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from .color_extraction import lab_opencv_to_colormath


def load_sanzo_wada_palettes():
    """
    Load Sanzo Wada color palettes from GitHub or fallback data.
    
    Returns:
        DataFrame with palette information and LAB colors
    """
    print("Loading Sanzo Wada palettes...")
    
    # Try loading from GitHub
    url = "https://raw.githubusercontent.com/dblodorn/sanzo-wada/master/data.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        palettes_data = response.json()
        print("✓ Loaded palettes from GitHub")
    except Exception as e:
        print(f"Could not fetch from GitHub ({e}), using fallback dataset...")
        palettes_data = get_fallback_sanzo_wada()
    
    # Process palettes
    palette_records = []
    
    for palette in palettes_data:
        palette_id = palette.get('id', palette.get('name', 'unknown'))
        palette_name = palette.get('name', palette.get('id', 'Unknown'))
        colors = palette.get('colors', [])
        
        for color_hex in colors:
            # Convert HEX to RGB
            color_hex = color_hex.lstrip('#')
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            
            # Convert RGB to LAB using colormath
            rgb_color = sRGBColor(r/255.0, g/255.0, b/255.0)
            lab_color = convert_color(rgb_color, LabColor)
            
            palette_records.append({
                'palette_id': palette_id,
                'palette_name': palette_name,
                'hex': f"#{color_hex}",
                'r': r,
                'g': g,
                'b': b,
                'lab_l': lab_color.lab_l,
                'lab_a': lab_color.lab_a,
                'lab_b': lab_color.lab_b
            })
    
    df_palettes = pd.DataFrame(palette_records)
    print(f"✓ Loaded {len(df_palettes['palette_id'].unique())} palettes with {len(df_palettes)} colors")
    
    return df_palettes


def get_fallback_sanzo_wada():
    """
    Fallback Sanzo Wada palette dataset if API is unavailable.
    Representative subset of the 348 original palettes.
    
    Returns:
        List of palette dictionaries
    """
    return [
        {"id": "001", "name": "紅梅鼠", "colors": ["#917877", "#E9DFE0", "#D3BCB3", "#B97B6D"]},
        {"id": "002", "name": "海老茶", "colors": ["#772C25", "#AF4436", "#D7C4BB", "#E8D5C8"]},
        {"id": "003", "name": "深川鼠", "colors": ["#5B7E91", "#93B5C6", "#BBC8D4", "#D4E2E8"]},
        {"id": "004", "name": "桜鼠", "colors": ["#A88E87", "#E8D4CD", "#EAD7CE", "#F4E9E3"]},
        {"id": "005", "name": "藍鼠", "colors": ["#5C6D7C", "#8B9FAF", "#B2C2CE", "#D5E0E8"]},
        {"id": "006", "name": "柳鼠", "colors": ["#7F8A7F", "#A8B5A8", "#C5D0C5", "#DEE5DE"]},
        {"id": "007", "name": "鴬茶", "colors": ["#6C5B3D", "#A08C68", "#C9B897", "#E5D9C1"]},
        {"id": "008", "name": "海松茶", "colors": ["#5B6356", "#8C9486", "#B7C0B2", "#D8DED4"]},
        {"id": "009", "name": "紺青", "colors": ["#003854", "#1E5A74", "#4A7C92", "#76A0B3"]},
        {"id": "010", "name": "臙脂", "colors": ["#AB2D3A", "#C74654", "#DC8189", "#ECBCC0"]},
        {"id": "011", "name": "鶯色", "colors": ["#6C6B2C", "#949438", "#B9B95A", "#D9D98C"]},
        {"id": "012", "name": "鶸茶", "colors": ["#8F8526", "#B7AE45", "#CEC870", "#E3DC9A"]},
        {"id": "013", "name": "青磁色", "colors": ["#78AFA3", "#9AC8BE", "#BDD9D1", "#DEE9E5"]},
        {"id": "014", "name": "小豆色", "colors": ["#6F3430", "#954E47", "#B87C76", "#D9B3AE"]},
        {"id": "015", "name": "水色", "colors": ["#7DB9DE", "#A0CFE8", "#BFE0F0", "#DEEFF7"]},
        {"id": "016", "name": "芥子色", "colors": ["#C4972F", "#D9B44A", "#E5C76B", "#EFE0A2"]},
        {"id": "017", "name": "牡丹色", "colors": ["#E03C8A", "#ED6EA7", "#F49EC0", "#FAD0DC"]},
        {"id": "018", "name": "青緑", "colors": ["#00A497", "#00BFB0", "#5CD1C7", "#A3E5DE"]},
        {"id": "019", "name": "山吹色", "colors": ["#F5B800", "#F8C500", "#FAD64B", "#FCE78C"]},
        {"id": "020", "name": "桃色", "colors": ["#F19CA7", "#F5B5BD", "#F9CFD4", "#FCE8EA"]},
        {"id": "021", "name": "露草色", "colors": ["#2F5DA6", "#5580BE", "#7FA3D1", "#B3CCE5"]},
        {"id": "022", "name": "萌黄", "colors": ["#8FC31F", "#A7D143", "#BFDD6E", "#D9EBA3"]},
        {"id": "023", "name": "浅葱色", "colors": ["#00A3AF", "#00BCC9", "#4DD2DC", "#99E5EC"]},
        {"id": "024", "name": "紅色", "colors": ["#D71345", "#E64166", "#F07B95", "#F9BEC7"]},
        {"id": "025", "name": "紫", "colors": ["#884898", "#A367B1", "#BE8DCA", "#DCBFE7"]},
        {"id": "026", "name": "鼠色", "colors": ["#787878", "#9B9B9B", "#BEBEBE", "#E0E0E0"]},
        {"id": "027", "name": "墨色", "colors": ["#3A3A3A", "#5E5E5E", "#828282", "#A6A6A6"]},
        {"id": "028", "name": "白群", "colors": ["#83CCD2", "#A3DAE0", "#C3E8ED", "#E3F6F8"]},
        {"id": "029", "name": "若草色", "colors": ["#C3D825", "#D3E445", "#E3F06B", "#F3FC9B"]},
        {"id": "030", "name": "桜色", "colors": ["#FEEEED", "#FDD5D3", "#FCBCB9", "#FBA3A0"]},
    ]


def find_closest_wada_palette(lab_colors, df_sanzo, weights=None):
    """
    Map extracted colors to the closest Sanzo Wada palette.
    
    Uses the delta E 2000 color difference metric to find the palette
    that best matches the extracted colors.
    
    Args:
        lab_colors: Array of LAB colors (OpenCV scale)
        df_sanzo: DataFrame with Sanzo Wada palettes
        weights: Optional weights for each color (e.g., proportions)
    
    Returns:
        Dictionary with palette_id, palette_name, and mean_distance
    """
    if weights is None:
        weights = np.ones(len(lab_colors)) / len(lab_colors)
    
    # Convert extracted colors to colormath format
    extracted_lab = [lab_opencv_to_colormath(color) for color in lab_colors]
    
    # Calculate minimum distance for each extracted color to any Wada color
    palette_scores = {}
    
    for palette_id in df_sanzo['palette_id'].unique():
        palette_colors = df_sanzo[df_sanzo['palette_id'] == palette_id]
        
        # For each extracted color, find min distance to this palette
        weighted_distances = []
        
        for i, extracted_color in enumerate(extracted_lab):
            min_delta_e = float('inf')
            
            for _, wada_color in palette_colors.iterrows():
                wada_lab = LabColor(
                    wada_color['lab_l'], 
                    wada_color['lab_a'], 
                    wada_color['lab_b']
                )
                delta_e = delta_e_cie2000(extracted_color, wada_lab)
                min_delta_e = min(min_delta_e, delta_e)
            
            weighted_distances.append(min_delta_e * weights[i])
        
        palette_scores[palette_id] = np.sum(weighted_distances)
    
    # Find best matching palette
    best_palette_id = min(palette_scores, key=palette_scores.get)
    best_score = palette_scores[best_palette_id]
    best_name = df_sanzo[df_sanzo['palette_id'] == best_palette_id]['palette_name'].iloc[0]
    
    return {
        'palette_id': best_palette_id,
        'palette_name': best_name,
        'mean_distance': best_score
    }


def get_palette_colors(df_sanzo, palette_id):
    """
    Get all colors for a specific palette.
    
    Args:
        df_sanzo: DataFrame with Sanzo Wada palettes
        palette_id: ID of the palette
    
    Returns:
        DataFrame with colors from the palette
    """
    return df_sanzo[df_sanzo['palette_id'] == palette_id].copy()

