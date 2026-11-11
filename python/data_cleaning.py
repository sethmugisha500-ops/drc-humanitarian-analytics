from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data/raw"; OUT=ROOT/"data/processed"; OUT.mkdir(parents=True,exist_ok=True)

def clean(path, date_cols, numeric_cols):
    df=pd.read_csv(path)
    for c in date_cols: df[c]=pd.to_datetime(df[c],errors="coerce")
    for c in numeric_cols: df[c]=pd.to_numeric(df[c],errors="coerce")
    df.columns=[c.strip().lower().replace(" ","_") for c in df.columns]
    return df
needs=clean(RAW/"needs_assessment.csv",["date"],["people_in_need","severity_index","displaced_population"])
response=clean(RAW/"response.csv",["date"],["people_reached","intervention_count","response_cost_usd"])
funding=clean(RAW/"funding.csv",["date"],["requirements_usd","received_usd"])
# Standardize text and clip impossible business values.
for df in [needs,response,funding]:
    for c in df.select_dtypes(include="object").columns: df[c]=df[c].astype(str).str.strip()
needs["severity_index"]=needs["severity_index"].clip(1,5)
needs["people_in_need"]=needs["people_in_need"].clip(lower=0)
needs["displaced_population"]=needs["displaced_population"].clip(lower=0)
response["people_reached"]=response["people_reached"].clip(lower=0)
response["intervention_count"]=response["intervention_count"].clip(lower=0)
funding["requirements_usd"]=funding["requirements_usd"].clip(lower=0)
funding["received_usd"]=funding["received_usd"].clip(lower=0)
funding["received_usd"]=np.minimum(funding["received_usd"],funding["requirements_usd"]*1.10)
for name,df in [("needs_assessment",needs),("response",response),("funding",funding)]: df.to_csv(OUT/f"{name}_clean.csv",index=False)
print("Cleaning complete:")
for n,df in [("needs",needs),("response",response),("funding",funding)]: print(f"  {n}: {len(df):,} rows")
