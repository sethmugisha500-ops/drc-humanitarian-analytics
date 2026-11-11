# 🇨🇩 DRC Humanitarian Operations Analytics

**Senior Data Analytics & Business Intelligence Portfolio Project**

> An end-to-end synthetic humanitarian analytics platform designed to demonstrate how Python, Excel, SQL/MySQL and Power BI can support evidence-based operational decisions in the Democratic Republic of Congo.

## ⚠️ Synthetic-data notice
All records, funding values, population figures, organizations and indicators are simulated. They are **not official DRC humanitarian statistics** and must not be used for operational decision-making.

## Business questions
- Where are humanitarian needs concentrated?
- Which provinces and territories have high need but low response coverage?
- Which sectors have the largest funding gaps?
- How does response coverage vary geographically?
- Which interventions/organizations show better cost efficiency?
- Where should managers investigate priority gaps?

## End-to-end architecture
```text
Synthetic Data → Python ETL & Validation → Excel → MySQL/SQL → Power BI/DAX → Executive Decision Support
```

## Technology stack
Python • Pandas • NumPy • Excel • SQL • MySQL 8 • Power BI • DAX • Data Modelling • ETL/ELT • Data Quality • Git/GitHub

## Project structure
```text
drc-humanitarian-analytics/
├── data/raw/                 # Generated source CSVs
├── data/processed/           # Cleaned + analytical extracts
├── python/                   # Generation, cleaning, validation, analysis
├── sql/                      # Schema, loading, views, analysis queries
├── powerbi/                  # DAX and report construction guide
├── documentation/            # Methodology, KPIs, quality, dictionary, insights
├── screenshots/              # Dashboard reference / final screenshots
├── requirements.txt
└── README.md
```

## Run locally
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python python/data_generation.py
python python/data_cleaning.py
python python/data_validation.py
python python/analysis.py
```

For a quick test:
```bash
NEEDS_ROWS=50000 RESPONSE_ROWS=30000 FUNDING_ROWS=15000 python python/data_generation.py
```

## Excel deliverable
The recommended workbook contains: README, data dictionary, quality checks, KPI calculations, province/sector summaries, priority analysis and an executive management sheet. Raw CSVs remain the source layer so Excel is not overloaded unnecessarily.

## Power BI deliverable
Build the report from the processed/analytics CSVs or MySQL. The intended report pages are:
1. Executive Overview
2. Geographic Analysis
3. Sector Analysis
4. Response & Coverage
5. Funding & Efficiency
6. Priority Index
7. Detailed Analysis
8. Data Dictionary & Methodology

The executive page should follow the supplied reference layout while using this project's own calculated values.

## Portfolio positioning
Suggested title:
**DRC Humanitarian Operations Analytics — End-to-End Data Analytics & Business Intelligence Project**

Suggested LinkedIn description:
> Built an end-to-end synthetic humanitarian analytics platform for the DRC using Python, Excel, SQL/MySQL and Power BI. Designed a star-schema analytical model, implemented data-quality validation, developed executive KPIs and a humanitarian priority index, and translated needs, response coverage and funding gaps into decision-oriented insights.

## Important ethical note
The project demonstrates technical and analytical capability. It does not claim access to confidential beneficiary data, official humanitarian datasets, or real organizational performance information.
