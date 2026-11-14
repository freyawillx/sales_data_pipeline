import pandas as pd

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    required = ['date', 'product', 'quantity', 'price']
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError('Missing required sales columns: ' + ', '.join(missing))
    df = df.copy()
    df.dropna(subset=["date", "product", "quantity", "price"], inplace=True)
    df = df.loc[df['product'].astype(str).str.strip().ne('')].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=["date"], inplace=True)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df.dropna(subset=['quantity', 'price'], inplace=True)
    df['quantity'] = df['quantity'].astype(int)
    df = df.loc[df['quantity'] >= 0].copy()
    df['price'] = df['price'].astype(float)
    df = df.loc[df['price'] >= 0].copy()
    return df
