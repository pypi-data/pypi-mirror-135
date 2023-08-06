/* The table contains mask image UID and other identifiers for extracting images
 and metainfo*/
CREATE TABLE IF NOT EXISTS mask_table (
	series_uid TEXT NOT NULL,
	mask_uid TEXT NOT NULL,
    model_id TEXT NOT NULL,
	PRIMARY KEY (mask_uid),
    CONSTRAINT fk_model_id
        FOREIGN KEY (model_id)
        REFERENCES junction_ml_table (model_id)
);
