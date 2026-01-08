import numpy as np
import cv2

def extract_basic_features(image):
    features = {}

    black_pixels = np.sum(image > 0)

    if black_pixels == 0:
        features['width'] = 0
        features['height'] = 0
        features['black_pixels'] = 0
        return features

    ys, xs = np.where(image > 0)

    features['width'] = xs.max() - xs.min() + 1
    features['height'] = ys.max() - ys.min() + 1
    features['black_pixels'] = black_pixels

    return features


def extract_advanced_features(image):
    """
    image : binary image (numpy array)
    return : dictionary of advanced features
    """

    features = {}

    # OpenCV يخدم ب uint8
    img_uint8 = image.astype(np.uint8) * 255

    # إيجاد contours
    contours, _ = cv2.findContours(
        img_uint8,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    total_stroke_length = 0.0

    for contour in contours:
        total_stroke_length += cv2.arcLength(contour, True)

    features['stroke_length'] = total_stroke_length

    return features
