CREATE TABLE countdowns (
    id SERIAL PRIMARY KEY,
    chanell_id BIGINT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    countdown INT
);