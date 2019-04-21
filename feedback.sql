CREATE TABLE region
(
  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
  name varchar(100)
);
INSERT INTO region (name) VALUES ('Краснодарский край');
INSERT INTO region (name) VALUES ('Ростовская область');
INSERT INTO region (name) VALUES ('Ставропольский край');


CREATE TABLE city
(
  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
  region INTEGER REFERENCES region(id),
  name varchar(50)
);
INSERT INTO city (region,name) VALUES (1,'Краснодар');
INSERT INTO city (region,name) VALUES (1,'Кропоткин');
INSERT INTO city (region,name) VALUES (1,'Славянск');
INSERT INTO city (region,name) VALUES (2,'Ростов');
INSERT INTO city (region,name) VALUES (2,'Шахты');
INSERT INTO city (region,name) VALUES (2,'Батайск');
INSERT INTO city (region,name) VALUES (3,'Ставрополь');
INSERT INTO city (region,name) VALUES (3,'Пятигорск');
INSERT INTO city (region,name) VALUES (3,'Кисловодск');

CREATE TABLE feedback
(
  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
  lastname varchar(100) NOT NULL,
  firstname varchar(50) NOT NULL,
  middlename varchar(50) DEFAULT (''),
  region INTEGER REFERENCES region(id),
  city INTEGER REFERENCES city(id),
  phone VARCHAR(30) DEFAULT(''),
  email VARCHAR(50) DEFAULT(''),
  comment TEXT
);