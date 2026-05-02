# clean the raw indicator data
# drops indicators with too few observations
# forward fills only the slow moving ones (population, urbanization)

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "gambia_indicators_wide.csv"
OUT = ROOT / "data" / "clean" / "gambia_clean.csv"

# these have less than 5 data points so not useful for trends
drop_cols = ["poverty_headcount_national_pct", "gini_index", "adult_literacy_pct"]

# safe to forward fill these (population doesnt jump)
ffill_cols = ["population_total", "urban_population_pct"]


def clean():
    df = pd.read_csv(RAW, index_col="year")
    df.index = df.index.astype(int)
    df = df.sort_index()

    # drop low coverage columns
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # make sure everything is numeric
    df = df.apply(pd.to_numeric, errors="coerce")

    # forward fill the slow moving stuff
    for col in ffill_cols:
        if col in df.columns:
            df[col] = df[col].ffill()

    # drop fully empty years
    df = df.dropna(how="all")
    return df


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df = clean()
    df.to_csv(OUT)
    print(f"clean shape: {df.shape}")
    print(f"years: {df.index.min()} to {df.index.max()}")
    print(f"saved to {OUT}")


if __name__ == "__main__":
    main()
