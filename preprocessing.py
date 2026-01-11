# preprocessing.py
import cv2
import numpy as np
from PIL import Image


# -------- Phase 1 : bruit + niveaux de gris --------

def remove_noise(image):
    """Applique un filtre médian pour enlever le bruit."""
    # kernel 3x3 (doit être impair)
    denoised = cv2.medianBlur(image, 3)
    return denoised


def convert_to_grayscale(image):
    """Convertit en niveau de gris si nécessaire."""
    if len(image.shape) == 3:  # image couleur BGR
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    return gray


# -------- Phase 2 : binarisation + squelettisation --------

def binarize_image(gray):
    """
    Binarisation adaptative : image binaire
    signature noire (0), fond blanc (255).
    """
    bw = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Si l'image est trop sombre on inverse pour avoir la signature noire
    if np.mean(bw) < 127:
        bw = 255 - bw

    return bw


def skeletonize_image(binary):
    """
    Squelettisation (amincissement) pour obtenir des traits de 1 pixel.
    Utilise cv2.ximgproc.thinning si disponible, sinon une version simple.
    """
    # On suppose binaire 0/255, on convertit en 0/1
    bin01 = (binary == 0).astype(np.uint8) * 255

    try:
        # OpenCV contrib: ximgproc.thinning
        import cv2.ximgproc as ximgproc
        skel = ximgproc.thinning(bin01)
    except Exception:
        # Version morphologique simple (moins parfaite mais suffisante)
        img = bin01.copy()
        skel = np.zeros_like(img)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        while True:
            eroded = cv2.erode(img, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()

            if cv2.countNonZero(img) == 0:
                break

    # On revient à 0 = noir, 255 = blanc
    skel = (skel == 0).astype(np.uint8) * 255
    return skel


# -------- Phase 3 : ROI --------

def compute_roi(image):
    """
    Trouve la bounding-box de la signature (pixels noirs)
    et retourne (roi, width, height).
    """
    # signature = noir = 0
    mask = (image == 0)

    if not np.any(mask):
        return None, 0, 0

    ys, xs = np.where(mask)
    min_x, max_x = xs.min(), xs.max()
    min_y, max_y = ys.min(), ys.max()

    roi = image[min_y:max_y + 1, min_x:max_x + 1]
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    return roi, int(width), int(height)


# -------- Phase 4 : utilitaires + pipeline complet --------

def save_processed_image(image, filename):
    """Sauvegarde une image NumPy en PNG avec PIL."""
    if image is None:
        return
    img_pil = Image.fromarray(image)
    img_pil.save(filename)


def preprocess_pipeline(path):
    """
    Pipeline complet du module 2.
    Retourne (roi, width, height) ou (None, 0, 0) en cas d'erreur.
    """
    # Charger l'image
    img = cv2.imread(path)
    if img is None:
        print("Erreur : image introuvable ->", path)
        return None, 0, 0

    # Phase 1
    denoised = remove_noise(img)
    gray = convert_to_grayscale(denoised)

    # Phase 2
    binary = binarize_image(gray)
    skeleton = skeletonize_image(binary)

    # Phase 3
    roi, w, h = compute_roi(skeleton)
    if roi is None or w == 0 or h == 0:
        print("Erreur : ROI vide après traitement.")
        return None, 0, 0

    # Phase 4 : sauvegarde optionnelle pour debug
    save_processed_image(denoised, "step1_denoised.png")
    save_processed_image(gray, "step2_gray.png")
    save_processed_image(binary, "step3_binary.png")
    save_processed_image(skeleton, "step4_skeleton.png")
    save_processed_image(roi, "step5_roi.png")

    return roi, w, h


# -------- Test rapide du module 2 --------

if __name__ == "__main__":
    roi, w, h = preprocess_pipeline("image_test.png")
    print("ROI width :", w)
    print("ROI height:", h)
