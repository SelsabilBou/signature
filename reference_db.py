# reference_db.py (Phase 4)
import os
import numpy as np
import cv2
from features import extract_basic_features, extract_advanced_features

REF_FOLDER = "references"

def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
    return binary

def load_references():
    """Charge toutes les images de référence et extrait leurs features"""
    references = []
    for filename in os.listdir(REF_FOLDER):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            path = os.path.join(REF_FOLDER, filename)
            image = load_image(path)
            features = extract_basic_features(image)
            # features.update(extract_advanced_features(image))  # optionnel
            references.append({"name": filename, "features": features})
    return references

def compare_features(ref_features, input_features):
    """Calcule la distance Euclidienne entre features"""
    keys = ['width', 'height', 'black_pixels']
    distance = 0
    for k in keys:
        distance += (ref_features[k] - input_features[k]) ** 2
    return np.sqrt(distance)

def is_match(distance, threshold=1000):
    """Retourne True si distance < threshold"""
    return distance < threshold

def find_best_match(input_image, references, threshold=1000):
    """Compare input_image avec toutes les références et retourne la meilleure correspondance"""
    input_features = extract_basic_features(input_image)
    best_match = None
    min_distance = float('inf')

    for ref in references:
        dist = compare_features(ref["features"], input_features)
        if dist < min_distance:
            min_distance = dist
            best_match = ref

    match = is_match(min_distance, threshold)
    return best_match, min_distance, match

# --- TEST ---
if __name__ == "__main__":
    refs = load_references()
    input_image = load_image("bb.jpg")

    best_ref, distance, match = find_best_match(input_image, refs, threshold=1000)
    print(f"Meilleure correspondance: {best_ref['name']}")
    print(f"Distance: {distance:.2f}")
    print("Match?" , "Oui" if match else "Non")
