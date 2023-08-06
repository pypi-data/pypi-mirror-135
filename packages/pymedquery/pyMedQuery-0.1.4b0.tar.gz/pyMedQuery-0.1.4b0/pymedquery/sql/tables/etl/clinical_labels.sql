/* This table contains meta info on labels of cancer.*/
CREATE TABLE IF NOT EXISTS cancer_labels (
    time_of_diagnosis TIMESTAMP WITHOUT TIME ZONE,
	study_uid TEXT NOT NULL,
	series_uid TEXT NOT NULL,
    cancer BOOLEAN NOT NULL,
	cancer_type TEXT NOT NULL,
	masked BOOLEAN NOT NULL,
	departed BOOLEAN NOT NULL,
	diagnosis TEXT,
    stage TEXT,
    FOREIGN KEY (study_uid) REFERENCES study_table (study_uid),
	FOREIGN KEY(series_uid) REFERENCES multimodal_image_table (series_uid)
);
