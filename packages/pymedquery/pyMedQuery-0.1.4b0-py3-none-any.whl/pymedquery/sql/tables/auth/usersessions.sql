CREATE TABLE IF NOT EXISTS restricted.usersessions (
	created_at TIMESTAMP WITHOUT TIME ZONE,
	last_used_at TIMESTAMP WITHOUT TIME ZONE,
	session_id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL,
	FOREIGN KEY(user_id) REFERENCES restricted.users (user_id)
);
