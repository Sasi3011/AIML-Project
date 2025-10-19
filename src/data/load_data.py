import pandas as pd
from pathlib import Path


RAW = Path('data/raw')




def load_raw(filepath=None):
filepath = filepath or RAW / 'Smart_Fertilizer_Recommender_Dataset.xlsx'
df = pd.read_excel(filepath)
return df




if __name__ == '__main__':
df = load_raw()
print('Loaded', df.shape)
print(df.dtypes)