# Data Quality Framework

Validation checks include:
- Primary-key uniqueness
- Core-field completeness
- Numeric non-negativity
- Severity range 1–5
- Funding received plausibility
- Consistent geographic keys

Run `python python/data_validation.py` after cleaning. The output is stored in `data/processed/data_quality_report.csv`.
