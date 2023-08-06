CREATE TABLE IF NOT EXISTS restricted.userverification (
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	email TEXT PRIMARY KEY,
	created_by INTEGER,
    bearer_toke BOOLEAN,
	FOREIGN KEY(created_by) REFERENCES restricted.users (user_id)
);
