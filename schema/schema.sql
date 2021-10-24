CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL UNIQUE CHECK(LENGTH(username) > 2),
  password TEXT NOT NULL,
  isAdmin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE manufacturers (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL CHECK(LENGTH(name) > 2)
);

CREATE TABLE productions (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL CHECK(LENGTH(name) > 2),
  starting DATE NOT NULL,
  ending DATE NOT NULL CHECK(ending >= starting)
);

CREATE TABLE equipment (
  id SERIAL PRIMARY KEY,
  model TEXT UNIQUE NOT NULL CHECK(LENGTH(model) > 2),
  manufacturer_id INTEGER REFERENCES manufacturers NOT NULL
);

CREATE TABLE inventory (
  id SERIAL PRIMARY KEY,
  model_id INTEGER REFERENCES equipment ON DELETE CASCADE NOT NULL,
  serialnum TEXT NOT NULL CHECK(LENGTH(serialnum) > 2)
);

CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  production_id INTEGER REFERENCES productions ON DELETE CASCADE NOT NULL,
  inventory_id INTEGER REFERENCES inventory ON DELETE CASCADE NOT NULL
);

CREATE TABLE userinventory (
  user_id INTEGER REFERENCES users ON DELETE CASCADE NOT NULL,
  inventory_id INTEGER REFERENCES inventory ON DELETE CASCADE NOT NULL
);

CREATE TABLE userequipment (
  user_id INTEGER REFERENCES users ON DELETE CASCADE NOT NULL,
  equipment_id INTEGER REFERENCES equipment ON DELETE CASCADE NOT NULL
);

CREATE TABLE userproductions (
  user_id INTEGER REFERENCES users ON DELETE CASCADE NOT NULL,
  production_id INTEGER REFERENCES productions ON DELETE CASCADE NOT NULL
);

CREATE TABLE userreservations (
  user_id INTEGER REFERENCES users ON DELETE CASCADE NOT NULL,
  reservation_id INTEGER REFERENCES reservations ON DELETE CASCADE NOT NULl
);

CREATE TABLE usermanufacturers (
  user_id INTEGER REFERENCES users ON DELETE CASCADE NOT NULL,
  manufacturer_id INTEGER REFERENCES manufacturers ON DELETE CASCADE NOT NULL
);