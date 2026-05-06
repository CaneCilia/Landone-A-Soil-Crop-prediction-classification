import cv2
import numpy as np

SOIL_TYPE_RULES = [
    ("Sandy", lambda h, s, v: v > 170 and s < 100),
    ("Clay", lambda h, s, v: v < 95 and s > 90),
    ("Peaty", lambda h, s, v: v < 100 and s < 80),
    ("Silty", lambda h, s, v: 10 < h < 40 and s > 60),
]

BASE_SOIL_PROPERTIES = {
    "Sandy": {"texture": "Coarse", "organic_content": 18, "ph": 6.2},
    "Clay": {"texture": "Fine", "organic_content": 22, "ph": 6.6},
    "Loamy": {"texture": "Balanced", "organic_content": 28, "ph": 6.8},
    "Peaty": {"texture": "Soft", "organic_content": 34, "ph": 5.9},
    "Silty": {"texture": "Smooth", "organic_content": 24, "ph": 6.4},
}


def classify_soil(image: np.ndarray) -> tuple[str, float]:
    """Classify soil type using simple color heuristics over the input image."""
    blur = cv2.GaussianBlur(image, (7, 7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)
    avg_hue = float(np.mean(hsv[:, :, 0]))
    avg_sat = float(np.mean(hsv[:, :, 1]))
    avg_val = float(np.mean(hsv[:, :, 2]))

    for soil_type, rule in SOIL_TYPE_RULES:
        if rule(avg_hue, avg_sat, avg_val):
            return soil_type, 0.88

    return "Loamy", 0.84


def estimate_soil_properties(soil_type: str, humidity: float, temperature: float) -> dict:
    base = BASE_SOIL_PROPERTIES.get(soil_type, BASE_SOIL_PROPERTIES["Loamy"])
    moisture = min(100, max(10, humidity * 0.9 + (temperature - 20) * 0.5))
    organic_content = min(60, max(10, base["organic_content"] + (humidity - 50) * 0.12))
    ph = round(base["ph"] + (temperature - 22) * 0.01 - (humidity - 50) * 0.005, 1)

    return {
        "texture": base["texture"],
        "moisture": round(moisture, 1),
        "organic_content": round(organic_content, 1),
        "ph": ph,
    }
