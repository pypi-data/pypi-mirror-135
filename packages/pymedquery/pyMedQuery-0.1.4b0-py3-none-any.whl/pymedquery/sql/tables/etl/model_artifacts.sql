/* Model artifacts contains metainfo on the models that are developed in CRAI*/
CREATE TABLE IF NOT EXISTS model_artifacts (
	time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	model_id TEXT NOT NULL,
	model_version TEXT NOT NULL,
	project_owner TEXT NOT NULL,
    CONSTRAINT fk_model_id
        FOREIGN KEY (model_id)
        REFERENCES junction_ml_table (model_id)
);
