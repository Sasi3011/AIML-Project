
# Model Card — Smart Fertilizer Recommender

**Date:** Auto-generated

**Models:**
- Classifier: RandomForestClassifier (fertilizer type)
- Regressor: RandomForestRegressor (fertilizer quantity)

**Performance:**
- Accuracy: 0.23
- MAE: 46.02
- R²: -0.01

**Training Data:** 1000 samples, 15 features  
**Input Fields:** Crop Type, Soil pH, NPK levels, Region, Plant Age, etc.  
**Output:** Fertilizer type + recommended quantity  

**Usage:** Intended for smallholder farmers. The model combines expert rules and ML-based insights.  

**Limitations:** Performance may vary for unseen soil types or rare crops. Retrain annually with new data.
