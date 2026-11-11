from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/"data/processed"
checks=[]
def check(name,condition,detail): checks.append((name,bool(condition),detail))
needs=pd.read_csv(D/"needs_assessment_clean.csv"); response=pd.read_csv(D/"response_clean.csv"); funding=pd.read_csv(D/"funding_clean.csv")
check("Needs primary key",needs.need_id.is_unique,"need_id must be unique")
check("Response primary key",response.response_id.is_unique,"response_id must be unique")
check("Funding primary key",funding.funding_id.is_unique,"funding_id must be unique")
check("Needs numeric validity",(needs.people_in_need>=0).all() and needs.severity_index.between(1,5).all(),"need and severity ranges")
check("Response numeric validity",(response.people_reached>=0).all() and (response.intervention_count>=0).all(),"response measures")
check("Funding validity",(funding.requirements_usd>=0).all() and (funding.received_usd>=0).all() and (funding.received_usd<=funding.requirements_usd*1.10+0.01).all(),"funding measures")
check("Missing core fields",not any(df[[c for c in ["date","territory_id","province","sector"] if c in df]].isna().any().any() for df in [needs,response,funding]),"core dimensions")
report=pd.DataFrame(checks,columns=["check","passed","detail"]); report.to_csv(ROOT/"data/processed/data_quality_report.csv",index=False)
print(report.to_string(index=False)); raise SystemExit(1 if not report.passed.all() else 0)
