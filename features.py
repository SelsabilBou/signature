# features.py

def extract_features(roi, width, height):
    """
    roi : image de la région d'intérêt (numpy array)
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
