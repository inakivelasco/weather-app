CREATE DATABASE notes_db;
use notes_db;

CREATE TABLE notes (
    id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO notes (title, content) VALUES ('Note 1', 'Content of note 1');
INSERT INTO notes (title, content) VALUES ('Note 2', 'Content of note 2');
INSERT INTO notes (title, content) VALUES ('Note 3', 'Content of note 3');