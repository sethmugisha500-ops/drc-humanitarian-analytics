"""Generate a synthetic DRC humanitarian operations dataset.

Default scale is deliberately large enough to demonstrate senior-level ETL,
SQL and BI skills. Override row counts with environment variables for a fast
local test, e.g. NEEDS_ROWS=50000 RESPONSE_ROWS=30000 FUNDING_ROWS=15000.
"""
from pathlib import Path
import os
import numpy as np
import pandas as pd

SEED=int(os.getenv("SEED","2026")); rng=np.random.default_rng(SEED)
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data/raw"; RAW.mkdir(parents=True,exist_ok=True)
NEEDS_ROWS=int(os.getenv("NEEDS_ROWS","500000")); RESPONSE_ROWS=int(os.getenv("RESPONSE_ROWS","350000")); FUNDING_ROWS=int(os.getenv("FUNDING_ROWS","180000"))
START=pd.Timestamp("2024-01-01"); END=pd.Timestamp("2026-12-01")
MONTHS=pd.date_range(START,END,freq="MS")
PROVINCES=["Kinshasa","Kongo Central","Kwango","Kwilu","Mai-Ndombe","Kasaï","Kasaï-Central","Kasaï-Oriental","Lomami","Sankuru","Maniema","South Kivu","North Kivu","Ituri","Haut-Uele","Bas-Uele","Tshopo","Bas-Congo","Tanganyika","Haut-Lomami","Lualaba","Haut-Katanga","Nord-Ubangi","Sud-Ubangi","Mongala","Équateur"]
# Historical naming is intentionally retained only as a synthetic label; no official statistics are implied.
SECTORS=["Food Security","Health","WASH","Protection","Nutrition","Education","Shelter / NFI","Livelihoods"]
POP_GROUPS=["Children","Women","Men","Older Persons","Persons with Disabilities","IDPs","Returnees","Refugees","Host Communities"]
ORGS=["Humanitarian Partner A","Humanitarian Partner B","Humanitarian Partner C","Humanitarian Partner D","Humanitarian Partner E","Humanitarian Partner F","Humanitarian Partner G","Humanitarian Partner H","Humanitarian Partner I","Humanitarian Partner J"]
MODALITIES=["Cash","In-kind","Services","Kits","Community Outreach","Referral"]
# Familiar place names are included only to make the portfolio dashboard realistic; all measures remain synthetic.
SPECIAL={"North Kivu":["Beni","Goma","Lubero","Masisi","Rutshuru","Walikale"],"Ituri":["Djugu","Irumu","Mambasa","Mahagi","Aru"],"South Kivu":["Mwenga","Fizi","Uvira","Kabare","Kalehe"],"Tanganyika":["Kalemie","Nyunzu","Manono"],"Kinshasa":["Kinshasa"],"Haut-Uele":["Watsa","Dungu","Faradje"]}

def make_geo():
    rows=[]
    for p in PROVINCES:
        names=SPECIAL.get(p,[])
        names += [f"{p} Territory {i:02d}" for i in range(1,8)]
        for i,t in enumerate(names): rows.append((f"T{len(rows)+1:03d}",p,t))
    return pd.DataFrame(rows,columns=["territory_id","province","territory"])
geo=make_geo(); TERR=geo.territory_id.to_numpy(); weights=np.ones(len(TERR));
for i,r in geo.iterrows():
    if r.territory in {"Beni","Djugu","Irumu","Mwenga","Fizi","Lubero","Uvira","Mambasa","Kalemie"}: weights[i]=4
weights=weights/weights.sum()

def dates(n): return pd.Series(rng.choice(MONTHS.to_numpy(),n)).astype("datetime64[ns]")
def cat(vals,n,p=None): return rng.choice(vals,n,p=p)

def generate_needs(n):
    idx=rng.choice(len(geo),n,p=weights); g=geo.iloc[idx].reset_index(drop=True); sector=cat(SECTORS,n,[.23,.16,.15,.14,.11,.08,.08,.05]); pop=cat(POP_GROUPS,n)
    base=rng.gamma(2.2,1400,n); severity=np.clip(rng.normal(3.35,.9,n),1,5); displaced=np.maximum(0,(base*rng.uniform(.05,.8,n)).astype(int))
    return pd.DataFrame({"need_id":[f"N{i:07d}" for i in range(1,n+1)],"date":dates(n),"territory_id":g.territory_id.values,"province":g.province.values,"territory":g.territory.values,"sector":sector,"population_group":pop,"people_in_need":np.maximum(20,base.astype(int)),"severity_index":np.round(severity,2),"displaced_population":displaced,"assessment_status":cat(["Verified","Reviewed","Preliminary"],n,[.68,.25,.07])})

def generate_response(n):
    idx=rng.choice(len(geo),n,p=weights); g=geo.iloc[idx].reset_index(drop=True); sector=cat(SECTORS,n,[.22,.17,.15,.13,.11,.08,.08,.06]); need=np.maximum(10,rng.gamma(2.0,900,n)); coverage=np.clip(rng.beta(2.2,3.2,n),.02,.98); reached=np.minimum(need,(need*coverage).astype(int)+1)
    return pd.DataFrame({"response_id":[f"R{i:07d}" for i in range(1,n+1)],"date":dates(n),"territory_id":g.territory_id.values,"province":g.province.values,"territory":g.territory.values,"sector":sector,"organization":cat(ORGS,n),"modality":cat(MODALITIES,n),"people_reached":reached,"intervention_count":rng.integers(1,6,n),"response_cost_usd":np.round(rng.lognormal(7.2,.9,n),2)})

def generate_funding(n):
    idx=rng.choice(len(geo),n,p=weights); g=geo.iloc[idx].reset_index(drop=True); req=rng.lognormal(8.3,1.0,n)*100; rate=np.clip(rng.beta(4,3,n),.08,.92); rec=req*rate
    return pd.DataFrame({"funding_id":[f"F{i:07d}" for i in range(1,n+1)],"date":dates(n),"territory_id":g.territory_id.values,"province":g.province.values,"territory":g.territory.values,"sector":cat(SECTORS,n),"organization":cat(ORGS,n),"requirements_usd":np.round(req,2),"received_usd":np.round(rec,2),"funding_source":cat(["Bilateral","Multilateral","Private","Pooled Fund","Internal"],n)})

needs=generate_needs(NEEDS_ROWS); response=generate_response(RESPONSE_ROWS); funding=generate_funding(FUNDING_ROWS)
for name,df in [("needs_assessment",needs),("response",response),("funding",funding)]:
    df.to_csv(RAW/f"{name}.csv",index=False)
geo.to_csv(RAW/"geography.csv",index=False)
print(f"Generated {len(needs):,} needs, {len(response):,} response, {len(funding):,} funding rows and {len(geo):,} territories.")
