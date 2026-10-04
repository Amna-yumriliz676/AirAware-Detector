"""
AirAware — Air Quality Alert System
Real-time AQI + Smart Alerts + Personalized Health Advice + Pollution Map
No API key required — all data is realistic simulated.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from data import (
    CITIES, get_aqi_category, generate_aqi,
    get_all_cities_data, get_aqi_color, get_aqi_emoji
)
from advisories import (
    HEALTH_CONDITIONS, ACTIVITY_LEVELS, AGE_GROUPS,
    get_advisory, get_health_tips, get_mask_recommendation
)


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AirAware",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    .stApp { background: #f7f8fc; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f172a;
        min-width: 280px !important;
        max-width: 280px !important;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] .stRadio > label { display: none; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 4px; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background: transparent; padding: 10px 16px; border-radius: 10px;
        cursor: pointer; transition: all 0.2s; font-weight: 500;
        font-size: 0.88rem; width: 100%; border: none;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, #0ea5e9, #06b6d4) !important;
        box-shadow: 0 4px 12px rgba(14,165,233,0.35);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio input[type="radio"] { display: none; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* Brand */
    .brand { display: flex; align-items: center; gap: 0.7rem;
        padding: 1rem 0.5rem 1.5rem 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 1rem; }
    .brand-logo { width: 42px; height: 42px;
        background: linear-gradient(135deg, #0ea5e9, #06b6d4);
        border-radius: 12px; display: flex; align-items: center;
        justify-content: center; font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(14,165,233,0.4); }
    .brand-name { font-weight: 800; font-size: 1.1rem; color: #ffffff !important; }
    .brand-sub { font-size: 0.68rem; color: #0ea5e9 !important;
        font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

    /* Page header */
    .page-header { margin-bottom: 1.5rem; }
    .page-title { font-size: 1.7rem; font-weight: 800; color: #0f172a;
        letter-spacing: -0.6px; margin: 0; }
    .page-sub { font-size: 0.88rem; color: #64748b; margin-top: 0.3rem; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        padding: 1.8rem 2rem; border-radius: 18px; color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px -15px rgba(14,165,233,0.4);
        position: relative; overflow: hidden;
    }
    .hero::before { content: ""; position: absolute; top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.15), transparent 70%);
        border-radius: 50%; }
    .hero h1 { font-size: 1.8rem; font-weight: 800; margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px; position: relative; }
    .hero p { font-size: 0.95rem; opacity: 0.95; margin: 0; position: relative; }

    /* AQI hero */
    .aqi-hero {
        background: white; border-radius: 20px; padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px -10px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    .aqi-value {
        font-size: 5rem; font-weight: 800; line-height: 1;
        letter-spacing: -3px; margin: 0.5rem 0;
    }
    .aqi-label {
        display: inline-block; padding: 6px 16px; border-radius: 50px;
        font-size: 0.85rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1px; color: white;
    }
    .aqi-location { font-size: 1.1rem; color: #64748b;
        font-weight: 600; margin-bottom: 0.5rem; }
    .aqi-time { font-size: 0.78rem; color: #94a3b8; margin-top: 0.8rem; }

    /* Cards */
    .card { background: white; border: 1px solid #e2e8f0;
        border-radius: 14px; padding: 1.2rem 1.3rem;
        margin-bottom: 1rem; transition: all 0.2s; }
    .card:hover { box-shadow: 0 8px 20px -10px rgba(0,0,0,0.1);
        border-color: #cbd5e1; }

    /* KPI */
    .kpi-card { background: white; padding: 1.1rem 1.2rem;
        border-radius: 14px; border: 1px solid #eef0f4;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03); height: 100%; }
    .kpi-icon { width: 38px; height: 38px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; margin-bottom: 0.7rem; }
    .kpi-icon.blue { background: #dbeafe; }
    .kpi-icon.green { background: #d1fae5; }
    .kpi-icon.orange { background: #ffedd5; }
    .kpi-icon.red { background: #fee2e2; }
    .kpi-icon.purple { background: #f3e8ff; }
    .kpi-label { font-size: 0.72rem; color: #64748b;
        font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.5px; margin-bottom: 0.3rem; }
    .kpi-value { font-size: 1.5rem; font-weight: 800;
        color: #0f172a; line-height: 1.1; }

    /* Risk badge */
    .risk-badge { display: inline-block; padding: 8px 20px;
        border-radius: 50px; font-weight: 700; font-size: 0.9rem;
        color: white; text-transform: uppercase; letter-spacing: 1px; }

    /* Advice list */
    .advice-list { list-style: none; padding: 0; margin: 0; }
    .advice-list li { padding: 0.6rem 0;
        border-bottom: 1px solid #f1f5f9; font-size: 0.92rem;
        color: #334155; display: flex; align-items: flex-start; gap: 0.6rem; }
    .advice-list li:last-child { border-bottom: none; }

    /* Pollutant rows */
    .pollutant-row { display: flex; justify-content: space-between;
        align-items: center; padding: 0.7rem 0;
        border-bottom: 1px solid #f1f5f9; }
    .pollutant-row:last-child { border-bottom: none; }
    .pollutant-name { font-weight: 600; color: #334155; font-size: 0.88rem; }
    .pollutant-value { font-weight: 700; color: #0f172a; font-size: 0.92rem; }

    /* Buttons */
    .stButton > button {
        border-radius: 10px; font-weight: 600; font-size: 0.85rem;
        padding: 0.5rem 1.1rem; transition: all 0.2s;
        border: 1px solid #e2e8f0; background: white; color: #334155;
    }
    .stButton > button:hover { border-color: #a5f3fc;
        color: #0ea5e9; transform: translateY(-1px); }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9, #06b6d4);
        border: none; color: white;
        box-shadow: 0 4px 12px -4px rgba(14,165,233,0.5);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 20px -6px rgba(14,165,233,0.6); color: white; }

    /* Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #e2e8f0 !important;
        font-size: 0.88rem !important;
    }

    /* Sidebar metrics */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04); padding: 0.7rem 0.9rem;
        border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.5rem; }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] * {
        color: #94a3b8 !important; font-size: 0.75rem !important; }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] * {
        color: #ffffff !important; font-size: 1.2rem !important;
        font-weight: 700 !important; }

    /* Responsive */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        .aqi-value { font-size: 3.5rem; }
        .hero h1 { font-size: 1.4rem; }
        .page-title { font-size: 1.3rem; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
if "selected_city" not in st.session_state:
    st.session_state.selected_city = "Lahore"
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "condition": "None (Healthy)",
        "activity": "Indoor (Home/Office)",
        "age": "Adult (20-59)"
    }
if "alert_threshold" not in st.session_state:
    st.session_state.alert_threshold = 150


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-logo">🌫️</div>
        <div>
            <div class="brand-name">AirAware</div>
            <div class="brand-sub">Air Quality Alert</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "👤  My Health Profile",
            "🗺️  Pollution Map",
            "📊  Compare Cities",
            "ℹ️  About"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📍 City")
    selected_city = st.selectbox(
        "Select city",
        list(CITIES.keys()),
        index=list(CITIES.keys()).index(st.session_state.selected_city),
        label_visibility="collapsed"
    )
    st.session_state.selected_city = selected_city

    st.markdown("<br>")
    st.markdown("### 🔔 Alert Threshold")
    st.session_state.alert_threshold = st.slider(
        "Alert me when AQI exceeds:",
        min_value=50, max_value=400,
        value=st.session_state.alert_threshold,
        step=10,
        label_visibility="collapsed"
    )

    st.markdown("<br>")
    st.caption("🌫️ Simulated AQI Data")
    st.caption("⚠️ Educational purposes only")


# ============================================================
# GET DATA
# ============================================================
current_data = generate_aqi(st.session_state.selected_city)


# ============================================================
# PAGE: DASHBOARD
# ============================================================
if page == "🏠  Dashboard":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🏠 Air Quality Dashboard</h1>
        <div class="page-sub">Real-time AQI with personalized health advice</div>
    </div>
    """, unsafe_allow_html=True)

    aqi = current_data["aqi"]
    category = get_aqi_category(aqi)
    profile = st.session_state.user_profile

    # AQI Hero + Risk card
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(f"""
        <div class="aqi-hero">
            <div class="aqi-location">📍 {current_data['city']}, {current_data['country']}</div>
            <div class="aqi-value" style="color:{category['color']};">{aqi}</div>
            <div style="margin-top:0.5rem;">
                <span class="aqi-label" style="background:{category['color']};">
                    {category['emoji']} {category['label']}
                </span>
            </div>
            <div class="aqi-time">
                🕐 Updated: {current_data['time']} · Source: {current_data['source']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if aqi >= st.session_state.alert_threshold:
            st.error(f"🚨 **ALERT:** AQI ({aqi}) has exceeded your threshold ({st.session_state.alert_threshold})")

    with col2:
        advisory = get_advisory(aqi, profile["condition"], profile["activity"], profile["age"])
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.72rem; color:#64748b; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
                Your Personal Risk
            </div>
            <div style="margin:0.6rem 0;">
                <span class="risk-badge" style="background:{advisory['risk_color']};">
                    {advisory['risk_emoji']} {advisory['risk_level']}
                </span>
            </div>
            <div style="font-size:0.9rem; color:#334155; line-height:1.5;">
                {advisory['summary']}
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.8rem;">
                Based on: {profile['condition']} · {profile['activity']} · {profile['age']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Pollutants + Weather
    col3, col4 = st.columns([1, 1], gap="large")

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🧪 Pollutants Breakdown")

        pollutants = [
            ("PM2.5", current_data.get("pm25"), "µg/m³", "Fine particles"),
            ("PM10", current_data.get("pm10"), "µg/m³", "Coarse particles"),
            ("O₃", current_data.get("o3"), "ppb", "Ozone"),
            ("NO₂", current_data.get("no2"), "ppb", "Nitrogen dioxide"),
            ("SO₂", current_data.get("so2"), "ppb", "Sulfur dioxide"),
            ("CO", current_data.get("co"), "ppm", "Carbon monoxide"),
        ]

        rows_html = ""
        for name, value, unit, desc in pollutants:
            val_str = f"{value} {unit}" if value is not None else "N/A"
            rows_html += f"""
            <div class="pollutant-row">
                <div>
                    <div class="pollutant-name">{name}</div>
                    <div style="font-size:0.7rem; color:#94a3b8;">{desc}</div>
                </div>
                <div class="pollutant-value">{val_str}</div>
            </div>
            """
        st.markdown(rows_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🌡️ Weather & Environment")

        weather_rows = [
            ("🌡️ Temperature", f"{current_data.get('temp', 'N/A')}°C"),
            ("💧 Humidity", f"{current_data.get('humidity', 'N/A')}%"),
            ("💨 Wind Speed", f"{current_data.get('wind', 'N/A')} m/s"),
            ("🎯 Dominant Pollutant", str(current_data.get("dominant", "N/A")).upper()),
            ("📡 Station", current_data.get("station", "N/A")),
        ]

        weather_html = ""
        for label, value in weather_rows:
            weather_html += f"""
            <div class="pollutant-row">
                <div class="pollutant-name">{label}</div>
                <div class="pollutant-value">{value}</div>
            </div>
            """
        st.markdown(weather_html, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:1rem; padding:1rem; background:#f0fdfa; border-radius:10px; border:1px solid #a7f3d0;">
            <div style="font-size:0.72rem; color:#047857; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
                😷 Mask Recommendation
            </div>
            <div style="font-size:1rem; color:#064e3b; font-weight:700; margin-top:0.3rem;">
                {get_mask_recommendation(aqi)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Do's and Don'ts
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 💡 Personalized Advice for You")

    adv_col1, adv_col2 = st.columns(2)

    with adv_col1:
        st.markdown("##### ✅ Do's")
        dos_html = "<ul class='advice-list'>"
        for item in advisory["dos"]:
            dos_html += f"<li>{item}</li>"
        dos_html += "</ul>"
        st.markdown(dos_html, unsafe_allow_html=True)

    with adv_col2:
        st.markdown("##### ❌ Don'ts")
        donts_html = "<ul class='advice-list'>"
        for item in advisory["donts"]:
            donts_html += f"<li>{item}</li>"
        donts_html += "</ul>"
        st.markdown(donts_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # General tips
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🌿 General Health Tips")
    tips = get_health_tips(aqi)
    tip_cols = st.columns(len(tips))
    for i, tip in enumerate(tips):
        with tip_cols[i]:
            st.info(tip)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: MY HEALTH PROFILE
# ============================================================
elif page == "👤  My Health Profile":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">👤 My Health Profile</h1>
        <div class="page-sub">Personalize your advisories — set your profile once</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 Set your health profile to get personalized advice on the Dashboard.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🩺 Your Information")

        p = st.session_state.user_profile

        condition = st.selectbox(
            "Health Condition",
            HEALTH_CONDITIONS,
            index=HEALTH_CONDITIONS.index(p["condition"])
        )
        activity = st.selectbox(
            "Activity Level",
            ACTIVITY_LEVELS,
            index=ACTIVITY_LEVELS.index(p["activity"])
        )
        age = st.selectbox(
            "Age Group",
            AGE_GROUPS,
            index=AGE_GROUPS.index(p["age"])
        )

        if st.button("💾  Save Profile", type="primary", use_container_width=True):
            st.session_state.user_profile = {
                "condition": condition,
                "activity": activity,
                "age": age
            }
            st.success("✅ Profile saved! Go to Dashboard to see personalized advice.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Current Profile")

        p = st.session_state.user_profile
        st.markdown(f"""
        <div class="pollutant-row">
            <div class="pollutant-name">🩺 Health Condition</div>
            <div class="pollutant-value">{p['condition']}</div>
        </div>
        <div class="pollutant-row">
            <div class="pollutant-name">🏃 Activity Level</div>
            <div class="pollutant-value">{p['activity']}</div>
        </div>
        <div class="pollutant-row">
            <div class="pollutant-name">👤 Age Group</div>
            <div class="pollutant-value">{p['age']}</div>
        </div>
        """, unsafe_allow_html=True)

        aqi = current_data["aqi"]
        advisory = get_advisory(aqi, p["condition"], p["activity"], p["age"])
        st.markdown(f"""
        <div style="margin-top:1rem; padding:1rem; border-radius:10px;
             background:{advisory['risk_color']}15; border:1px solid {advisory['risk_color']}40;">
            <div style="font-size:0.72rem; color:{advisory['risk_color']};
                 font-weight:700; text-transform:uppercase;">
                Current Risk
            </div>
            <div style="font-size:1.5rem; font-weight:800;
                 color:{advisory['risk_color']}; margin-top:0.3rem;">
                {advisory['risk_emoji']} {advisory['risk_level']}
            </div>
            <div style="font-size:0.85rem; color:#334155; margin-top:0.3rem;">
                {advisory['summary']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: POLLUTION MAP
# ============================================================
elif page == "🗺️  Pollution Map":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🗺️ Pollution Map</h1>
        <div class="page-sub">Live AQI across 12+ major cities</div>
    </div>
    """, unsafe_allow_html=True)

    all_cities = get_all_cities_data()
    df = pd.DataFrame(all_cities)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon red">🚨</div>
            <div class="kpi-label">Hazardous</div>
            <div class="kpi-value">{len(df[df['aqi'] > 300])}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon orange">⚠️</div>
            <div class="kpi-label">Unhealthy</div>
            <div class="kpi-value">{len(df[(df['aqi'] > 150) & (df['aqi'] <= 300)])}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon green">✅</div>
            <div class="kpi-label">Safe Cities</div>
            <div class="kpi-value">{len(df[df['aqi'] <= 100])}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon blue">📊</div>
            <div class="kpi-label">Average AQI</div>
            <div class="kpi-value">{int(df['aqi'].mean())}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Map
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🗺️ Live AQI Map")
    map_df = df[["lat", "lng"]].rename(columns={"lat": "lat", "lng": "lon"})
    st.map(map_df, zoom=4, use_container_width=True, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

    # Ranking
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📊 City Rankings (Worst → Best)")

    df_sorted = df.sort_values("aqi", ascending=False).reset_index(drop=True)
    rows_html = ""
    for _, row in df_sorted.iterrows():
        cat = get_aqi_category(row["aqi"])
        rows_html += f"""
        <div class="pollutant-row">
            <div class="pollutant-name">{cat['emoji']} <b>{row['city']}</b> <span style="color:#94a3b8; font-weight:400; font-size:0.8rem;">({row['country']})</span></div>
            <div style="display:flex; gap:0.5rem; align-items:center;">
                <span style="font-weight:800; color:{cat['color']}; font-size:1.1rem;">{row['aqi']}</span>
                <span style="font-size:0.72rem; color:{cat['color']}; background:{cat['color']}20;
                     padding:3px 10px; border-radius:50px; font-weight:700;">
                    {cat['label']}
                </span>
            </div>
        </div>
        """
    st.markdown(rows_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: COMPARE CITIES
# ============================================================
elif page == "📊  Compare Cities":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📊 Compare Cities</h1>
        <div class="page-sub">AQI comparison across cities</div>
    </div>
    """, unsafe_allow_html=True)

    all_data = get_all_cities_data()
    df = pd.DataFrame(all_data)
    df_sorted = df.sort_values("aqi", ascending=False)

    # Bar chart
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📊 AQI Comparison")

    colors = [get_aqi_color(aqi) for aqi in df_sorted["aqi"]]
    fig = go.Figure(data=[
        go.Bar(
            x=df_sorted["city"],
            y=df_sorted["aqi"],
            marker_color=colors,
            text=df_sorted["aqi"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>AQI: %{y}<extra></extra>"
        )
    ])
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color="#334155"),
        yaxis_title="AQI",
        xaxis_title="",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Pollutant comparison
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🧪 Pollutant Comparison")

    pollutants = ["pm25", "pm10", "o3", "no2", "so2"]
    p_df = df_sorted[["city"] + pollutants].copy()
    for p in pollutants:
        p_df[p] = pd.to_numeric(p_df[p], errors="coerce")

    fig2 = go.Figure()
    for p in pollutants:
        fig2.add_trace(go.Bar(
            name=p.upper(),
            x=p_df["city"],
            y=p_df[p],
        ))
    fig2.update_layout(
        barmode="group",
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color="#334155"),
        yaxis_title="Concentration",
        legend=dict(orientation="h", y=1.1, x=0)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📋 View Raw Data"):
        st.dataframe(df_sorted, use_container_width=True, hide_index=True)


# ============================================================
# PAGE: ABOUT
# ============================================================
elif page == "ℹ️  About":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">ℹ️ About AirAware</h1>
        <div class="page-sub">Your personal air quality guardian</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🌫️ What is AirAware?

    AirAware is an air quality alert system that helps you:
    - **Monitor** real-time AQI in your city
    - **Understand** pollution levels with easy visuals
    - **Get personalized** health advice based on your profile
    - **Compare** air quality across cities
    - **Protect** yourself and your family

    ### 🎯 Why It Matters

    - **Lahore** has been ranked among the world's most polluted cities
    - Air pollution causes **7+ million deaths** globally every year
    - **Asthma, heart, and COPD** patients are at high risk
    - Real-time awareness can **save lives**

    ### 🛠️ Tech Stack

    - **Frontend:** Streamlit
    - **Data:** Realistic simulated data (no API key required)
    - **Visualization:** Plotly, Streamlit Maps
    - **Deployment:** Streamlit Cloud

    ### 📊 Data Note

    This app uses **simulated AQI data** that mimics real-world patterns:
    - City-specific base pollution levels (Lahore high, Islamabad lower)
    - Time-of-day variations (worse during rush hours)
    - Realistic pollutant ratios

    For production use, the data layer can be swapped with a real API
    (AQICN, OpenWeather) by replacing a single function.

    ### ⚠️ Disclaimer

    For **educational purposes only**. Always consult a medical professional
    for health concerns.

    ### 📞 Emergency

    If you experience breathing difficulty, chest pain, or severe symptoms,
    **call emergency services immediately**.
    """)


# ============================================================
# FOOTER
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.78rem;
     padding:1rem 0; border-top:1px solid #e2e8f0;">
    AirAware v1.0  ·  Simulated AQI Data  ·  Built with Streamlit
</div>
""", unsafe_allow_html=True)
