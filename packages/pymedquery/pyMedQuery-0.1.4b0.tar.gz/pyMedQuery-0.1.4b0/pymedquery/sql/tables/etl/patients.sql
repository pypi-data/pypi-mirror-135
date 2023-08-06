CREATE TABLE IF NOT EXISTS patient_table (
	patient_uid TEXT NOT NULL,
	age TEXT,
	gender TEXT,
	weight INTEGER,
	FOREIGN KEY (patient_uid) REFERENCES junction_img_table (patient_uid)
);
