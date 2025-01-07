CREATE DATABASE IF NOT EXISTS weather_db;
use weather_db;

create table weather (
    id int auto_increment primary key,
    title varchar(255) not null,
    content text not null
);

INSERT INTO weather (title, content) VALUES ('Day 1', 'Sunny');
INSERT INTO weather (title, content) VALUES ('Day 2', 'Sunny');
INSERT INTO weather (title, content) VALUES ('Day 3', 'Windy');