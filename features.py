import numpy as np


def extract_features(roi, width: int, height: int):
    """
    roi : image de la région d'intérêt (numpy array, 0 = noir, 255 = blanc)
    width, height : largeur et hauteur de la ROI
    Retourne un dictionnaire avec width, height, black_pixels.
    """
    # On s'assure que width/height existent bien localement
    w = int(width)
    h = int(height)

    if roi is None:
        return {"width": 0, "height": 0, "black_pixels": 0}

    # Pixels noirs = valeur 0
    black_pixels = int(np.sum(roi == 0))

    return {
        "width": w,
        "height": h,
        "black_pixels": black_pixels,
    }


def extract_basic_features(image):
    """
    Version simplifiée pour des images binaires complètes (0 = noir, 1 ou 255 = blanc).
    Calcule largeur, hauteur et nombre de pixels noirs.
    Utilisé par reference_db.py / test_features.py.
    """
    if image is None:
        return {"width": 0, "height": 0, "black_pixels": 0}

    arr = np.array(image)
    if arr.ndim == 3:
        arr = arr[:, :, 0]

    h, w = arr.shape
    black_pixels = int(np.sum(arr == 0))

    return {
        "width": int(w),
        "height": int(h),
        "black_pixels": black_pixels,
    }


def extract_advanced_features(image):
    """
    Placeholder pour features avancées (tu peux compléter plus tard).
    """
    return {}
