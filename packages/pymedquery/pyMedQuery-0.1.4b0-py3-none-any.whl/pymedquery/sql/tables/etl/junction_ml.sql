/* This table contains the most important identifiers for fetching data on
 machine learning projects.*/
CREATE TABLE IF NOT EXISTS junction_ml_table (
	model_id TEXT NOT NULL,
	project_id TEXT NOT NULL,
	PRIMARY KEY (model_id)
);
