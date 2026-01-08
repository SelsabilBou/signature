import numpy as np
from features import extract_basic_features, extract_advanced_features

image = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
])

basic = extract_basic_features(image)
advanced = extract_advanced_features(image)

print("Basic Features:")
print(basic)

print("\nAdvanced Features:")
print(advanced)
