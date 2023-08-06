/* This table contains the relations needed to extract predicted masks and 
 respective meta info on the raw images*/
CREATE TABLE IF NOT EXISTS mask_predicted_table (
    time_of_prediction TIMESTAMP WITHOUT TIME ZONE,
    pmask_uid TEXT NOT NULL,
    mask_uid TEXT NOT NULL,
    model_id TEXT NOT NULL,
    PRIMARY KEY (pmask_uid),
    CONSTRAINT fk_mask_uid
        FOREIGN KEY (mask_uid)
        REFERENCES mask_table (mask_uid)
);
