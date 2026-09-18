# PRODIGY_DS_01 — Population Distribution (Bar Chart & Histogram)

Task 1 of the **Data Science Internship at Prodigy InfoTech**.

> Create a bar chart or histogram to visualize the distribution of a categorical or continuous
> variable, such as the distribution of ages or genders in a population.

This submission uses the **World Bank — World Development Indicators, "Population, total"**
dataset (linked from Prodigy InfoTech's own [Task 1 dataset repo](https://github.com/Prodigy-InfoTech/data-science-datasets/tree/main/Task%201)),
which reports the population of every country from **1960 to 2024**.

## What's in here

| File | What it is |
|---|---|
| `PRODIGY_DS_01.ipynb` | Full notebook — cleaning, EDA, 4 charts, insights (run top-to-bottom) |
| `eda.py` | Same analysis as a standalone, reusable Python script |
| `data/world_population.csv` | Raw dataset (World Bank export) |
| `data/metadata_country.csv` | Country metadata (region / income group) used for cleaning |
| `outputs/*.png` | The generated charts, saved at 150 DPI |
| `requirements.txt` | pandas, numpy, matplotlib, seaborn |

## How to run

```bash
pip install -r requirements.txt
python eda.py              # regenerates all 4 charts in outputs/
# or open PRODIGY_DS_01.ipynb in Jupyter to see the full walkthrough
```

## Approach

1. **Load** the raw World Bank CSV (its exports always ship with 4 metadata lines above the
   real header) and the accompanying country metadata file.
2. **Clean**:
   - The raw file mixes **217 real countries** with **49 regional/income aggregates** (e.g.
     `"World"`, `"High income"`, `"East Asia & Pacific"`). These aggregates have no `Region`
     in the metadata table, so they're filtered out via an inner join — otherwise every chart
     would be double-counting the world's population several times over.
   - Checked for duplicate country codes (none) and missing values in the latest year (none).
3. **Visualize**:
   - **Histogram** of population across all 217 countries — shown on both a raw and log10
     scale, since population is heavily right-skewed.
   - **Bar chart** of the 15 most populous countries.
   - **Bar chart** of total population by World Bank region.
   - *(Bonus)* Boxplot of population spread across World Bank income groups.
4. **Summarize** the insights (see below).

## Key insights

- After cleaning, **217 countries** were analyzed (49 aggregate rows removed).
- Country population is **heavily right-skewed** (skewness ≈ 8.8) — a small number of
  countries hold enormous shares of the population while most are comparatively small.
- **India (1.45B) and China (1.41B)** alone account for **~35%** of the world's population,
  despite being just 2 of 217 countries.
- The **median** country population (~6.6M) is roughly **5.6x smaller** than the **mean**
  (~37M) — a classic signature of outlier-dominated data, not a "typical" distribution.
- On a log scale, the distribution is roughly **log-normal**, a shape commonly seen in
  quantities shaped by multiplicative growth (population, income, city size).
- **East Asia & Pacific** and **South Asia** are the two most populous World Bank regions,
  together accounting for roughly half of the global population.
- Population size doesn't map cleanly onto income group — some of the largest
  lower-middle-income countries (India, Nigeria, Pakistan) individually outweigh many
  high-income countries combined.

## Tools

`Python` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `Jupyter`

---
*Divyanshi Shukla — Data Science Intern, Prodigy InfoTech*
