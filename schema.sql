DROP TABLE IF EXISTS sleepTimes;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE sleepTimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent INTEGER NOT NULL,
    sleepdate TEXT NOT NULL,
    sleeptime TEXT NOT NULL,
    FOREIGN KEY (parent) REFERENCES user (username)
);