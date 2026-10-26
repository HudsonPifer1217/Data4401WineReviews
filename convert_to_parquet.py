from pathlib import Path

import pandas as pd

Path("data_clean").mkdir(exist_ok=True)

for csv_path in Path("data").glob("*.csv"):
    df = pd.read_csv(csv_path, index_col=0)
    text_cols = df.select_dtypes(include="str").columns
    df[text_cols] = df[text_cols].apply(lambda s: s.str.strip())
    df = df.drop_duplicates()
    df.to_parquet(f"data_clean/{csv_path.stem}.parquet", index=False)
