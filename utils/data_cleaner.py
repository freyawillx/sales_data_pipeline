import pandas as pd

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.dropna(subset=["date", "product", "quantity", "price"], inplace=True)
    df = df.loc[df['product'].astype(str).str.strip().ne('')].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=["date"], inplace=True)
    quantity = pd.to_numeric(df['quantity'], errors='coerce')
    df = df.loc[quantity.notna() & quantity.mod(1).eq(0)].copy()
    df['quantity'] = quantity.loc[df.index].astype(int)
    df['price'] = df['price'].astype(float)
    df = df.loc[df['price'] >= 0].copy()
    return df
