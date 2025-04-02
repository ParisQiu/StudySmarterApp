CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS study_rooms (
    room_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    capacity INTEGER CHECK (capacity > 0),
    creator_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    creator_id INTEGER NOT NULL REFERENCES users(id),
    room_id INTEGER REFERENCES study_rooms(room_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(post_id),
    creator_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS media (
    media_id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    post_id INTEGER REFERENCES posts(post_id),
    created_at TIMESTAMP DEFAULT NOW()
);
