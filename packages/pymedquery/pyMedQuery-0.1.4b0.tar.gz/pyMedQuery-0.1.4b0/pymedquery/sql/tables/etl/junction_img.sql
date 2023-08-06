/* This table is meant to be a connection table for other tables and contains
 the most important identifier for the fetching data on the images.*/
CREATE TABLE IF NOT EXISTS junction_img_table (
	patient_uid TEXT NOT NULL,
	project_id TEXT NOT NULL,
	study_uid TEXT NOT NULL,
	PRIMARY KEY (patient_uid),
    FOREIGN KEY (study_uid) REFERENCES study_table (study_uid)
);
