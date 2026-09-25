import pandas as pd

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.dropna(subset=["date", "product", "quantity", "price"], inplace=True)
    df = df.loc[df['product'].astype(str).str.strip().ne('')].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=["date"], inplace=True)
    df['date'] = df['date'].dt.date
    df['quantity'] = df['quantity'].astype(int)
    df = df.loc[df['quantity'] >= 0].copy()
    df['price'] = df['price'].astype(float)
    df = df.loc[df['price'] >= 0].copy()
    return df
