import pandas as pd
import gutenbergpy.textget
import tensorflow as tf

from pathlib import Path

data_dir=Path("./data/")
df = pd.concat([pd.read_csv(f, na_filter=True, na_values="[]") for f in data_dir.glob("genres-*.csv")], ignore_index=True)
df = df.dropna()

print(df)

def get_text(text_id):
    raw = gutenbergpy.textget.get_text_by_id(text_id)
    clean = gutenbergpy.textget.strip_headers(raw).decode("utf-8")

    return clean

df["Text"] = [get_text(text_id) for text_id in df["Text#"]]

df.to_csv("./data/dataset.csv")

df = pd.read_csv("./data/dataset.csv")
