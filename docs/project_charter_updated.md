# Project Charter — Smart Fertilizer Recommender

**Objective:** Recommend fertilizer type and quantity (kg/acre) for smallholder farmers using soil, crop, plant age, and environmental data.


**Success metrics:**
- Classification accuracy for fertilizer type >= 85%
- MAE for quantity <= 10 kg/acre
- Pilot reduction in fertilizer usage >= 20%


**Stakeholders:** Agronomists, data engineering, extension services


**Deliverables:** EDA report, processed datasets, trained models, API, dashboard

---

## Design Methodology

This system is designed to balance engineering complexity, cost, and environmental sustainability while delivering accurate fertilizer recommendations to smallholder farmers.

- Engineering complexity
  - Modular pipelines: a reproducible data ingestion stage, an extensible feature-engineering layer (e.g., NPK ratios, moisture–pH interactions), and configurable model training pipelines that support hyperparameter search and artifact versioning.
  - Performance considerations: document empirical runtimes for preprocessing and training on representative hardware, estimate memory and disk requirements, and limit feature explosion (e.g., careful choice between one-hot encoding and target/frequency encoding).
  - Integration: separate preprocessor, model, and API components to simplify testing and deployment; use pipelines (sklearn Pipeline / ColumnTransformer) so preprocessing is bundled with models.

- Cost considerations
  - Development costs: estimate person-hours for data cleaning, feature engineering, modeling, and testing.
  - Compute & storage: estimate training compute time (CPU/GPU hours), storage for datasets and model artifacts, and recurring costs for model serving (per-request inference cost, autoscaling overhead).
  - Trade-offs: prefer model architectures that achieve required accuracy while minimizing serving latency and compute costs (e.g., tree ensembles with constrained depth, model distillation, or smaller single-model alternatives).

- Environmental & sustainability relevance
  - Minimize training and inference energy where possible (prefer batched offline inference, lightweight models for edge deployment, and cloud regions with lower carbon intensity).
  - Quantify impact: where feasible, estimate kWh and CO₂e for major experiments and include a plan to favor lower-energy options in production.
  - Societal/environmental benefit: specify how improved fertilizer recommendations reduce runoff, nutrient leaching, and greenhouse gas emissions while improving yield and farmer livelihoods.

## Technical Competency

The project demonstrates competency across data engineering, modeling, evaluation, and deployment.

- Languages & tools
  - Python, pandas, NumPy, scikit-learn, XGBoost / LightGBM, Optuna (hyperparameter tuning), joblib for artifact serialization, and FastAPI/Flask for serving models. Use Docker for environment reproducibility and GitHub Actions (or equivalent) for CI.

- Engineering practices
  - Reproducibility: pin dependencies in `requirements.txt`, set RNG seeds, save preprocessing pipelines (joblib), and record dataset versions.
  - Testing & quality: unit tests for data loaders and small model tests, linting (flake8/black), and CI to run tests automatically.
  - Documentation: keep notebooks focused (clean outputs), maintain `README.md` with run instructions, and include a `models/` and `reports/` folder for artifacts.

- Model validation & explainability
  - Validation: use appropriate splits (train/val/test), cross-validation or time-aware CV if applicable, and clear metrics (MAE, R² for regression; accuracy and classification report for classification).
  - Explainability: provide feature-importance plots and SHAP summaries for key models; include a short model card outlining intended use, limitations, and performance.

## Code & Repo Structure (recommended)

Adopt an industry-friendly repository layout to improve readability and maintainability. Suggested structure:

```
AIML-Project/
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ raw/
│  └─ processed/    # canonical processed datasets
├─ notebooks/       # exploratory notebooks (clear outputs before commit)
├─ src/
│  ├─ data/         # data loading & processing scripts
│  ├─ features/     # feature engineering modules
│  ├─ models/       # model training and evaluation code
│  └─ app/          # serving code / API
├─ models/          # saved model artifacts (avoid committing large binaries)
├─ reports/         # evaluation outputs
└─ docs/
```

Practical repo housekeeping (safe recommendations)
- Keep a single canonical copy of processed datasets under `data/processed/`. If `notebooks/data/processed/` exists, move or remove duplicates to avoid confusion.
- Do not commit virtual environments (`.venv/`, `.venv312/`) — add them to `.gitignore` and optionally delete them from the repository to keep the repo small.
- Remove or avoid committing large notebook outputs (images/HTML). Clear cell outputs before committing or store large artifacts in `reports/` or an external storage.

Safe cleanup steps (dry-run first)
1. Verify duplicates by comparing file hashes for `data/processed/*.csv` vs `notebooks/data/processed/*.csv`.
2. Move or delete duplicates after backup, e.g., create `data/processed/backup_from_notebooks/` if unsure.
3. Remove virtualenv folders from repo (`.venv/`, `.venv312/`) — these can be recreated locally from `requirements.txt`.

I can perform the safe cleanup and reorganization for you (dry-run → backup → apply). Would you like me to proceed with the automated cleanup now, or should I first compute file hashes and present a confirmation list?
