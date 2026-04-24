DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS user_segments CASCADE;
DROP TABLE IF EXISTS segments CASCADE;
DROP TABLE IF EXISTS quiz_responses CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS studios CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    age INT CHECK (age BETWEEN 10 AND 100),
    gender VARCHAR(20),
    district VARCHAR(50),
    data_source VARCHAR(20) DEFAULT 'real',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_responses (
    response_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    experience_level VARCHAR(20) NOT NULL,
    group_preference VARCHAR(20) NOT NULL,
    energy_preference VARCHAR(30) NOT NULL,
    structure_preference VARCHAR(20) NOT NULL,
    goal VARCHAR(50) NOT NULL,
    budget_max_amd INT,
    preferred_days TEXT,
    preferred_time VARCHAR(20),
    max_travel_km VARCHAR(20),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE studios (
    studio_id INT PRIMARY KEY,
    studio_name VARCHAR(255) NOT NULL,
    district VARCHAR(50),
    address VARCHAR(255),
    instagram VARCHAR(100),
    price_tier VARCHAR(20),
    studio_type VARCHAR(50)
);

CREATE TABLE classes (
    class_id INT PRIMARY KEY,
    studio_id INT NOT NULL REFERENCES studios(studio_id) ON DELETE CASCADE,
    studio_name VARCHAR(255),
    activity_type VARCHAR(50) NOT NULL,
    style VARCHAR(100) NOT NULL,
    day VARCHAR(100),
    time VARCHAR(20),
    duration_min INT,
    price_per_session_amd INT,
    price_monthly_amd INT,
    experience_required VARCHAR(20),
    group_or_private VARCHAR(20),
    energy_level VARCHAR(20),
    structure_level VARCHAR(20),
    district VARCHAR(50)
);

CREATE TABLE segments (
    segment_id SERIAL PRIMARY KEY,
    segment_name VARCHAR(100) NOT NULL,
    description TEXT,
    size INT DEFAULT 0,
    booking_likelihood FLOAT
);

CREATE TABLE user_segments (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    segment_id INT REFERENCES segments(segment_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, segment_id)
);

CREATE TABLE recommendations (
    rec_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(class_id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    rank INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_classes_studio ON classes(studio_id);
CREATE INDEX idx_classes_activity ON classes(activity_type);
CREATE INDEX idx_recs_user ON recommendations(user_id);
CREATE INDEX idx_quiz_user ON quiz_responses(user_id);
