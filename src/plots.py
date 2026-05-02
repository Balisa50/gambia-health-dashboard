# makes all the figures for the report
# saves png files to figures/

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean" / "gambia_clean.csv"
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def setup_style():
    sns.set_style("whitegrid")
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["savefig.dpi"] = 140
    plt.rcParams["savefig.bbox"] = "tight"


def label_ends(ax, x, y, fmt="{:.0f}"):
    # puts text on the first and last point of a line
    if len(x) == 0:
        return
    ax.annotate(fmt.format(y[0]), xy=(x[0], y[0]),
                xytext=(5, 5), textcoords="offset points", fontsize=9, color="#444")
    ax.annotate(fmt.format(y[-1]), xy=(x[-1], y[-1]),
                xytext=(5, 5), textcoords="offset points", fontsize=9, color="#444")


def plot_life_expectancy(df):
    s = df["life_expectancy_years"].dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(s.index, s.values, color="#2563eb", linewidth=2.4)
    ax.fill_between(s.index, s.values, alpha=0.08, color="#2563eb")
    label_ends(ax, list(s.index), list(s.values), "{:.1f} yrs")
    ax.set_title("Life expectancy at birth, The Gambia (1960 to today)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Years")
    fig.savefig(FIG / "01_life_expectancy.png")
    plt.close(fig)


def plot_infant_mortality(df):
    s = df["infant_mortality_per_1000"].dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(s.index, s.values, color="#dc2626", linewidth=2.4)
    ax.fill_between(s.index, s.values, alpha=0.08, color="#dc2626")
    label_ends(ax, list(s.index), list(s.values), "{:.0f}")
    ax.set_title("Infant mortality (deaths per 1,000 live births)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 1,000 live births")
    fig.savefig(FIG / "02_infant_mortality.png")
    plt.close(fig)


def plot_maternal_mortality(df):
    s = df["maternal_mortality_per_100k"].dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(s.index, s.values, color="#9333ea", linewidth=2.4, marker="o", markersize=3)
    label_ends(ax, list(s.index), list(s.values), "{:.0f}")
    ax.set_title("Maternal mortality (deaths per 100,000 live births)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 100,000 live births")
    fig.savefig(FIG / "03_maternal_mortality.png")
    plt.close(fig)


def plot_fertility(df):
    s = df["fertility_rate_births_per_woman"].dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(s.index, s.values, color="#059669", linewidth=2.4)
    label_ends(ax, list(s.index), list(s.values), "{:.1f}")
    ax.set_title("Fertility rate (births per woman)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Births per woman")
    fig.savefig(FIG / "04_fertility.png")
    plt.close(fig)


def plot_health_headline(df):
    # the two main charts side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    le = df["life_expectancy_years"].dropna()
    ax1.plot(le.index, le.values, color="#2563eb", linewidth=2.4)
    ax1.fill_between(le.index, le.values, alpha=0.08, color="#2563eb")
    ax1.set_title("Life expectancy almost doubled")
    ax1.set_ylabel("Years at birth")
    ax1.set_xlabel("Year")

    im = df["infant_mortality_per_1000"].dropna()
    ax2.plot(im.index, im.values, color="#dc2626", linewidth=2.4)
    ax2.fill_between(im.index, im.values, alpha=0.08, color="#dc2626")
    ax2.set_title("Infant mortality fell ~85%")
    ax2.set_ylabel("Deaths per 1,000")
    ax2.set_xlabel("Year")

    fig.suptitle("The Gambia: the headline health story (1960 to today)",
                 fontsize=15, fontweight="bold", y=1.02)
    fig.savefig(FIG / "05_health_headline.png")
    plt.close(fig)


def plot_immunization(df):
    s = df["measles_immunization_pct"].dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(s.index, s.values, color="#0891b2", linewidth=2.4)
    ax.fill_between(s.index, s.values, alpha=0.08, color="#0891b2")
    ax.set_ylim(0, 105)
    label_ends(ax, list(s.index), list(s.values), "{:.0f}%")
    ax.set_title("Measles immunization coverage (children 12-23 months)")
    ax.set_xlabel("Year")
    ax.set_ylabel("% of children")
    fig.savefig(FIG / "06_immunization.png")
    plt.close(fig)


def plot_enrolment(df):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    if "primary_enrolment_pct_gross" in df.columns:
        s = df["primary_enrolment_pct_gross"].dropna()
        ax.plot(s.index, s.values, color="#16a34a", linewidth=2.4, label="Primary")
    if "secondary_enrolment_pct_gross" in df.columns:
        s = df["secondary_enrolment_pct_gross"].dropna()
        ax.plot(s.index, s.values, color="#ea580c", linewidth=2.4, label="Secondary")
    ax.set_title("School enrolment, gross %")
    ax.set_xlabel("Year")
    ax.set_ylabel("Gross enrolment ratio (%)")
    ax.legend(frameon=False)
    fig.savefig(FIG / "07_school_enrolment.png")
    plt.close(fig)


def plot_gdp(df):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    if "gdp_per_capita_usd" in df.columns:
        s = df["gdp_per_capita_usd"].dropna()
        ax.plot(s.index, s.values, color="#0f172a", linewidth=2.4, label="GDP per capita (current US$)")
    if "gdp_per_capita_ppp_usd" in df.columns:
        s2 = df["gdp_per_capita_ppp_usd"].dropna()
        ax.plot(s2.index, s2.values, color="#f59e0b", linewidth=2.4, linestyle="--", label="GDP per capita (PPP US$)")
    ax.set_title("GDP per capita")
    ax.set_xlabel("Year")
    ax.set_ylabel("US$")
    ax.legend(frameon=False)
    fig.savefig(FIG / "08_gdp_per_capita.png")
    plt.close(fig)


def plot_macro(df):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    if "inflation_pct" in df.columns:
        s = df["inflation_pct"].dropna()
        ax.plot(s.index, s.values, color="#dc2626", linewidth=1.8, label="Inflation, % yoy")
    if "gdp_growth_pct" in df.columns:
        s = df["gdp_growth_pct"].dropna()
        ax.plot(s.index, s.values, color="#2563eb", linewidth=1.8, label="GDP growth, % yoy")
    ax.axhline(0, color="#999", linewidth=0.8)
    ax.set_title("Macro volatility, inflation and GDP growth")
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual %")
    ax.legend(frameon=False)
    fig.savefig(FIG / "09_macro_volatility.png")
    plt.close(fig)


def plot_remittances(df):
    if "remittances_received_usd" not in df.columns:
        return
    s = df["remittances_received_usd"].dropna() / 1e6
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(s.index, s.values, color="#16a34a", alpha=0.85)
    ax.set_title("Personal remittances received (US$ millions)")
    ax.set_xlabel("Year")
    ax.set_ylabel("US$ millions")
    label_ends(ax, list(s.index), list(s.values), "{:.0f}M")
    fig.savefig(FIG / "10_remittances.png")
    plt.close(fig)


def plot_population_urban(df):
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    pop = df["population_total"].dropna() / 1e6
    ax1.plot(pop.index, pop.values, color="#1e40af", linewidth=2.4, label="Population (millions)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Population (millions)", color="#1e40af")
    ax1.tick_params(axis="y", labelcolor="#1e40af")

    ax2 = ax1.twinx()
    urb = df["urban_population_pct"].dropna()
    ax2.plot(urb.index, urb.values, color="#ea580c", linewidth=2.4, label="Urban %", linestyle="--")
    ax2.set_ylabel("Urban population (%)", color="#ea580c")
    ax2.tick_params(axis="y", labelcolor="#ea580c")
    ax2.spines["right"].set_visible(True)

    ax1.set_title("Population growth and urbanisation")
    fig.savefig(FIG / "11_population_urban.png")
    plt.close(fig)


def plot_correlation(df):
    cols = [
        "life_expectancy_years",
        "infant_mortality_per_1000",
        "fertility_rate_births_per_woman",
        "measles_immunization_pct",
        "primary_enrolment_pct_gross",
        "secondary_enrolment_pct_gross",
        "gdp_per_capita_usd",
        "urban_population_pct",
    ]
    cols = [c for c in cols if c in df.columns]
    corr = df[cols].corr()

    nice_names = {
        "life_expectancy_years": "Life expectancy",
        "infant_mortality_per_1000": "Infant mortality",
        "fertility_rate_births_per_woman": "Fertility rate",
        "measles_immunization_pct": "Measles immun.",
        "primary_enrolment_pct_gross": "Primary enrol.",
        "secondary_enrolment_pct_gross": "Secondary enrol.",
        "gdp_per_capita_usd": "GDP per capita",
        "urban_population_pct": "Urban %",
    }
    corr.index = [nice_names[c] for c in corr.index]
    corr.columns = [nice_names[c] for c in corr.columns]

    fig, ax = plt.subplots(figsize=(8.5, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                vmin=-1, vmax=1, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("How indicators move together (Pearson r)")
    fig.savefig(FIG / "12_correlation.png")
    plt.close(fig)


def plot_decade_averages(df):
    pick = ["life_expectancy_years", "infant_mortality_per_1000", "gdp_per_capita_usd"]
    sub = df[pick].copy()
    sub["decade"] = (sub.index // 10) * 10
    means = sub.groupby("decade").mean(numeric_only=True).dropna(how="all")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    titles = {
        "life_expectancy_years": "Life expectancy (years)",
        "infant_mortality_per_1000": "Infant mortality (/1000)",
        "gdp_per_capita_usd": "GDP per capita (US$)",
    }
    colors = {
        "life_expectancy_years": "#2563eb",
        "infant_mortality_per_1000": "#dc2626",
        "gdp_per_capita_usd": "#0f172a",
    }
    for ax, col in zip(axes, pick):
        if col in means.columns:
            vals = means[col].dropna()
            ax.bar(vals.index.astype(str) + "s", vals.values, color=colors[col], alpha=0.85)
            ax.set_title(titles[col])
            ax.tick_params(axis="x", rotation=30)
    fig.suptitle("Decade averages, the long arc", fontsize=14, fontweight="bold")
    fig.savefig(FIG / "13_decade_averages.png")
    plt.close(fig)


def main():
    setup_style()
    df = pd.read_csv(CLEAN, index_col="year")
    print(f"loaded {df.shape[0]} years, {df.shape[1]} indicators")

    plot_life_expectancy(df)
    plot_infant_mortality(df)
    plot_maternal_mortality(df)
    plot_fertility(df)
    plot_health_headline(df)
    plot_immunization(df)
    plot_enrolment(df)
    plot_gdp(df)
    plot_macro(df)
    plot_remittances(df)
    plot_population_urban(df)
    plot_correlation(df)
    plot_decade_averages(df)

    print(f"all figures saved to {FIG}")


if __name__ == "__main__":
    main()
