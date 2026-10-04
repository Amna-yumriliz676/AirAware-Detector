"""
AirAware - Built-in data
No API key required. All data is simulated with realistic patterns.
"""

import random
from datetime import datetime


# ============================================================
# CITIES WITH BASE POLLUTION PROFILES
# ============================================================
CITIES = {
    "Lahore":     {"lat": 31.5204, "lng": 74.3587, "country": "Pakistan",  "base_aqi": 280},
    "Karachi":    {"lat": 24.8607, "lng": 67.0011, "country": "Pakistan",  "base_aqi": 165},
    "Islamabad":  {"lat": 33.6844, "lng": 73.0479, "country": "Pakistan",  "base_aqi": 120},
    "Rawalpindi": {"lat": 33.5651, "lng": 73.0169, "country": "Pakistan",  "base_aqi": 145},
    "Faisalabad": {"lat": 31.4180, "lng": 73.0790, "country": "Pakistan",  "base_aqi": 210},
    "Multan":     {"lat": 30.1575, "lng": 71.5249, "country": "Pakistan",  "base_aqi": 195},
    "Peshawar":   {"lat": 34.0151, "lng": 71.5249, "country": "Pakistan",  "base_aqi": 175},
    "Quetta":     {"lat": 30.1798, "lng": 66.9750, "country": "Pakistan",  "base_aqi": 130},
    "Delhi":      {"lat": 28.6139, "lng": 77.2090, "country": "India",     "base_aqi": 310},
    "Mumbai":     {"lat": 19.0760, "lng": 72.8777, "country": "India",     "base_aqi": 155},
    "Dhaka":      {"lat": 23.8103, "lng": 90.4125, "country": "Bangladesh","base_aqi": 260},
    "Beijing":    {"lat": 39.9042, "lng": 116.4074, "country": "China",    "base_aqi": 140},
}


# ============================================================
# AQI CATEGORY
# ============================================================
def get_aqi_category(aqi: int) -> dict:
    if aqi <= 50:
        return {"label": "Good", "color": "#10b981", "emoji": "🟢",
                "advice": "Air quality is satisfactory."}
    elif aqi <= 100:
        return {"label": "Moderate", "color": "#f59e0b", "emoji": "🟡",
                "advice": "Acceptable for most people."}
    elif aqi <= 150:
        return {"label": "Unhealthy for Sensitive", "color": "#f97316", "emoji": "🟠",
                "advice": "Sensitive groups should limit outdoor time."}
    elif aqi <= 200:
        return {"label": "Unhealthy", "color": "#ef4444", "emoji": "🔴",
                "advice": "Everyone may experience health effects."}
    elif aqi <= 300:
        return {"label": "Very Unhealthy", "color": "#a855f7", "emoji": "🟣",
                "advice": "Health alert: serious effects possible."}
    else:
        return {"label": "Hazardous", "color": "#7f1d1d", "emoji": "⚫",
                "advice": "Emergency conditions. Stay indoors."}


# ============================================================
# SIMULATED AQI GENERATOR (No API)
# ============================================================
def generate_aqi(city_name: str) -> dict:
    """
    Generate realistic AQI data for a city.
    Uses deterministic seed so data is stable within the same hour.
    """
    city_info = CITIES.get(city_name)
    if not city_info:
        return None

    hour = datetime.now().hour
    day = datetime.now().day
    # Stable seed per city + hour
    random.seed(hash(f"{city_name}_{day}_{hour}") % 100000)

    base = city_info["base_aqi"]

    # Time-of-day factor
    if 6 <= hour <= 9 or 17 <= hour <= 20:
        time_factor = 1.15  # rush hour
    elif 10 <= hour <= 16:
        time_factor = 0.90  # afternoon better
    else:
        time_factor = 1.05  # night

    variation = random.uniform(0.85, 1.15)
    aqi = int(base * time_factor * variation)
    aqi = max(20, min(aqi, 500))

    # Pollutants derived from AQI
    pm25 = max(round(aqi * 0.75 + random.uniform(-10, 10), 1), 5)
    pm10 = max(round(aqi * 0.95 + random.uniform(-15, 15), 1), 10)
    o3 = random.randint(20, 90)
    no2 = random.randint(15, 70)
    so2 = random.randint(5, 35)
    co = round(random.uniform(0.4, 3.5), 2)
    temp = random.randint(12, 38)
    humidity = random.randint(35, 85)
    wind = round(random.uniform(0.5, 8.0), 1)

    return {
        "city": city_name,
        "country": city_info["country"],
        "aqi": aqi,
        "pm25": pm25,
        "pm10": pm10,
        "o3": o3,
        "no2": no2,
        "so2": so2,
        "co": co,
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "dominant": "pm25",
        "station": f"{city_name} - Central Monitoring",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "lat": city_info["lat"],
        "lng": city_info["lng"],
        "source": "Simulated Data",
        "success": True,
    }


def get_all_cities_data():
    """Return AQI data for all cities."""
    results = []
    for city in CITIES.keys():
        data = generate_aqi(city)
        if data:
            results.append(data)
    return results


def get_aqi_color(aqi: int) -> str:
    if aqi <= 50:   return "#10b981"
    if aqi <= 100:  return "#f59e0b"
    if aqi <= 150:  return "#f97316"
    if aqi <= 200:  return "#ef4444"
    if aqi <= 300:  return "#a855f7"
    return "#7f1d1d"


def get_aqi_emoji(aqi: int) -> str:
    if aqi <= 50:   return "🟢"
    if aqi <= 100:  return "🟡"
    if aqi <= 150:  return "🟠"
    if aqi <= 200:  return "🔴"
    if aqi <= 300:  return "🟣"
    return "⚫"
