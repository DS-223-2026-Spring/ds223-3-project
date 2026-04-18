CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    age_group VARCHAR(20),
    experience_level VARCHAR(20),
    personal_goal VARCHAR(50)
);

CREATE TABLE activities (
    activity_id SERIAL PRIMARY KEY,
    activity_type VARCHAR(50) NOT NULL
);

CREATE TABLE time_slots (
    slot_id SERIAL PRIMARY KEY,
    preferred_day VARCHAR(20),
    preferred_time VARCHAR(20)
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    activity_id INT REFERENCES activities(activity_id),
    slot_id INT REFERENCES time_slots(slot_id),
    booking_status VARCHAR(20)
);

INSERT INTO activities (activity_type) VALUES
('yoga'),
('dance'),
('music');
