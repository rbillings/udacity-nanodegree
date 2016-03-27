-- Create database "tournament" and connect to that database before creating tables, tip found at https://discussions.udacity.com/t/project-2-tips-and-hints/19689
\c vagrant

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

-- Create table for Players
CREATE TABLE players
(
    id   SERIAL PRIMARY KEY,
    name   VARCHAR(50),
    wins   INT,
    matches   INT
);

-- Create table for Matches
CREATE TABLE matches
(
    id   SERIAL PRIMARY KEY,
    winner   INT,
    loser   INT
);

-- View winners
CREATE VIEW winners AS
    SELECT players.name, players.wins
    FROM players
    ORDER BY players.wins DESC, players.matches ASC;
