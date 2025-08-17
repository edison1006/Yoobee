import pandas as pd
import numpy as np
from pathlib import Path

CSV_PATH = "/Users/zhangxiaoyu/Desktop/Project/Yoobee/PSE-Activity/week3/AirQualityUCI.csv"
PARQUET_PATH = "/Users/zhangxiaoyu/Desktop/Project/Yoobee/PSE-Activity/week3/output.parquet"

CAND_SEPS = [";", ",", "\t", "|"]
CAND_ENCODINGS = ["utf-8", "latin1"]

def sniff_sep(sample: str):
    counts = {sep: sample.count(sep) for sep in CAND_SEPS}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else None

def robust_read_csv(path: str) -> pd.DataFrame:
    p = Path(path)
    head = p.read_bytes()[:4096].decode("utf-8", errors="ignore")
    guess = sniff_sep(head)

    na_vals = [-200, "-200", "NA", "N/A", ""]
    tried = []

    if guess:
        for enc in CAND_ENCODINGS:
            try:
                df = pd.read_csv(path, sep=guess, encoding=enc, na_values=na_vals, low_memory=False)
                if df.shape[1] > 1:
                    return df
                tried.append((guess, enc, "one-column"))
            except Exception as e:
                tried.append((guess, enc, repr(e)))

    for sep in CAND_SEPS:
        for enc in CAND_ENCODINGS:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, na_values=na_vals, low_memory=False)
                if df.shape[1] > 1:
                    return df
                tried.append((sep, enc, "one-column"))
            except Exception as e:
                tried.append((sep, enc, repr(e)))

    try:
        return pd.read_csv(path, sep=None, engine="python", na_values=na_vals, low_memory=False)
    except Exception as e:
        raise RuntimeError(f"Failed to parse CSV. Tried: {tried}\nLast error: {e}")

def main():
    print(f"Loading CSV: {CSV_PATH}")
    df = robust_read_csv(CSV_PATH)
    print("Loaded shape:", df.shape)

    num = df.apply(pd.to_numeric, errors="coerce")

    stats = pd.DataFrame({
        "min":      num.min(),
        "max":      num.max(),
        "mean":     num.mean(),
        "mean_abs": num.abs().mean(),
        "count":    num.count(),
        "nulls":    num.isna().sum()
    }).dropna(how="all") 

    stats.to_csv("column_stats.csv")
    print("Saved stats -> column_stats.csv")
    print(stats.head(10))

    try:
        df.to_parquet(PARQUET_PATH, index=False)
        print("Saved Parquet ->", PARQUET_PATH)
    except Exception as e:
        print("Parquet skipped (install pyarrow to enable). Error:", e)

if __name__ == "__main__":
    main()
