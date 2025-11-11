
# 🌾 Smart Fertilizer Recommender — Model Card

**Generated:** Automatically  
**Version:** 1.0  

**Models Used:**
- RandomForestClassifier — Fertilizer Type  
- RandomForestRegressor — Recommended Quantity  

**Performance:**
- Accuracy: 0.82  
- MAE: 13.37  
- R²: 0.12  

**Data Summary:**
- ~16592 samples  
- 15 input features (Crop type, Region, Soil properties, Weather, etc.)

**Purpose:**
To recommend the optimal fertilizer type and quantity per acre based on soil nutrients, crop type, and climate.

**Limitations:**
- May not generalize perfectly to new soil types or extreme weather.  
- Retrain yearly with updated data for local calibration.  

**Ethical Note:**
Model designed for assisting, not replacing, agricultural expertise.
