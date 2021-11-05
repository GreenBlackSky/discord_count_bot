CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    author VARCHAR(200) NOT NULL,
    channel_id BIGINT NOT NULL,
    is_dm BOOLEAN NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    count INT NOT NULL,
    canceled BOOLEAN NOT NULL DEFAULT FALSE
);