USE drc_humanitarian_analytics;
-- Adjust LOCAL INFILE permissions if required by your MySQL installation.
LOAD DATA LOCAL INFILE 'PROJECT_PATH/data/raw/geography.csv' INTO TABLE geography FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'PROJECT_PATH/data/processed/needs_assessment_clean.csv' INTO TABLE needs_assessment FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'PROJECT_PATH/data/processed/response_clean.csv' INTO TABLE response FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'PROJECT_PATH/data/processed/funding_clean.csv' INTO TABLE funding FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
