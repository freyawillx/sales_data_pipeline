import pandas as pd
import numpy as np

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(subset=["date", "product", "quantity", "price"], inplace=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=["date"], inplace=True)
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)
    df = df.loc[np.isfinite(df['price'])].copy()
    return df
