"""
Pull World Bank indicators for The Gambia.

Saves one CSV per indicator under data/raw/. Run this once before
anything else. Requires `wbdata` (pip install wbdata).

Indicators cover four buckets the dashboard cares about:
  health     — life expectancy, infant mortality, maternal mortality
  education  — adult literacy, primary/secondary enrolment
  economy    — GDP per capita (current US$ and PPP), inflation
  poverty    — poverty headcount, gini

Country code GMB = The Gambia (ISO-3).
Date range 1960 to today (wbdata returns whatever years exist).
"""

from pathlib import Path
import pandas as pd
import wbdata


COUNTRY = "GMB"

# Canonical World Bank indicator codes.
# Picked carefully so each maps to one of the four buckets above and
# all have decent coverage for The Gambia (some series start later
# than 1960 — that's expected and we keep nulls visible in the EDA).
INDICATORS = {
    # ── HEALTH ──────────────────────────────────────────────────────
    "SP.DYN.LE00.IN":     "life_expectancy_years",
    "SP.DYN.IMRT.IN":     "infant_mortality_per_1000",
    "SH.STA.MMRT":        "maternal_mortality_per_100k",
    "SP.DYN.TFRT.IN":     "fertility_rate_births_per_woman",
    "SH.IMM.MEAS":        "measles_immunization_pct",
    "SH.XPD.CHEX.GD.ZS":  "health_spending_pct_gdp",

    # ── EDUCATION ──────────────────────────────────────────────────
    "SE.ADT.LITR.ZS":     "adult_literacy_pct",
    "SE.PRM.ENRR":        "primary_enrolment_pct_gross",
    "SE.SEC.ENRR":        "secondary_enrolment_pct_gross",
    "SE.XPD.TOTL.GD.ZS":  "education_spending_pct_gdp",

    # ── ECONOMY ────────────────────────────────────────────────────
    "NY.GDP.PCAP.CD":     "gdp_per_capita_usd",
    "NY.GDP.PCAP.PP.CD":  "gdp_per_capita_ppp_usd",
    "NY.GDP.MKTP.KD.ZG":  "gdp_growth_pct",
    "FP.CPI.TOTL.ZG":     "inflation_pct",
    "BX.TRF.PWKR.CD.DT":  "remittances_received_usd",

    # ── POVERTY & POPULATION ───────────────────────────────────────
    "SI.POV.NAHC":        "poverty_headcount_national_pct",
    "SI.POV.GINI":        "gini_index",
    "SP.POP.TOTL":        "population_total",
    "SP.URB.TOTL.IN.ZS":  "urban_population_pct",
}


def fetch_all() -> pd.DataFrame:
    """Pull every indicator and return one wide DataFrame indexed by year."""
    print(f"fetching {len(INDICATORS)} indicators for {COUNTRY}...")
    df = wbdata.get_dataframe(INDICATORS, country=COUNTRY)
    # wbdata returns the date as a string index — coerce to int year
    df.index = pd.to_datetime(df.index).year
    df.index.name = "year"
    df = df.sort_index()
    return df


def save_per_indicator(df: pd.DataFrame, out_dir: Path) -> None:
    """Save each column as its own CSV for granular inspection later."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for col in df.columns:
        path = out_dir / f"{col}.csv"
        df[[col]].dropna().to_csv(path)
    print(f"  per-indicator CSVs written to {out_dir}")


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "data" / "raw"
    out.mkdir(parents=True, exist_ok=True)

    df = fetch_all()
    df.to_csv(out / "gambia_indicators_wide.csv")
    print(f"  wide table: {df.shape[0]} years x {df.shape[1]} indicators")
    save_per_indicator(df, out)
    print("done.")


if __name__ == "__main__":
    main()
