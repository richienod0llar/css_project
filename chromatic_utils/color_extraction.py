"""
Color Extraction Module for Chromatic Mood Analysis

This module provides functions for extracting dominant colors from images
using K-Means clustering in the LAB color space.
"""

import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans
from colormath.color_objects import LabColor


def load_and_preprocess_image(image_path, target_size=256):
    """
    Load an image and prepare it for color extraction.
    
    Args:
        image_path: Path to the image file
        target_size: Resize to this dimension (square)
    
    Returns:
        numpy array in RGB format, or None if error
    """
    try:
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize maintaining aspect ratio
        img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
        
        return np.array(img)
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None


def rgb_to_lab(rgb_array):
    """
    Convert RGB image to LAB color space.
    
    Args:
        rgb_array: numpy array in RGB format (0-255)
    
    Returns:
        numpy array in LAB format
    """
    # OpenCV expects BGR
    bgr = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    return lab


def extract_dominant_colors_lab(image_path, n_colors=5, target_size=256):
    """
    Extract dominant colors from an image using K-Means in LAB color space.
    
    Args:
        image_path: Path to image
        n_colors: Number of dominant colors to extract
        target_size: Resize dimension
    
    Returns:
        Dictionary with LAB colors and their proportions, or None if error
    """
    # Load image
    rgb_img = load_and_preprocess_image(image_path, target_size)
    if rgb_img is None:
        return None
    
    # Convert to LAB
    lab_img = rgb_to_lab(rgb_img)
    
    # Reshape for clustering
    pixels = lab_img.reshape(-1, 3)
    
    # Remove very dark/light pixels (potential backgrounds)
    # L channel: 0 (black) to 100 (white) in LAB, but OpenCV uses 0-255 scale
    mask = (pixels[:, 0] > 10) & (pixels[:, 0] < 245)
    pixels_filtered = pixels[mask]
    
    if len(pixels_filtered) < n_colors:
        pixels_filtered = pixels
    
    # K-Means clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels_filtered)
    
    # Get colors and their proportions
    colors_lab = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # Calculate proportions
    unique, counts = np.unique(labels, return_counts=True)
    proportions = counts / len(labels)
    
    return {
        'colors_lab': colors_lab,
        'proportions': proportions
    }


def lab_to_rgb(lab_color):
    """
    Convert LAB color (OpenCV scale) to RGB.
    
    Args:
        lab_color: Array [L, A, B] in OpenCV scale (0-255, 0-255, 0-255)
    
    Returns:
        RGB tuple (0-255)
    """
    lab_pixel = np.uint8([[lab_color]])
    bgr_pixel = cv2.cvtColor(lab_pixel, cv2.COLOR_LAB2BGR)
    rgb_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2RGB)
    return tuple(rgb_pixel[0][0])


def lab_opencv_to_colormath(lab_opencv):
    """
    Convert OpenCV LAB (0-255 scale) to colormath LAB.
    
    OpenCV: L [0, 255], A [0, 255], B [0, 255]
    CIE LAB: L [0, 100], A [-128, 127], B [-128, 127]
    
    Args:
        lab_opencv: Array-like [L, A, B] in OpenCV scale
    
    Returns:
        colormath LabColor object
    """
    L = (lab_opencv[0] / 255.0) * 100.0
    A = lab_opencv[1] - 128.0
    B = lab_opencv[2] - 128.0
    return LabColor(L, A, B)


def calculate_color_statistics(lab_colors, proportions):
    """
    Calculate color statistics from LAB colors.
    
    Args:
        lab_colors: Array of LAB colors (OpenCV scale)
        proportions: Array of color proportions
    
    Returns:
        Dictionary of statistics
    """
    # Weighted averages
    mean_lightness = np.average(lab_colors[:, 0], weights=proportions)
    mean_a = np.average(lab_colors[:, 1], weights=proportions)
    mean_b = np.average(lab_colors[:, 2], weights=proportions)
    
    # Saturation (chroma) = sqrt(a^2 + b^2)
    chromas = np.sqrt((lab_colors[:, 1] - 128)**2 + (lab_colors[:, 2] - 128)**2)
    mean_saturation = np.average(chromas, weights=proportions)
    
    # Color diversity (std of colors)
    color_diversity = np.std(lab_colors, axis=0).mean()
    
    return {
        'mean_lightness': mean_lightness,
        'mean_a': mean_a,
        'mean_b': mean_b,
        'mean_saturation': mean_saturation,
        'color_diversity': color_diversity
    }



