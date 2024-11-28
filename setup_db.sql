CREATE TABLE USER
(
    discord_id   text PRIMARY KEY,
    nickname     text,
    adventname   text,
    shouldremind boolean
);

CREATE TABLE SERVER
(
    guild_id   text PRIMARY KEY,
    channel_id text,
    api_id     text,
    owner_id   text
);

CREATE TABLE SCOREBOARD
(
    api_id       text PRIMARY KEY,
    cookie_value text,
    owner_id     text,
    json_content text,
    last_refresh text
);

CREATE TABLE HINT
(
    guild_id text,
    day_id   text,
    puzzle1  text,
    puzzle2  text,
    PRIMARY KEY (guild_id, day_id)
);

CREATE TABLE EVENTDAY
(
    day         text PRIMARY KEY,
    year        text,
    title       text,
    description text,
    has_been_send boolean default FALSE,
    FOREIGN KEY (year) REFERENCES ADVENTTABLE (year),
    UNIQUE (day, year)
);


CREATE TABLE ADVENTTABLE
(
    year        text PRIMARY KEY,
    title       text,
    description text
);


