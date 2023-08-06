/*This table contains the adjusted predicted masks*/
CREATE TABLE IF NOT EXISTS mask_adjusted_table (
    time_of_adjustment TIMESTAMP WITHOUT TIME ZONE,
    amask_uid TEXT NOT NULL,
    pmask_uid TEXT NOT NULL,
    corrector_id TEXT NOT NULL,
    PRIMARY KEY (amask_uid),
    FOREIGN KEY (pmask_uid) REFERENCES mask_predicted_table (pmask_uid) 
);
