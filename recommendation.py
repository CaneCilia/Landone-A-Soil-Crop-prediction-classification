CROP_PROFILE = {
    "Sandy": [
        {"crop": "Millet", "base_score": 85, "ideal_temp": (20, 35), "ideal_humidity": (20, 50)},
        {"crop": "Groundnut", "base_score": 78, "ideal_temp": (22, 32), "ideal_humidity": (40, 60)},
        {"crop": "Cotton", "base_score": 72, "ideal_temp": (24, 33), "ideal_humidity": (35, 55)},
    ],
    "Clay": [
        {"crop": "Rice", "base_score": 88, "ideal_temp": (20, 30), "ideal_humidity": (60, 90)},
        {"crop": "Sugarcane", "base_score": 80, "ideal_temp": (21, 32), "ideal_humidity": (65, 90)},
        {"crop": "Soybean", "base_score": 75, "ideal_temp": (18, 30), "ideal_humidity": (50, 70)},
    ],
    "Loamy": [
        {"crop": "Wheat", "base_score": 90, "ideal_temp": (10, 25), "ideal_humidity": (40, 60)},
        {"crop": "Maize", "base_score": 86, "ideal_temp": (18, 32), "ideal_humidity": (45, 65)},
        {"crop": "Tomato", "base_score": 80, "ideal_temp": (18, 27), "ideal_humidity": (50, 70)},
    ],
    "Peaty": [
        {"crop": "Potato", "base_score": 82, "ideal_temp": (15, 22), "ideal_humidity": (55, 75)},
        {"crop": "Tobacco", "base_score": 78, "ideal_temp": (15, 28), "ideal_humidity": (55, 75)},
        {"crop": "Vegetables", "base_score": 84, "ideal_temp": (14, 26), "ideal_humidity": (50, 78)},
    ],
    "Silty": [
        {"crop": "Barley", "base_score": 80, "ideal_temp": (10, 24), "ideal_humidity": (40, 65)},
        {"crop": "Sugar Beet", "base_score": 76, "ideal_temp": (15, 25), "ideal_humidity": (45, 70)},
        {"crop": "Sunflower", "base_score": 74, "ideal_temp": (20, 30), "ideal_humidity": (35, 60)},
    ],
}


def score_crop(crop_profile: dict, humidity: float, temperature: float, land_size: float) -> int:
    score = crop_profile["base_score"]
    low_t, high_t = crop_profile["ideal_temp"]
    low_h, high_h = crop_profile["ideal_humidity"]

    if low_t <= temperature <= high_t:
        score += 8
    else:
        score -= int(abs(temperature - (low_t + high_t) / 2) * 1.2)

    if low_h <= humidity <= high_h:
        score += 6
    else:
        score -= int(abs(humidity - (low_h + high_h) / 2) * 0.8)

    if land_size >= 0.5:
        score += 2
    if land_size < 0.3:
        score -= 4

    return max(0, min(100, score))


def generate_recommendations(soil_type: str, properties: dict, humidity: float, temperature: float, land_size: float) -> list:
    candidates = CROP_PROFILE.get(soil_type, CROP_PROFILE["Loamy"])
    recommendations = []

    for profile in candidates:
        score = score_crop(profile, humidity, temperature, land_size)
        reason_parts = [f"base suitability for {soil_type.lower()} soil"]

        if profile["ideal_temp"][0] <= temperature <= profile["ideal_temp"][1]:
            reason_parts.append("temperature is within the ideal range")
        else:
            reason_parts.append("temperature is slightly outside the ideal range")

        if profile["ideal_humidity"][0] <= humidity <= profile["ideal_humidity"][1]:
            reason_parts.append("humidity is supportive")
        else:
            reason_parts.append("humidity may require extra irrigation or drainage")

        if score >= 70:
            reason_parts.append("suitable for the current land area")

        recommendations.append(
            {
                "crop": profile["crop"],
                "score": score,
                "reason": ", ".join(reason_parts).capitalize() + "."
            }
        )

    return sorted(recommendations, key=lambda item: item["score"], reverse=True)
