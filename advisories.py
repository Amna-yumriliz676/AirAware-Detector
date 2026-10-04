"""
AirAware - Personalized health advisories
Rule-based engine. No ML, no API — just smart logic.
"""

# ============================================================
# USER PROFILE OPTIONS
# ============================================================
HEALTH_CONDITIONS = [
    "None (Healthy)",
    "Asthma",
    "Heart Disease",
    "Diabetes",
    "Allergies",
    "COPD",
    "Other Respiratory Issue"
]

ACTIVITY_LEVELS = [
    "Indoor (Home/Office)",
    "Student",
    "Outdoor Worker",
    "Jogger / Athlete",
    "Commuter"
]

AGE_GROUPS = [
    "Child (0-12)",
    "Teen (13-19)",
    "Adult (20-59)",
    "Senior (60+)"
]


# ============================================================
# ADVISORY ENGINE
# ============================================================
def get_advisory(aqi: int, condition: str, activity: str, age: str) -> dict:
    # Base risk from AQI
    if aqi <= 50:      risk = 0
    elif aqi <= 100:   risk = 1
    elif aqi <= 150:   risk = 2
    elif aqi <= 200:   risk = 3
    elif aqi <= 300:   risk = 4
    else:              risk = 5

    # Condition boost
    high_risk = ["Asthma", "Heart Disease", "COPD", "Other Respiratory Issue"]
    mid_risk  = ["Diabetes", "Allergies"]
    if condition in high_risk:   risk = min(risk + 2, 5)
    elif condition in mid_risk:  risk = min(risk + 1, 5)

    # Age boost
    if age in ["Child (0-12)", "Senior (60+)"]:
        risk = min(risk + 1, 5)

    # Activity boost
    if activity in ["Outdoor Worker", "Jogger / Athlete"]:
        risk = min(risk + 1, 5)

    # Risk level
    if risk >= 5:
        level, color, emoji = "EXTREME", "#7f1d1d", "🔴"
    elif risk >= 4:
        level, color, emoji = "VERY HIGH", "#dc2626", "🟥"
    elif risk >= 3:
        level, color, emoji = "HIGH", "#f97316", "🟠"
    elif risk >= 2:
        level, color, emoji = "MODERATE", "#f59e0b", "🟡"
    elif risk >= 1:
        level, color, emoji = "LOW", "#84cc16", "🟢"
    else:
        level, color, emoji = "MINIMAL", "#10b981", "✅"

    dos, donts = _actions(aqi, condition, activity, age)
    summary = _summary(aqi, level)

    return {
        "risk_score": risk,
        "risk_level": level,
        "risk_color": color,
        "risk_emoji": emoji,
        "dos": dos,
        "donts": donts,
        "summary": summary,
    }


def _actions(aqi, condition, activity, age):
    dos, donts = [], []

    # Universal
    if aqi <= 100:
        dos += ["Enjoy outdoor activities normally", "Keep windows open for ventilation"]
        donts += ["No restrictions for healthy individuals"]
    elif aqi <= 150:
        dos += ["Wear a mask if you have respiratory issues", "Limit prolonged outdoor exertion"]
        donts += ["Avoid outdoor exercise if you have asthma"]
    elif aqi <= 200:
        dos += ["Wear N95 mask outdoors", "Keep windows closed", "Use air purifier indoors"]
        donts += ["Avoid outdoor exercise", "Don't burn candles or incense indoors"]
    elif aqi <= 300:
        dos += ["Stay indoors as much as possible", "Wear N95 mask if going out",
                "Use air purifier continuously", "Drink plenty of water"]
        donts += ["No outdoor exercise", "Avoid cooking with gas", "Don't smoke indoors"]
    else:
        dos += ["DO NOT go outside unless emergency", "Seal windows and doors",
                "Run air purifier in a closed room",
                "Seek medical help if breathing difficulty"]
        donts += ["Absolutely no outdoor activity", "Don't open windows",
                  "Don't exercise indoors without purifier"]

    # Condition-specific
    if condition == "Asthma":
        dos.append("💊 Keep your inhaler within reach at all times")
        dos.append("📞 Have emergency contact ready")
        if aqi > 150:
            donts.append("❌ Don't skip your preventive medication")
    elif condition == "Heart Disease":
        dos.append("❤️ Monitor blood pressure regularly")
        if aqi > 150:
            donts.append("❌ Avoid strenuous activity even indoors")
    elif condition == "COPD":
        dos.append("🫁 Use prescribed oxygen if advised")
        if aqi > 150:
            donts.append("❌ Avoid going outdoors completely")
    elif condition == "Diabetes":
        dos.append("🩸 Monitor blood sugar — pollution affects it")
    elif condition == "Allergies":
        dos.append("🤧 Take antihistamine if prescribed")
        donts.append("❌ Avoid areas with smoke or dust")

    # Age-specific
    if age == "Child (0-12)":
        dos.append("👶 Keep children indoors during high AQI")
        if aqi > 150:
            donts.append("❌ Don't send children to outdoor play")
    elif age == "Senior (60+)":
        dos.append("👴 Seniors should limit outdoor exposure")
        if aqi > 150:
            donts.append("❌ Avoid morning walks on high AQI days")

    # Activity-specific
    if activity == "Outdoor Worker":
        dos.append("🦺 Wear N95 mask during work hours")
        dos.append("🚰 Take frequent water breaks")
        if aqi > 200:
            donts.append("❌ Request indoor work if possible")
    elif activity == "Jogger / Athlete":
        dos.append("🏃 Move workout indoors to gym")
        if aqi > 150:
            donts.append("❌ Don't jog outdoors on high AQI days")
    elif activity == "Commuter":
        dos.append("🚗 Use AC with recirculation mode in car")
        dos.append("😷 Wear mask on public transport")

    return dos, donts


def _summary(aqi, level):
    if level in ["EXTREME", "VERY HIGH"]:
        return f"⚠️ AQI {aqi} is DANGEROUS for you. Stay indoors."
    if level == "HIGH":
        return f"🚨 AQI {aqi} is unhealthy. Take precautions below."
    if level == "MODERATE":
        return f"⚠️ AQI {aqi} may affect you. Follow recommendations."
    if level == "LOW":
        return f"✅ AQI {aqi} is acceptable. Minor precautions recommended."
    return f"🎉 AQI {aqi} is good. Enjoy outdoor activities!"


def get_health_tips(aqi: int) -> list:
    if aqi <= 50:
        return ["Great day for outdoor activities",
                "Open windows for fresh air",
                "Perfect for a walk or jog"]
    if aqi <= 100:
        return ["Acceptable air quality",
                "Sensitive individuals should monitor",
                "Moderate outdoor activity is fine"]
    if aqi <= 150:
        return ["Sensitive groups limit outdoor time",
                "Consider wearing a mask",
                "Keep windows partially closed"]
    if aqi <= 200:
        return ["Wear N95 mask outdoors",
                "Avoid prolonged outdoor exposure",
                "Use air purifier indoors"]
    if aqi <= 300:
        return ["Stay indoors",
                "Use air purifier continuously",
                "Wear N95 if you must go out"]
    return ["EMERGENCY — Do not go outside",
            "Seal windows and doors",
            "Seek medical help if symptoms occur"]


def get_mask_recommendation(aqi: int) -> str:
    if aqi <= 50:   return "No mask needed 😊"
    if aqi <= 100:  return "Optional: Surgical mask"
    if aqi <= 150:  return "Recommended: Surgical mask"
    if aqi <= 200:  return "Strongly Recommended: N95 mask"
    if aqi <= 300:  return "Required: N95 or N99 mask"
    return "🚨 Required: N95/N99 + Eye protection"
