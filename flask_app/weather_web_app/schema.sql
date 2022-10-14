DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS user_locations;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NULL,
    phone INTEGER NULL,
    user_addr TEXT NULL,
    user_latitude FLOAT(8) NOT NULL,
    user_longitude FLOAT(8) NOT NULL,
    user_office TEXT NOT NULL, 
    user_gridx TEXT NOT NULL,
    user_gridy TEXT NOT NULL
);

CREATE TABLE locations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_address TEXT NOT NULL,
  latitude FLOAT(8) NOT NULL,
  longitude FLOAT(8) NOT NULL,
  office TEXT NOT NULL,
  gridx INT NOT NULL, 
  gridy INT NOT NULL
);

CREATE TABLE user_locations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_id INTEGER NOT NULL,
  mapper_id INTEGER NOT NULL, 
  FOREIGN KEY (location_id) REFERENCES saved_locations (id),
  FOREIGN KEY (mapper_id) REFERENCES user (id)
)