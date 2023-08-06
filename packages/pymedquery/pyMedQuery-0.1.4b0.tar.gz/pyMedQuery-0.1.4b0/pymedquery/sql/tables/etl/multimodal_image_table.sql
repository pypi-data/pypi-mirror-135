/* The multimodal_image_table contains the relations for the medical images where series_uid
 is the uniques pseudo anonymised identifier for a 3D medical image.
 */
CREATE TABLE IF NOT EXISTS multimodal_image_table (
	series_uid TEXT NOT NULL,
	affine_uid TEXT NOT NULL,
	patient_uid TEXT NOT NULL,
	modality TEXT,
	PRIMARY KEY (series_uid)
);
