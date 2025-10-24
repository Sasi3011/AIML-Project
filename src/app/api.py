from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

# Initialize FastAPI
app = FastAPI(title="Smart Fertilizer Recommender API")

# Configure CORS to allow requests from HTML file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for local development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load models and artifacts
MODELS_DIR = Path("models")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
label_encoders = joblib.load(MODELS_DIR / "label_encoders.pkl")
clf = joblib.load(MODELS_DIR / "fertilizer_type_model.pkl")
reg = joblib.load(MODELS_DIR / "fertilizer_quantity_model.pkl")
final_features = joblib.load(MODELS_DIR / "feature_columns.pkl")  # <--- NEW LINE

# Input schema
class InputData(BaseModel):
    Crop_Type: str
    Region: str
    Soil_Type: str
    Soil_pH: float
    Nitrogen_Level: float
    Phosphorus_Level: float
    Potassium_Level: float
    Organic_Carbon: float
    Moisture_Content: float
    Rainfall_mm: float
    Temperature_C: float
    Plant_Age_Weeks: int
    Application_Timing: str

# Feature engineering
def add_rule_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["High_N_Need"] = (df["Nitrogen_Level"] < 100).astype(int)
    df["High_P_Need"] = (df["Phosphorus_Level"] < 30).astype(int)
    df["High_K_Need"] = (df["Potassium_Level"] < 100).astype(int)
    df["NPK_Ratio"] = df["Nitrogen_Level"] / (df["Phosphorus_Level"] + df["Potassium_Level"] + 1)
    return df

# Prediction endpoint
@app.post("/predict")
def predict(input_data: InputData):
    data = input_data.dict()

    # Safe categorical encoding
    for col, le in label_encoders.items():
        if col in data:
            try:
                data[col] = le.transform([data[col]])[0]
            except ValueError:
                data[col] = 0  # fallback for unseen categories

    df = pd.DataFrame([data])

    # Apply same rule-based features
    df = add_rule_features(df)

    # Ensure all expected columns exist
    for col in final_features:
        if col not in df.columns:
            df[col] = 0

    # Align column order exactly like training
    df = df[final_features]

    # Scale numeric columns
    num_cols = [col for col in df.columns if col in scaler.feature_names_in_]
    df[num_cols] = scaler.transform(df[num_cols])

    # Predict
    fert_type = clf.predict(df)[0]
    fert_qty = reg.predict(df)[0]

    return {
        "Fertilizer_Type": str(fert_type),
        "Recommended_Quantity_kg_per_acre": round(float(fert_qty), 2)
    }

@app.get("/")
def root():
    return {"message": "Smart Fertilizer Recommender API is running successfully!"}
