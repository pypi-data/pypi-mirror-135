CREATE TABLE IF NOT EXISTS restricted.users (
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	user_id SERIAL PRIMARY KEY,
    access_token UUID,
	email TEXT NOT NULL UNIQUE,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	institution TEXT NOT NULL,
	password_hash TEXT NOT NULL
);
