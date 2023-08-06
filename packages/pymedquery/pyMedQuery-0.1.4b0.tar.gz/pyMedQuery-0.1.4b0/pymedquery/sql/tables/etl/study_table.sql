/* This table contains meta information on a full study of a patient. A study often inlcudes 
 several 3D images(series) and is done to monitor e.g. progression in pathology or recovery.
 The table is related to other tables about the doctor and station that was involved and used
 in the study.
 */
CREATE TABLE IF NOT EXISTS study_table (
	study_uid TEXT NOT NULL,
	time TIMESTAMP WITHOUT TIME ZONE,
	doctor_id INTEGER,
	station_id INTEGER,
	study_description TEXT,
	PRIMARY KEY (study_uid),
	FOREIGN KEY(doctor_id) REFERENCES doctor_table (id),
	FOREIGN KEY(station_id) REFERENCES scanning_station_table (id)
);
