CREATE TABLE countdowns (
    id SERIAL PRIMARY KEY,
    chanell_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL
);