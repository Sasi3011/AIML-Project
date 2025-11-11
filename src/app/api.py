from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any

app = FastAPI(title="Smart Fertilizer Recommender API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS_DIR = Path("models")


def _load_first(candidates):
    """Load the first existing artifact from candidates (list of filenames). Returns object or None."""
    for name in candidates:
        p = MODELS_DIR / name
        if p.exists():
            try:
                return joblib.load(p)
            except Exception as e:
                raise RuntimeError(f"Failed loading {p}: {e}")
    return None


# Load artifacts (prefer latest/hybrid names, fall back to older names)
scaler = _load_first(["scaler.pkl"])  # numeric feature scaler
y_scaler = _load_first(["y_scaler.pkl", "y_scaler.sav"])
label_encoders: Optional[Dict[str, Any]] = _load_first(["label_encoders.pkl", "label_encoders.sav"])
fert_label = _load_first(["fertilizer_label_encoder.pkl", "fertilizer_label_encoder.sav"])
target_encoder = _load_first(["target_encoder.pkl"])

clf = _load_first([
    "hybrid_fertilizer_type_model_v2.pkl",
    "hybrid_fertilizer_type_model.pkl",
    "fertilizer_type_model.pkl",
])
reg = _load_first([
    "hybrid_fertilizer_quantity_model_v2.pkl",
    "hybrid_fertilizer_quantity_model.pkl",
    "fertilizer_quantity_model.pkl",
])

final_features = _load_first(["feature_columns.pkl", "final_features.pkl", "feature_columns_list.pkl"]) or None


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


def add_rule_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["High_N_Need"] = (df["Nitrogen_Level"] < 100).astype(int)
    df["High_P_Need"] = (df["Phosphorus_Level"] < 30).astype(int)
    df["High_K_Need"] = (df["Potassium_Level"] < 100).astype(int)
    df["NPK_Ratio"] = df["Nitrogen_Level"] / (df["Phosphorus_Level"] + df["Potassium_Level"] + 1e-6)
    return df


def _ensure_models_loaded():
    missing = []
    if clf is None:
        missing.append("classifier (hybrid_fertilizer_type_model_v2.pkl or fallback)")
    if reg is None:
        missing.append("regressor (hybrid_fertilizer_quantity_model_v2.pkl or fallback)")
    if scaler is None:
        missing.append("scaler (scaler.pkl)")
    if missing:
        raise RuntimeError("Missing model artifacts: " + ", ".join(missing))


@app.post("/predict")
def predict(input_data: InputData):
    try:
        _ensure_models_loaded()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    data = input_data.dict()

    # Apply label encoders (if available) to categorical inputs
    if label_encoders and isinstance(label_encoders, dict):
        for col, le in label_encoders.items():
            if col in data:
                try:
                    data[col] = le.transform([data[col]])[0]
                except Exception:
                    data[col] = 0
    elif target_encoder is not None:
        # target encoder expects a DataFrame; we'll transform later
        pass

    df = pd.DataFrame([data])

    # Add rule-based features
    df = add_rule_features(df)

    # If target_encoder exists (category_encoders.TargetEncoder), apply it
    if target_encoder is not None:
        try:
            df = target_encoder.transform(df)
        except Exception:
            # if transform fails, continue with available numeric/coded columns
            pass

    # Ensure any remaining non-numeric columns are converted to numeric.
    # Prefer stored label encoders when available, otherwise use category codes as a fallback.
    for col in df.select_dtypes(include=['object', 'category']).columns:
        transformed = False
        if label_encoders is not None:
            try:
                # label_encoders may be a dict mapping column->encoder
                if isinstance(label_encoders, dict) and col in label_encoders:
                    le = label_encoders[col]
                    df[col] = le.transform(df[col].astype(str)).astype(int)
                    transformed = True
            except Exception:
                transformed = False

        if not transformed:
            # fallback: convert to category codes (best-effort)
            try:
                df[col] = df[col].astype('category').cat.codes
            except Exception:
                # last resort: map unique values to integers
                mapping = {v: i for i, v in enumerate(df[col].astype(str).unique())}
                df[col] = df[col].astype(str).map(mapping).fillna(0).astype(int)

    # Ensure we have the expected feature columns and order
    if final_features is not None:
        # final_features may be a list or array
        features_list = list(final_features)
    else:
        features_list = [c for c in df.columns]

    for col in features_list:
        if col not in df.columns:
            df[col] = 0

    df = df[features_list]

    # Numeric scaling: safely pick numeric columns that scaler knows about
    try:
        if scaler is not None:
            if hasattr(scaler, "feature_names_in_"):
                num_cols = [c for c in df.columns if c in list(scaler.feature_names_in_)]
            else:
                # fallback: assume all columns are numeric
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                df[num_cols] = scaler.transform(df[num_cols])
    except Exception:
        # if scaling fails, proceed without scaling (best-effort)
        pass

    # Predict
    try:
        raw_fert = clf.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classifier prediction failed: {e}")

    # Decode fertilizer label if encoder present
    fert_type: str
    if fert_label is not None:
        try:
            fert_type = fert_label.inverse_transform([raw_fert])[0]
        except Exception:
            try:
                fert_type = str(raw_fert)
            except Exception:
                fert_type = "Unknown"
    else:
        try:
            fert_type = str(raw_fert)
        except Exception:
            fert_type = "Unknown"

    # Regression prediction (quantity)
    try:
        raw_qty = reg.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regressor prediction failed: {e}")

    try:
        if y_scaler is not None:
            qty = float(y_scaler.inverse_transform(np.array(raw_qty).reshape(-1, 1)).ravel()[0])
        else:
            qty = float(raw_qty)
    except Exception:
        qty = float(raw_qty)

    return {
        "Fertilizer_Type": fert_type,
        "Recommended_Quantity_kg_per_acre": round(qty, 2)
    }


@app.get("/")
def root():
    return {"message": "Smart Fertilizer Recommender API is running successfully!"}