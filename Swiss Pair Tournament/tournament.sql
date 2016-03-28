-- Create database "tournament" and connect to that database before creating tables, tip found at https://discussions.udacity.com/t/project-2-tips-and-hints/19689
\c vagrant

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

-- Create table for Players
CREATE TABLE players
(
    id   SERIAL PRIMARY KEY,
    name   VARCHAR(50)
);

-- Create table for Matches
CREATE TABLE matches
(
    id   SERIAL PRIMARY KEY,
    winner   INT,
    loser   INT
);

-- Create View standings_list
CREATE VIEW standings_list as
SELECT players.id, players.name, count(matches.winner) as wins,
(select count(*) from matches where players.id = matches.winner or players.id = matches.loser) as matches
from players left join matches
on players.id=matches.winner
group by players.id
order by wins DESC;
