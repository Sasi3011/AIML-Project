# Smart Fertilizer Recommender System

This project provides a machine learning-based API for recommending fertilizer types and quantities based on various agricultural parameters.

## Project Structure

```
AIML Project/
├── data/                   # Data files
├── docs/                   # Documentation
├── models/                 # Trained models
├── notebooks/              # Jupyter notebooks for EDA and modeling
├── reports/                # Evaluation reports and visualizations
└── src/                    # Source code
    ├── app/                # FastAPI application
    │   └── api.py          # Main API endpoints
    ├── data/               # Data loading utilities
    └── ui/                 # User interface components
```

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIML-Project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn src.app.api:app --reload
   ```

2. **Access the API**
   - Open your browser and go to: http://127.0.0.1:8000
   - API documentation (Swagger UI): http://127.0.0.1:8000/docs

## API Endpoints

- `GET /`: Check if the API is running
- `POST /predict`: Get fertilizer recommendation

### Example Request

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
    "Crop_Type": "Wheat",
    "Region": "North",
    "Soil_Type": "Loamy",
    "Soil_pH": 6.5,
    "Nitrogen_Level": 150.0,
    "Phosphorus_Level": 25.0,
    "Potassium_Level": 120.0,
    "Organic_Carbon": 1.2,
    "Moisture_Content": 25.5,
    "Rainfall_mm": 750.0,
    "Temperature_C": 28.0,
    "Plant_Age_Weeks": 8,
    "Application_Timing": "Early Morning"
  }'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
