# pulls Gambia indicators from World Bank
# run this first

from pathlib import Path
import pandas as pd
import wbdata


COUNTRY = "GMB"

# indicators i want
# health, education, economy, poverty
INDICATORS = {
    "SP.DYN.LE00.IN":     "life_expectancy_years",
    "SP.DYN.IMRT.IN":     "infant_mortality_per_1000",
    "SH.STA.MMRT":        "maternal_mortality_per_100k",
    "SP.DYN.TFRT.IN":     "fertility_rate_births_per_woman",
    "SH.IMM.MEAS":        "measles_immunization_pct",
    "SH.XPD.CHEX.GD.ZS":  "health_spending_pct_gdp",

    "SE.ADT.LITR.ZS":     "adult_literacy_pct",
    "SE.PRM.ENRR":        "primary_enrolment_pct_gross",
    "SE.SEC.ENRR":        "secondary_enrolment_pct_gross",
    "SE.XPD.TOTL.GD.ZS":  "education_spending_pct_gdp",

    "NY.GDP.PCAP.CD":     "gdp_per_capita_usd",
    "NY.GDP.PCAP.PP.CD":  "gdp_per_capita_ppp_usd",
    "NY.GDP.MKTP.KD.ZG":  "gdp_growth_pct",
    "FP.CPI.TOTL.ZG":     "inflation_pct",
    "BX.TRF.PWKR.CD.DT":  "remittances_received_usd",

    "SI.POV.NAHC":        "poverty_headcount_national_pct",
    "SI.POV.GINI":        "gini_index",
    "SP.POP.TOTL":        "population_total",
    "SP.URB.TOTL.IN.ZS":  "urban_population_pct",
}


def fetch_all():
    print(f"fetching {len(INDICATORS)} indicators for {COUNTRY}")
    df = wbdata.get_dataframe(INDICATORS, country=COUNTRY)
    # year comes back as string, convert to int
    df.index = pd.to_datetime(df.index).year
    df.index.name = "year"
    df = df.sort_index()
    return df


def save_per_indicator(df, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for col in df.columns:
        df[[col]].dropna().to_csv(out_dir / f"{col}.csv")
    print(f"saved per-indicator csvs in {out_dir}")


def main():
    out = Path(__file__).resolve().parents[1] / "data" / "raw"
    out.mkdir(parents=True, exist_ok=True)

    df = fetch_all()
    df.to_csv(out / "gambia_indicators_wide.csv")
    print(f"wide table: {df.shape[0]} years, {df.shape[1]} indicators")
    save_per_indicator(df, out)
    print("done")


if __name__ == "__main__":
    main()
