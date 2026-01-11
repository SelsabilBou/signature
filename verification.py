# verification.py
import logging

from preprocessing import preprocess_signature
from features import extract_features

logging.basicConfig(
    filename="verification.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def compute_distance(ref_features, test_features):
    dx = ref_features["width"]  - test_features["width"]
    dy = ref_features["height"] - test_features["height"]
    db = ref_features["black_pixels"] - test_features["black_pixels"]
    return (dx**2 + dy**2 + db**2) ** 0.5

def verify_signature(input_image_path, reference_path, threshold=1000.0):
    """
    Retourne (match: bool, message: str)
    """

    logging.info("Début vérification")
    logging.info(f"Image entrée   : {input_image_path}")
    logging.info(f"Image référence: {reference_path}")

    # 1) Prétraitement des deux images
    roi_in,  w_in,  h_in  = preprocess_signature(input_image_path)
    roi_ref, w_ref, h_ref = preprocess_signature(reference_path)

    if roi_in is None or roi_ref is None:
        logging.error("Prétraitement impossible (ROI None).")
        return False, "Erreur : impossible de prétraiter l'image."

    # 2) Image trop petite ?
    if w_in < 50 or h_in < 50:
        logging.warning("Image trop petite")
        return False, "Erreur : image trop petite pour une vérification fiable."

    # 3) Extraction des caractéristiques
    feat_input = extract_features(roi_in, w_in, h_in)
    feat_ref   = extract_features(roi_ref, w_ref, h_ref)

    logging.info(f"Features ref : {feat_ref}")
    logging.info(f"Features in  : {feat_input}")

    # 4) Distance + décision
    dist = compute_distance(feat_ref, feat_input)
    logging.info(f"Distance = {dist:.2f} (seuil = {threshold})")

    if dist <= threshold:
        msg = "✅ C'EST LA SIGNATURE DE SELSABIL !"
        logging.info("Résultat : MATCH")
        return True, msg
    else:
        msg = "❌ Signature non reconnue."
        logging.info("Résultat : NO MATCH")
        return False, msg


# petit test en ligne de commande
if __name__ == "__main__":
    ok, msg = verify_signature("image_test.png", "image_test.png")
    print(msg)
