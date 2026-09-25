import pandas as pd

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    required = {'date', 'product', 'quantity', 'price'}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    df.dropna(subset=["date", "product", "quantity", "price"], inplace=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=["date"], inplace=True)
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)
    return df
