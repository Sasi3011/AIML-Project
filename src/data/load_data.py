import pandas as pd
from pathlib import Path

# Define the raw data folder
RAW = Path(__file__).resolve().parents[2] / 'data' / 'raw'

def load_all_raw():
    """
    Loads and combines all raw datasets (CSV and Excel) from data/raw/.
    Returns a single combined DataFrame.
    """
    all_files = list(RAW.glob("*.csv")) + list(RAW.glob("*.xlsx"))
    dataframes = []

    if not all_files:
        print("❌ No raw data files found in 'data/raw/'.")
        return None

    print(f"📂 Found {len(all_files)} raw files:")
    for f in all_files:
        print(f"   - {f.name}")

        try:
            if f.suffix == ".csv":
                df = pd.read_csv(f)
            elif f.suffix in [".xls", ".xlsx"]:
                df = pd.read_excel(f)
            else:
                print(f"⚠️ Skipping unsupported file: {f.name}")
                continue

            df["source_file"] = f.name  # Track file origin
            dataframes.append(df)

        except Exception as e:
            print(f"⚠️ Failed to load {f.name}: {e}")

    # Combine all datasets
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"\n✅ Combined Dataset Loaded Successfully!")
        print(f"📊 Total Rows: {combined_df.shape[0]}, Columns: {combined_df.shape[1]}")
        return combined_df
    else:
        print("❌ No valid datasets loaded.")
        return None


# Run the script directly
if __name__ == "__main__":
    df = load_all_raw()
    if df is not None:
        print("\n🔍 Dataset Preview:")
        print(df.head(5))
        print("\n📋 Column Summary:")
        print(df.columns.tolist())
