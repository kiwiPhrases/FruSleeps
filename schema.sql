DROP TABLE IF EXISTS sleepTimes;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS parents;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE parents (
  munchkin TEXT NOT NULL,
  parent TEXT UNIQUE NOT NULL
  --FOREIGN key (munchkin) references user (username)
);

CREATE TABLE sleepTimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    munchkin TEXT NOT NULL,
    parent TEXT NOT NULL,
    sleepdate TEXT NOT NULL,
    sleeptime TEXT NOT NULL
    --FOREIGN KEY (parent) REFERENCES parents (parent)
);