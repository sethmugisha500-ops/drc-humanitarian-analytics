USE drc_humanitarian_analytics;
CREATE OR REPLACE VIEW vw_province_performance AS
SELECT n.province, SUM(n.people_in_need) people_in_need, COALESCE(r.people_reached,0) people_reached, COALESCE(f.requirements_usd,0) requirements_usd, COALESCE(f.received_usd,0) received_usd, ROUND(COALESCE(r.people_reached,0)/NULLIF(SUM(n.people_in_need),0)*100,2) coverage_pct, ROUND(COALESCE(f.received_usd,0)/NULLIF(f.requirements_usd,0)*100,2) funding_coverage_pct
FROM needs_assessment n LEFT JOIN (SELECT province,SUM(people_reached) people_reached FROM response GROUP BY province) r USING(province)
LEFT JOIN (SELECT province,SUM(requirements_usd) requirements_usd,SUM(received_usd) received_usd FROM funding GROUP BY province) f USING(province) GROUP BY n.province,r.people_reached,f.requirements_usd,f.received_usd;
CREATE OR REPLACE VIEW vw_sector_performance AS
SELECT n.sector,SUM(n.people_in_need) people_in_need,COALESCE(r.people_reached,0) people_reached,COALESCE(f.requirements_usd,0) requirements_usd,COALESCE(f.received_usd,0) received_usd,ROUND(COALESCE(r.people_reached,0)/NULLIF(SUM(n.people_in_need),0)*100,2) coverage_pct FROM needs_assessment n
LEFT JOIN (SELECT sector,SUM(people_reached) people_reached FROM response GROUP BY sector) r USING(sector)
LEFT JOIN (SELECT sector,SUM(requirements_usd) requirements_usd,SUM(received_usd) received_usd FROM funding GROUP BY sector) f USING(sector)
GROUP BY n.sector,r.people_reached,f.requirements_usd,f.received_usd;
