"""
PRODIGY_DS_01
=============
Task 1 (Data Science Internship, Prodigy InfoTech)
Create a bar chart or histogram to visualize the distribution of a categorical
or continuous variable — here, the distribution of population across the
world's countries (World Bank, "Population, total", 1960-2024).

Author : Divyanshi Shukla
Dataset: World Bank World Development Indicators — SP.POP.TOTL
         https://github.com/Prodigy-InfoTech/data-science-datasets/tree/main/Task%201
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")
PALETTE = "crest"
LATEST_YEAR = "2024"
OUT = "outputs"

# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
def load_data():
    """World Bank exports have 4 metadata lines above the real header."""
    pop = pd.read_csv("data/world_population.csv", skiprows=4)
    meta = pd.read_csv("data/metadata_country.csv")
    return pop, meta


# ---------------------------------------------------------------------------
# 2. CLEAN
# ---------------------------------------------------------------------------
def clean_data(pop: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    # Drop the trailing empty "Unnamed" column the World Bank CSV always ships with
    pop = pop.loc[:, ~pop.columns.str.startswith("Unnamed")]

    # The raw file mixes 217 real countries with 49 aggregate rows (e.g. "World",
    # "High income", "East Asia & Pacific"). Aggregates have no Region in the
    # metadata file, so an inner join isolates true countries only.
    df = pop.merge(meta[["Country Code", "Region", "IncomeGroup"]], on="Country Code", how="inner")
    df = df[df["Region"].notna()].copy()

    # Duplicate check
    dupes = df.duplicated(subset="Country Code").sum()

    # Missing values: keep only countries with a reported figure for the latest year
    before = len(df)
    df = df.dropna(subset=[LATEST_YEAR]).copy()
    dropped = before - len(df)

    df[LATEST_YEAR] = df[LATEST_YEAR].astype(float)
    df["Population (millions)"] = df[LATEST_YEAR] / 1_000_000

    print(f"[clean] duplicate country codes found : {dupes}")
    print(f"[clean] countries dropped (missing {LATEST_YEAR} value): {dropped}")
    print(f"[clean] final dataset: {len(df)} countries x {df.shape[1]} columns")
    return df


# ---------------------------------------------------------------------------
# 3. VISUALIZE
# ---------------------------------------------------------------------------
def plot_top_countries_bar(df: pd.DataFrame):
    """Bar chart — categorical variable: the 15 most populous countries."""
    top15 = df.nlargest(15, LATEST_YEAR).sort_values(LATEST_YEAR)

    fig, ax = plt.subplots(figsize=(11, 8))
    colors = sns.color_palette(PALETTE, len(top15))
    bars = ax.barh(top15["Country Name"], top15["Population (millions)"], color=colors)

    for bar, val in zip(bars, top15["Population (millions)"]):
        ax.text(bar.get_width() + 15, bar.get_y() + bar.get_height() / 2,
                 f"{val:,.0f}M", va="center", fontsize=11)

    ax.set_xlabel("Population (millions)")
    ax.set_title(f"Top 15 Most Populous Countries ({LATEST_YEAR})", fontsize=18, weight="bold", pad=15)
    ax.set_xlim(0, top15["Population (millions)"].max() * 1.15)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(f"{OUT}/01_top15_countries_bar.png", dpi=150)
    plt.close()


def plot_population_histogram(df: pd.DataFrame):
    """Histogram — continuous variable: how population is distributed across all countries."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Raw scale: extremely right-skewed (China/India dwarf everything else)
    sns.histplot(df["Population (millions)"], bins=30, color="#3A7CA5", ax=axes[0], edgecolor="white")
    axes[0].set_title("Raw Scale", fontsize=14, weight="bold")
    axes[0].set_xlabel("Population (millions)")
    axes[0].set_ylabel("Number of Countries")

    # Log scale: reveals the true underlying (roughly log-normal) shape
    sns.histplot(np.log10(df[LATEST_YEAR]), bins=30, color="#D9822B", ax=axes[1], edgecolor="white")
    axes[1].set_title("Log10 Scale", fontsize=14, weight="bold")
    axes[1].set_xlabel("log10(Population)")
    axes[1].set_ylabel("")

    fig.suptitle(f"Distribution of Country Population ({LATEST_YEAR}, n={len(df)})", fontsize=18, weight="bold")
    sns.despine()
    plt.tight_layout()
    plt.savefig(f"{OUT}/02_population_histogram.png", dpi=150)
    plt.close()


def plot_region_bar(df: pd.DataFrame):
    """Bar chart — categorical variable: total population by World Bank region."""
    region_totals = (
        df.groupby("Region")[LATEST_YEAR].sum().sort_values(ascending=False) / 1_000_000
    )

    fig, ax = plt.subplots(figsize=(11, 7))
    colors = sns.color_palette(PALETTE, len(region_totals))
    bars = ax.bar(region_totals.index, region_totals.values, color=colors)

    for bar, val in zip(bars, region_totals.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 20, f"{val:,.0f}M",
                 ha="center", fontsize=10)

    ax.set_ylabel("Population (millions)")
    ax.set_title(f"Total Population by World Bank Region ({LATEST_YEAR})", fontsize=18, weight="bold", pad=15)
    plt.xticks(rotation=35, ha="right")
    sns.despine(left=True)
    plt.tight_layout()
    plt.savefig(f"{OUT}/03_population_by_region_bar.png", dpi=150)
    plt.close()


def plot_income_group_box(df: pd.DataFrame):
    """Bonus: how population varies (log scale) across World Bank income groups."""
    order = ["Low income", "Lower middle income", "Upper middle income", "High income"]
    d = df[df["IncomeGroup"].isin(order)].copy()
    d["log_pop"] = np.log10(d[LATEST_YEAR])

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.boxplot(data=d, x="IncomeGroup", y="log_pop", hue="IncomeGroup", order=order,
                 palette=PALETTE, legend=False, ax=ax)
    sns.stripplot(data=d, x="IncomeGroup", y="log_pop", order=order, color="black", alpha=0.35, ax=ax)

    ax.set_ylabel("log10(Population)")
    ax.set_xlabel("")
    ax.set_title(f"Population Spread by Income Group ({LATEST_YEAR})", fontsize=18, weight="bold", pad=15)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([lbl.replace(" income", "\nincome") for lbl in order], fontsize=13)
    sns.despine()
    plt.tight_layout()
    plt.savefig(f"{OUT}/04_population_by_income_group.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# 4. INSIGHTS
# ---------------------------------------------------------------------------
def print_insights(df: pd.DataFrame):
    total_world = df[LATEST_YEAR].sum() / 1_000_000
    top2_share = df.nlargest(2, LATEST_YEAR)[LATEST_YEAR].sum() / df[LATEST_YEAR].sum() * 100
    median_pop = df[LATEST_YEAR].median() / 1_000_000
    mean_pop = df[LATEST_YEAR].mean() / 1_000_000
    skew = df[LATEST_YEAR].skew()

    print("\n===== KEY INSIGHTS =====")
    print(f"Countries analyzed              : {len(df)}")
    print(f"Combined population ({LATEST_YEAR})       : {total_world:,.0f} million")
    print(f"India + China share of total    : {top2_share:.1f}%")
    print(f"Mean country population         : {mean_pop:,.1f} million")
    print(f"Median country population       : {median_pop:,.1f} million  (mean >> median => heavy right skew)")
    print(f"Skewness of raw distribution    : {skew:.2f}")
    print(f"Top region by population        : {df.groupby('Region')[LATEST_YEAR].sum().idxmax()}")


if __name__ == "__main__":
    pop_raw, meta_raw = load_data()
    data = clean_data(pop_raw, meta_raw)

    plot_top_countries_bar(data)
    plot_population_histogram(data)
    plot_region_bar(data)
    plot_income_group_box(data)
    print_insights(data)

    print("\nAll charts saved to ./outputs/")
