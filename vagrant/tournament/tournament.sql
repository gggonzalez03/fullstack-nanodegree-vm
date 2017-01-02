-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CREATE DATABASE TOURNAMENT;

-- CONNECT TO DATABASE tournament

CREATE TABLE PLAYER(
    ID      SERIAL      NOT NULL,
    NAME    VARCHAR(20) NOT NULL,
    PRIMARY KEY(ID)
);

CREATE TABLE MATCH(
    ID      SERIAL                              NOT NULL,
    WINNER  INT         REFERENCES PLAYER(ID)   NOT NULL,
    LOSER   INT         REFERENCES PLAYER(ID)   NOT NULL,
    PRIMARY KEY(ID)
);


-- Returns wins and matches grouped by player ids
-- Note: column winner is a foreigh key of id in player table
CREATE VIEW STANDINGS_VIEW
AS SELECT * FROM (SELECT winner AS winnerid, COUNT(*) AS wins
FROM Match
GROUP BY winner) AS w
FULL JOIN
(SELECT loser AS loserid, COUNT(*) AS losses
FROM Match
GROUP BY loser) AS l
ON w.winnerid = l.loserid;
