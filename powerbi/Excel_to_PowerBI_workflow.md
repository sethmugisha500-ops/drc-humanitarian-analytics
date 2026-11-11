# Excel → Power BI workflow

1. Open `DRC_Humanitarian_Analytics.xlsx` and review KPI, province, sector and priority sheets.
2. In Power BI, import the cleaned CSVs from `data/processed/` or connect to MySQL.
3. Build dimensions and fact tables using the model in `PowerBI_build_guide.md`.
4. Add DAX measures from `DAX_measures.txt`.
5. Reproduce the executive layout from `screenshots/reference_executive_overview.png`, but never copy its illustrative numbers.
