/*This table contains IDs on preprocessed data*/    
CREATE TABLE IF NOT EXISTS preproc_data_table (
    time_of_upload TIMESTAMP WITHOUT TIME ZONE,
    data_id TEXT NOT NULL,
    model_id TEXT,
    project_id TEXT,
    PRIMARY KEY (data_id),
    FOREIGN KEY (model_id) REFERENCES junction_ml_table (model_id)
);
