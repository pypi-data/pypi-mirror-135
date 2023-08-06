/* The series param table contains all the meta info on the 3D image used in various analyses and projects
 in CRAI. You can connect the metainfo the the 3D image by series UID
 
 TODO: insert averages for slice_spacing, slice_thickness and pixel_spacing
*/
CREATE TABLE IF NOT EXISTS image_metainfo_table (
	series_uid TEXT NOT NULL,
	series_time TIMESTAMP WITHOUT TIME ZONE,
	series_description TEXT,
	body_part_examined TEXT,
	slice_thickness FLOAT,
	pixel_spacing FLOAT,
	number_of_averages INTEGER,
	series_number INTEGER,
	patient_position TEXT,
	acquistion_duration FLOAT,
	slice_spacing FLOAT,
	protocol_name TEXT,
	imaged_nucleus TEXT,
	repition_time FLOAT,
	echo_time FLOAT,
	inversion_time FLOAT,
	imaging_frequency FLOAT,
	echo_number FLOAT,
	magnetic_field_strength FLOAT,
	phase_encoding_steps FLOAT,
	echo_train_length FLOAT,
	pct_sampling FLOAT,
	pct_phase_fov FLOAT,
	pixel_bandwidth FLOAT,
	flip_angle FLOAT,
	phase_encoding_direction FLOAT,
	diffusion_bvalue FLOAT,
	diffusion_grad_orient FLOAT,
    CONSTRAINT fk_series_uid
        FOREIGN KEY (series_uid)
        REFERENCES multimodal_image_table (series_uid)
);
