from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# DRC HUMANITARIAN ANALYTICS
# Senior Analytical Data Mart
# Grain: Month + Province + Territory + Sector
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUT_DIR = DATA_DIR / "analytics"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. LOAD CLEAN DATA
# ============================================================

N = pd.read_csv(DATA_DIR / "needs_assessment_clean.csv")
R = pd.read_csv(DATA_DIR / "response_clean.csv")
F = pd.read_csv(DATA_DIR / "funding_clean.csv")


# ============================================================
# 2. STANDARDIZE DATES
# ============================================================

for df in [N, R, F]:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["year"] = df["date"].dt.year

    df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)

    df["month"] = df["date"].dt.to_period("M").astype(str)


# ============================================================
# 3. COMMON ANALYTICAL GRAIN
#
# Month + Province + Territory + Sector
# ============================================================

GRAIN = [
    "month",
    "year",
    "quarter",
    "province",
    "territory",
    "sector",
]


# ============================================================
# 4. NEEDS
# ============================================================

needs = (
    N.groupby(GRAIN, as_index=False)
    .agg(
        people_in_need=("people_in_need", "sum"),
        avg_severity=("severity_index", "mean"),
        displaced_population=("displaced_population", "sum"),
    )
)


# ============================================================
# 5. RESPONSE
# ============================================================

resp = (
    R.groupby(GRAIN, as_index=False)
    .agg(
        people_reached=("people_reached", "sum"),
        active_interventions=("intervention_count", "sum"),
        response_cost_usd=("response_cost_usd", "sum"),
    )
)


# ============================================================
# 6. FUNDING
# ============================================================

fund = (
    F.groupby(GRAIN, as_index=False)
    .agg(
        requirements_usd=("requirements_usd", "sum"),
        received_usd=("received_usd", "sum"),
    )
)


# ============================================================
# 7. BUILD ANALYTICAL DATA MART
# ============================================================

a = (
    needs
    .merge(resp, on=GRAIN, how="outer")
    .merge(fund, on=GRAIN, how="outer")
)


numeric_columns = [
    "people_in_need",
    "avg_severity",
    "displaced_population",
    "people_reached",
    "active_interventions",
    "response_cost_usd",
    "requirements_usd",
    "received_usd",
]

for col in numeric_columns:
    a[col] = a[col].fillna(0)


# ============================================================
# 8. RESPONSE KPIs
# ============================================================

a["coverage_pct"] = np.where(
    a["people_in_need"] > 0,
    a["people_reached"] / a["people_in_need"] * 100,
    0,
)

a["coverage_gap_pct"] = (100 - a["coverage_pct"]).clip(lower=0)


# ============================================================
# 9. FUNDING KPIs
# ============================================================

a["funding_gap_usd"] = (
    a["requirements_usd"] - a["received_usd"]
).clip(lower=0)


a["funding_coverage_pct"] = np.where(
    a["requirements_usd"] > 0,
    a["received_usd"] / a["requirements_usd"] * 100,
    0,
)


# ============================================================
# 10. RESPONSE EFFICIENCY
# ============================================================

a["cost_per_person_reached_usd"] = np.where(
    a["people_reached"] > 0,
    a["response_cost_usd"] / a["people_reached"],
    0,
)


# ============================================================
# 11. PRIORITY INDEX
#
# Components:
#   45% Need Pressure
#   25% Severity
#   20% Coverage Gap
#   10% Funding Gap
#
# Each component normalized 0-100.
# ============================================================

def minmax(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0.0, index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


a["need_pressure"] = minmax(a["people_in_need"])

a["severity_pressure"] = (
    a["avg_severity"] / 5 * 100
).clip(0, 100)

a["coverage_gap_pressure"] = (
    100 - minmax(a["coverage_pct"])
).clip(0, 100)

a["funding_gap_pressure"] = minmax(
    a["funding_gap_usd"]
)


a["priority_index"] = (
    0.45 * a["need_pressure"]
    + 0.25 * a["severity_pressure"]
    + 0.20 * a["coverage_gap_pressure"]
    + 0.10 * a["funding_gap_pressure"]
).round(1)


# ============================================================
# 12. PRIORITY CATEGORY
# ============================================================

a["priority_category"] = pd.cut(
    a["priority_index"],
    bins=[-np.inf, 25, 50, 75, np.inf],
    labels=[
        "Low",
        "Moderate",
        "High",
        "Critical",
    ],
)


# ============================================================
# 13. DATA QUALITY FLAGS
# ============================================================

a["response_exceeds_need"] = (
    a["people_reached"] > a["people_in_need"]
)

a["funding_exceeds_requirement"] = (
    a["received_usd"] > a["requirements_usd"]
)


# ============================================================
# 14. SAVE MASTER ANALYTICAL DATASET
# ============================================================

a = a.sort_values(
    ["priority_index", "month"],
    ascending=[False, True],
)

a.to_csv(
    OUT_DIR / "humanitarian_analytical_mart.csv",
    index=False,
)


# ============================================================
# 15. PRIORITY INDEX EXTRACT
# ============================================================

priority_columns = [
    "month",
    "year",
    "quarter",
    "province",
    "territory",
    "sector",
    "people_in_need",
    "avg_severity",
    "displaced_population",
    "people_reached",
    "active_interventions",
    "response_cost_usd",
    "requirements_usd",
    "received_usd",
    "coverage_pct",
    "coverage_gap_pct",
    "funding_gap_usd",
    "funding_coverage_pct",
    "cost_per_person_reached_usd",
    "need_pressure",
    "severity_pressure",
    "coverage_gap_pressure",
    "funding_gap_pressure",
    "priority_index",
    "priority_category",
    "response_exceeds_need",
    "funding_exceeds_requirement",
]

a[priority_columns].to_csv(
    OUT_DIR / "priority_index.csv",
    index=False,
)


# ============================================================
# 16. PROVINCE SUMMARY
# ============================================================

province_summary = (
    a.groupby("province", as_index=False)
    .agg(
        people_in_need=("people_in_need", "sum"),
        people_reached=("people_reached", "sum"),
        displaced_population=("displaced_population", "sum"),
        funding_requirements_usd=("requirements_usd", "sum"),
        funding_received_usd=("received_usd", "sum"),
        funding_gap_usd=("funding_gap_usd", "sum"),
        response_cost_usd=("response_cost_usd", "sum"),
        active_interventions=("active_interventions", "sum"),
        avg_severity=("avg_severity", "mean"),
    )
)


province_summary["coverage_pct"] = np.where(
    province_summary["people_in_need"] > 0,
    province_summary["people_reached"]
    / province_summary["people_in_need"]
    * 100,
    0,
)


province_summary["funding_coverage_pct"] = np.where(
    province_summary["funding_requirements_usd"] > 0,
    province_summary["funding_received_usd"]
    / province_summary["funding_requirements_usd"]
    * 100,
    0,
)


province_summary["cost_per_person_reached_usd"] = np.where(
    province_summary["people_reached"] > 0,
    province_summary["response_cost_usd"]
    / province_summary["people_reached"],
    0,
)


province_summary.to_csv(
    OUT_DIR / "province_summary.csv",
    index=False,
)


# ============================================================
# 17. SECTOR SUMMARY
# ============================================================

sector_summary = (
    a.groupby("sector", as_index=False)
    .agg(
        people_in_need=("people_in_need", "sum"),
        people_reached=("people_reached", "sum"),
        requirements_usd=("requirements_usd", "sum"),
        received_usd=("received_usd", "sum"),
        funding_gap_usd=("funding_gap_usd", "sum"),
        response_cost_usd=("response_cost_usd", "sum"),
        active_interventions=("active_interventions", "sum"),
        avg_severity=("avg_severity", "mean"),
    )
)


sector_summary["coverage_pct"] = np.where(
    sector_summary["people_in_need"] > 0,
    sector_summary["people_reached"]
    / sector_summary["people_in_need"]
    * 100,
    0,
)


sector_summary["funding_coverage_pct"] = np.where(
    sector_summary["requirements_usd"] > 0,
    sector_summary["received_usd"]
    / sector_summary["requirements_usd"]
    * 100,
    0,
)


sector_summary["cost_per_person_reached_usd"] = np.where(
    sector_summary["people_reached"] > 0,
    sector_summary["response_cost_usd"]
    / sector_summary["people_reached"],
    0,
)


sector_summary.to_csv(
    OUT_DIR / "sector_summary.csv",
    index=False,
)


# ============================================================
# 18. MONTHLY EXECUTIVE TREND
# ============================================================

monthly_summary = (
    a.groupby(
        ["month", "year", "quarter"],
        as_index=False,
    )
    .agg(
        people_in_need=("people_in_need", "sum"),
        people_reached=("people_reached", "sum"),
        displaced_population=("displaced_population", "sum"),
        funding_requirements_usd=("requirements_usd", "sum"),
        funding_received_usd=("received_usd", "sum"),
        funding_gap_usd=("funding_gap_usd", "sum"),
        response_cost_usd=("response_cost_usd", "sum"),
        active_interventions=("active_interventions", "sum"),
        avg_severity=("avg_severity", "mean"),
    )
)


monthly_summary["coverage_pct"] = np.where(
    monthly_summary["people_in_need"] > 0,
    monthly_summary["people_reached"]
    / monthly_summary["people_in_need"]
    * 100,
    0,
)


monthly_summary["funding_coverage_pct"] = np.where(
    monthly_summary["funding_requirements_usd"] > 0,
    monthly_summary["funding_received_usd"]
    / monthly_summary["funding_requirements_usd"]
    * 100,
    0,
)


monthly_summary.to_csv(
    OUT_DIR / "monthly_summary.csv",
    index=False,
)


# ============================================================
# 19. TOP PRIORITY AREAS
# ============================================================

top_priority = (
    a.groupby(
        ["province", "territory", "sector"],
        as_index=False,
    )
    .agg(
        people_in_need=("people_in_need", "sum"),
        people_reached=("people_reached", "sum"),
        avg_severity=("avg_severity", "mean"),
        funding_gap_usd=("funding_gap_usd", "sum"),
        coverage_pct=("coverage_pct", "mean"),
        priority_index=("priority_index", "mean"),
    )
    .sort_values(
        "priority_index",
        ascending=False,
    )
    .head(100)
)


top_priority.to_csv(
    OUT_DIR / "top_100_priority_areas.csv",
    index=False,
)


# ============================================================
# 20. FINAL MESSAGE
# ============================================================

print()
print("============================================================")
print("DRC HUMANITARIAN ANALYTICS - ANALYSIS COMPLETE")
print("============================================================")
print(f"Analytical mart rows: {len(a):,}")
print()
print("Files created:")
print("  humanitarian_analytical_mart.csv")
print("  priority_index.csv")
print("  province_summary.csv")
print("  sector_summary.csv")
print("  monthly_summary.csv")
print("  top_100_priority_areas.csv")
print()
print("Analytical grain:")
print("  Month + Province + Territory + Sector")
print()
print("Priority methodology:")
print("  45% Need Pressure")
print("  25% Severity")
print("  20% Coverage Gap")
print("  10% Funding Gap")
print("============================================================")