"""
Clean the raw indicator table.

Choices made and why, so it's easy to follow:
  - Drop indicators where I have under 5 observations (poverty, gini,
    adult_literacy). Three points cannot show a trend honestly.
  - Forward-fill ONLY for population and urban_population_pct, which
    move slowly. Never forward-fill mortality or income — that hides
    real gaps.
  - Convert all numeric columns to float, drop years that have nothing
    in any column.
  - Save to data/clean/gambia_clean.csv ready for the notebook + plots.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "gambia_indicators_wide.csv"
OUT = ROOT / "data" / "clean" / "gambia_clean.csv"

# Indicators with fewer than 5 obs are not useful for a trend story.
# We keep them in raw/ for reference but exclude from the clean table.
DROP_LOW_COVERAGE = {
    "poverty_headcount_national_pct",  # only 3 obs
    "gini_index",                      # only 5 obs
    "adult_literacy_pct",              # only 4 obs
}

# Slow-moving indicators where forward-fill is safe.
FORWARD_FILL = {"population_total", "urban_population_pct"}


def clean() -> pd.DataFrame:
    df = pd.read_csv(RAW, index_col="year")
    df.index = df.index.astype(int)
    df = df.sort_index()

    # 1. Drop low-coverage columns
    keep = [c for c in df.columns if c not in DROP_LOW_COVERAGE]
    df = df[keep]

    # 2. Coerce types
    df = df.apply(pd.to_numeric, errors="coerce")

    # 3. Targeted forward fill
    for col in FORWARD_FILL:
        if col in df.columns:
            df[col] = df[col].ffill()

    # 4. Drop years that are entirely empty (defensive)
    df = df.dropna(how="all")

    return df


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df = clean()
    df.to_csv(OUT)
    print(f"clean: {df.shape[0]} years x {df.shape[1]} indicators -> {OUT}")
    print(f"year range: {df.index.min()} to {df.index.max()}")


if __name__ == "__main__":
    main()
