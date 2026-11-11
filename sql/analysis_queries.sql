USE drc_humanitarian_analytics;
-- Executive KPIs
SELECT SUM(people_in_need) people_in_need FROM needs_assessment;
SELECT SUM(people_reached) people_reached FROM response;
SELECT ROUND((SELECT SUM(people_reached) FROM response)/(SELECT SUM(people_in_need) FROM needs_assessment)*100,2) coverage_pct;
SELECT SUM(requirements_usd) requirements_usd,SUM(received_usd) received_usd,SUM(requirements_usd-received_usd) funding_gap_usd FROM funding;
-- Top 10 high-need / low-coverage territories
WITH n AS (SELECT territory_id,territory,province,SUM(people_in_need) need FROM needs_assessment GROUP BY territory_id,territory,province), r AS (SELECT territory_id,SUM(people_reached) reached FROM response GROUP BY territory_id) SELECT n.territory,n.province,n.need,COALESCE(r.reached,0) reached,ROUND(COALESCE(r.reached,0)/NULLIF(n.need,0)*100,2) coverage_pct FROM n LEFT JOIN r USING(territory_id) ORDER BY n.need DESC,coverage_pct ASC LIMIT 10;
-- Funding gap by sector
SELECT sector,SUM(requirements_usd) requirements,SUM(received_usd) received,SUM(requirements_usd-received_usd) gap,ROUND(SUM(received_usd)/NULLIF(SUM(requirements_usd),0)*100,2) funding_coverage_pct FROM funding GROUP BY sector ORDER BY gap DESC;
-- Organizations: reach and cost efficiency
SELECT organization,SUM(people_reached) reached,SUM(response_cost_usd) cost,ROUND(SUM(response_cost_usd)/NULLIF(SUM(people_reached),0),2) cost_per_person FROM response GROUP BY organization ORDER BY cost_per_person;
