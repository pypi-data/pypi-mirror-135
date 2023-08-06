/*
This is a defualt query for extracting SERIES UID and MASK UID. The query is meant to be used 
by beginner user, users that dont have the need for advanced queries and users that don't
want to learn SQL.

The query is designed to fetch all images from a certain project which is why
the project_id variable is formatted into the query.

parameters
--------------
project_id : str
    This is user defined variable that will filter patientIDs on a projectID.


what will be returned from the query is a view that has to be converted to a dict
in python. 

Columns:
patient_uid | series_uid | mask_id |

*/
WITH subq1 AS (
        SELECT patient_uid FROM junction_img_table
        WHERE study_uid LIKE '{project_id}'
        LIMIT 300 
    ), 

    subq2 AS (
        SELECT a.patient_uid, b.series_uid FROM subq1 a
        LEFT JOIN multimodal_image_table b 
        ON a.patient_uid=b.patient_uid
    ),
    
    subq3 AS (
        SELECT a.*, b.mask_uid FROM  subq2 a
        LEFT JOIN mask_table b
        ON a.series_uid=b.series_uid
    )

    SELECT * FROM subq3 WHERE mask_uid IS NOT NULL
