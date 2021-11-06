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
CREATE TABLE general_errors (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    method VARCHAR(200) NOT NULL,
    error_info VARCHAR(2000) NOT NULL,
    traceback VARCHAR(2000) NOT NULL
);
CREATE TABLE command_errors (
    id SERIAL PRIMARY KEY,
    command VARCHAR(200) NOT NULL,
    author_name VARCHAR(200) NOT NULL,
    author_id BIGINT NOT NULL,
    channel_id BIGINT NOT NULL,
    is_dm BOOLEAN NOT NULL,
    time TIMESTAMP NOT NULL,
    traceback VARCHAR(2000) NOT NULL
);