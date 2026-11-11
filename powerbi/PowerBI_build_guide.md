# Power BI Build Guide

## Model
Use a star schema:
- FactNeeds
- FactResponse
- FactFunding
- DimGeography
- DimDate
- DimSector
- DimOrganization

Relate each fact to the dimensions through surrogate/business keys. Avoid direct many-to-many fact relationships.

## Executive Overview
Use the supplied reference screenshot as the visual direction, but populate every value from this project’s synthetic data. Recommended visuals:
1. KPI cards: People in Need, People Reached, Coverage %, Funding Received, Funding Gap, Active Interventions, Displaced Population.
2. Filled map: People in Need by Province.
3. Clustered bar: People in Need vs People Reached by Province.
4. Matrix: Top 10 territories by need and severity.
5. Donut: People in Need by Sector.
6. Bar: Coverage % by Sector.
7. Donut: Funding Received by Sector.
8. Column chart: Requirements vs Received.
9. Text boxes: Key Insights / Priority Areas / Recommendations.

## Navigation pages
Executive Overview | Geographic Analysis | Sector Analysis | Response & Coverage | Funding & Efficiency | Priority Index | Detailed Analysis | Data Dictionary

## Senior-level features
Add drill-through from Province to Territory, tooltip pages, dynamic titles, conditional formatting, bookmarks, synced slicers, and a last-refresh card.
