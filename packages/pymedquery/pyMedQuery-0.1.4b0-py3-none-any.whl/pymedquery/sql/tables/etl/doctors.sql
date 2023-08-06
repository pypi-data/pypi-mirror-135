/* This table contains the meta info on the radiologist that
 was involved in taking the 3D image
 */
CREATE TABLE IF NOT EXISTS doctor_table (
	id SERIAL PRIMARY KEY,
	physician_title TEXT NOT NULL,
	doctor_name TEXT NOT NULL
);
