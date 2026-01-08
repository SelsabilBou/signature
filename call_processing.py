# call_processing.py

from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage
from skimage.morphology import skeletonize

def process_image(image_path):
    
    try:
        print(f"\n{'='*60}")
        print(f"Processing image: {image_path}")
        print(f"{'='*60}\n")
        
        # Load image
        img = Image.open(image_path)
        print(f"✓ Image loaded successfully: {img.size[0]}x{img.size[1]} pixels")
        
        # Step 1: Noise Removal (Median Filter)
        img_denoised = noise_removal(img)
        print(f"✓ Noise removal completed (Median Filter applied)")
        
        # Step 2: Preprocessing
        img_gray = convert_to_grayscale(img_denoised)
        print(f"✓ Converted to grayscale")
        
        img_binary = binarization(img_gray)
        print(f"✓ Binarization completed")
        
        img_skeleton = skeletonization(img_binary)
        print(f"✓ Skeletonization completed")
        
        # Step 3: Feature Extraction
        features = extract_features(img_binary, img_skeleton)
        print(f"\n{'='*60}")
        print(f"FEATURE EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"Width:              {features['width']} pixels")
        print(f"Height:             {features['height']} pixels")
        print(f"Black Pixel Count:  {features['black_pixels']} pixels")
        print(f"Skeleton Pixels:    {features['skeleton_pixels']} pixels")
        print(f"Aspect Ratio:       {features['aspect_ratio']:.2f}")
        print(f"Density:            {features['density']:.4f}")
        print(f"{'='*60}\n")
        
        return {
            'success': True,
            'features': features,
            'processed_images': {
                'original': img,
                'grayscale': img_gray,
                'binary': img_binary,
                'skeleton': img_skeleton
            }
        }
        
    except Exception as e:
        print(f"\n❌ Error processing image: {str(e)}\n")
        return {
            'success': False,
            'error': str(e),
            'features': None
        }


def noise_removal(image):
    """Apply median filter to remove noise"""
    # Apply median filter with radius 2
    denoised = image.filter(ImageFilter.MedianFilter(size=3))
    return denoised


def convert_to_grayscale(image):
    """Convert image to grayscale"""
    return image.convert('L')


def binarization(image):
    """Convert grayscale image to binary (black and white)"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Apply Otsu's thresholding
    threshold = 127
    binary_array = (img_array < threshold).astype(np.uint8) * 255
    
    # Convert back to PIL Image
    binary_img = Image.fromarray(binary_array, mode='L')
    return binary_img


def skeletonization(image):
    """Apply skeletonization to binary image"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Convert to binary (0 and 1)
    binary = (img_array < 128).astype(bool)
    
    # Apply skeletonization
    skeleton = skeletonize(binary)
    
    # Convert back to image format (0-255)
    skeleton_img = (skeleton * 255).astype(np.uint8)
    
    return Image.fromarray(skeleton_img, mode='L')


def extract_features(binary_image, skeleton_image):
    """
    Extract features from processed signature:
    - Width and Height
    - Black pixel count
    - Skeleton pixel count
    - Aspect ratio
    - Density
    """
    # Convert images to numpy arrays
    binary_array = np.array(binary_image)
    skeleton_array = np.array(skeleton_image)
    
    # Get dimensions
    height, width = binary_array.shape
    
    # Count black pixels in binary image
    black_pixels = np.count_nonzero(binary_array < 128)
    
    # Count skeleton pixels
    skeleton_pixels = np.count_nonzero(skeleton_array > 0)
    
    # Calculate aspect ratio
    aspect_ratio = width / height if height > 0 else 0
    
    # Calculate density (black pixels / total pixels)
    total_pixels = width * height
    density = black_pixels / total_pixels if total_pixels > 0 else 0
    
    features = {
        'width': width,
        'height': height,
        'black_pixels': black_pixels,
        'skeleton_pixels': skeleton_pixels,
        'aspect_ratio': aspect_ratio,
        'density': density
    }
    
    return features


def compare_signatures(features1, features2, tolerance=0.2):
    """
    Compare two signature feature sets
    Returns True if signatures match within tolerance
    """
    if features1 is None or features2 is None:
        return False
    
    # Compare key features with tolerance
    width_match = abs(features1['width'] - features2['width']) / max(features1['width'], features2['width']) < tolerance
    height_match = abs(features1['height'] - features2['height']) / max(features1['height'], features2['height']) < tolerance
    pixels_match = abs(features1['black_pixels'] - features2['black_pixels']) / max(features1['black_pixels'], features2['black_pixels']) < tolerance
    
    # All features must match
    return width_match and height_match and pixels_match
