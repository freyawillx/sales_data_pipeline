"""Summarize common CSV data defects without calling the loader or cleaner."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    frame = pd.read_csv(args.input)
    required = ["date", "product", "quantity", "price"]
    missing = [name for name in required if name not in frame]
    if missing:
        parser.error("missing required columns: " + ", ".join(missing))
    quantity = pd.to_numeric(frame["quantity"], errors="coerce")
    price = pd.to_numeric(frame["price"], errors="coerce")
    q_finite = np.isfinite(quantity.to_numpy(dtype=float, na_value=np.nan))
    p_finite = np.isfinite(price.to_numpy(dtype=float, na_value=np.nan))
    report = {"rows": len(frame),
      "missing_required_rows": int(frame[required].isna().any(axis=1).sum()),
      "blank_product_rows": int(frame["product"].fillna("").astype(str).str.strip().eq("").sum()),
      "invalid_date_rows": int(pd.to_datetime(frame["date"], errors="coerce").isna().sum()),
      "invalid_or_nonfinite_quantities": int((~q_finite).sum()),
      "invalid_or_nonfinite_prices": int((~p_finite).sum()),
      "negative_quantities": int(quantity.lt(0).sum()),
      "negative_prices": int(price.lt(0).sum()),
      "fractional_quantities": int((quantity[q_finite] % 1 != 0).sum())}
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
