import streamlit as st
import requests
import pandas as pd

# =========================================================
# 1. Page Configuration
# =========================================================
st.set_page_config(
    page_title="Smart Fertilizer Recommender",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 Smart Fertilizer Recommender")
st.markdown("### Get the right fertilizer type and quantity for your farm")

# =========================================================
# 2. API Endpoint
# =========================================================
API_URL = "http://127.0.0.1:8000/predict"  # FastAPI must be running

# =========================================================
# 3. Input Form
# =========================================================
with st.form("fertilizer_form"):
    col1, col2 = st.columns(2)

    with col1:
        crop = st.selectbox("Crop Type", ["Rice", "Wheat", "Groundnut", "Cotton", "Tomato", "Maize"])
        region = st.selectbox("Region", ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Maharashtra", "Punjab"])
        soil_type = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy", "Red", "Black"])
        ph = st.number_input("Soil pH", min_value=3.0, max_value=9.0, value=6.5, step=0.1)
        organic_carbon = st.number_input("Organic Carbon (%)", min_value=0.0, max_value=5.0, value=1.2)

    with col2:
        nitrogen = st.number_input("Nitrogen Level", min_value=0, max_value=300, value=120)
        phosphorus = st.number_input("Phosphorus Level", min_value=0, max_value=150, value=40)
        potassium = st.number_input("Potassium Level", min_value=0, max_value=300, value=180)
        moisture = st.number_input("Moisture Content (%)", min_value=0, max_value=100, value=25)
        rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=1500, value=600)

    col3, col4 = st.columns(2)
    with col3:
        temperature = st.number_input("Temperature (°C)", min_value=0, max_value=50, value=30)
    with col4:
        plant_age = st.number_input("Plant Age (weeks)", min_value=1, max_value=52, value=8)

    app_timing = st.selectbox("Application Timing", ["Before sowing", "After sowing", "Mid-growth", "Flowering"])

    submitted = st.form_submit_button("🔍 Recommend Fertilizer")

# =========================================================
# 4. Handle Submission
# =========================================================
if submitted:
    payload = {
        "Crop_Type": crop,
        "Region": region,
        "Soil_Type": soil_type,
        "Soil_pH": ph,
        "Nitrogen_Level": nitrogen,
        "Phosphorus_Level": phosphorus,
        "Potassium_Level": potassium,
        "Organic_Carbon": organic_carbon,
        "Moisture_Content": moisture,
        "Rainfall_mm": rainfall,
        "Temperature_C": temperature,
        "Plant_Age_Weeks": plant_age,
        "Application_Timing": app_timing
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()

            st.success("✅ Recommendation Generated")
            st.markdown(f"""
            **Fertilizer Type:** 🌿 `{result['Fertilizer_Type']}`  
            **Recommended Quantity:** {result['Recommended_Quantity_kg_per_acre']} kg/acre
            """)

            # Optional: Display summary table
            st.subheader("📊 Input Summary")
            st.dataframe(pd.DataFrame([payload]))

        else:
            st.error(f"⚠️ API Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI. Please make sure it's running (port 8000).")

# =========================================================
# 5. Footer
# =========================================================
st.markdown("---")
st.caption("Made with ❤️ by Sasi | Smart Fertilizer Recommender 2025")
