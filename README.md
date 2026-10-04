# 🌫️ AirAware — Air Quality Alert System

A real-time air quality monitoring app with personalized health advisories.
**No API key required** — all data is realistically simulated.

## ✨ Features

- 🏠 **Live AQI Dashboard** — Color-coded air quality with alerts
- 👤 **Health Profile** — Set condition, activity, age for personalization
- 🔔 **Smart Alerts** — Warning when AQI exceeds your threshold
- 🗺️ **Pollution Map** — 12+ cities with live rankings
- 📊 **Compare Cities** — Interactive bar charts + pollutant comparison
- 💡 **Personalized Advice** — Do's & don'ts based on YOUR profile
- 😷 **Mask Recommendation** — Know which mask to wear

## 🚀 Deploy on Streamlit Cloud (Free)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "AirAware - Air Quality Alert System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/airaware.git
git push -u origin main
```

### 2. Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select repo → `app.py` → **Deploy**
4. Live in 2-3 minutes! 🎉

## 🧑‍💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Data | Simulated (no API key) |
| Charts | Plotly |
| Deploy | Streamlit Cloud |

## 📁 Structure

```
airaware/
├── app.py              # Main Streamlit app
├── data.py             # City data + AQI simulation
├── advisories.py       # Health advice engine
├── requirements.txt
└── README.md
```

## 🌍 Covered Cities

🇵🇰 Lahore, Karachi, Islamabad, Rawalpindi, Faisalabad, Multan, Peshawar, Quetta  
🇮🇳 Delhi, Mumbai  
🇧🇩 Dhaka  
🇨🇳 Beijing

## 🎯 Use Cases

- **Asthma patients** — Know when to stay indoors
- **Parents** — Protect children from pollution
- **Outdoor workers** — Plan work hours
- **Athletes** — Skip outdoor workouts on bad days
- **Commuters** — Choose safe travel times

## ⚠️ Disclaimer

**Educational purposes only.** Data is simulated for demonstration.
For production, swap with real API (AQICN / OpenWeather).

## 📄 License

MIT
