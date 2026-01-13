import numpy as np


def extract_features(roi, width, height):
    """
    roi : image de la région d'intérêt (numpy array, 0 = noir, 255 = blanc)
    width, height : largeur et hauteur de la ROI
    Retourne un dictionnaire avec width, height, black_pixels.
    """
    if roi is None:
        return {"width": 0, "height": 0, "black_pixels": 0}

    # Pixels noirs = valeur 0
    black_pixels = int((roi == 0).sum())

    return {
        "width": int(width),
        "height": int(height),
        "black_pixels": black_pixels
    }


# --- Pour reference_db.py / test_features.py ---

def extract_basic_features(image):
    """
    Version simplifiée pour des images binaires complètes (0 = noir, 1 ou 255 = blanc).
    Calcule largeur, hauteur et nombre de pixels noirs.
    """
    if image is None:
        return {"width": 0, "height": 0, "black_pixels": 0}

    arr = np.array(image)
    if arr.ndim == 3:
        # si jamais image couleur, on prend un seul canal
        arr = arr[:, :, 0]

    h, w = arr.shape
    # On considère noir = 0
    black_pixels = int((arr == 0).sum())

    return {
        "width": int(w),
        "height": int(h),
        "black_pixels": black_pixels
    }


def extract_advanced_features(image):
    """
    Placeholder pour features avancées (longueur de tracé, courbure, etc.).
    Pour le moment, on retourne un dict vide pour rester compatible.
    """
    return {}
