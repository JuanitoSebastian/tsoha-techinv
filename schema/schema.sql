CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT,
  isAdmin BOOLEAN
);

CREATE TABLE manufacturers (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE productions (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  starting DATE,
  ending DATE
);

CREATE TABLE equipment (
  id SERIAL PRIMARY KEY,
  model TEXT UNIQUE,
  manufacturer_id INTEGER REFERENCES manufacturers,
  visible BOOLEAN
);

CREATE TABLE inventory (
  id SERIAL PRIMARY KEY,
  model_id INTEGER REFERENCES equipment ON DELETE CASCADE,
  serialnum TEXT,
  available BOOLEAN
);

CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  production_id INTEGER REFERENCES productions ON DELETE CASCADE,
  inventory_id INTEGER REFERENCES inventory ON DELETE CASCADE
);

CREATE TABLE userinventory (
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  inventory_id INTEGER REFERENCES inventory ON DELETE CASCADE
);

CREATE TABLE userequipment (
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  equipment_id INTEGER REFERENCES equipment ON DELETE CASCADE
);

CREATE TABLE userproductions (
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  production_id INTEGER REFERENCES productions ON DELETE CASCADE
);

CREATE TABLE userreservations (
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  reservation_id INTEGER REFERENCES reservations ON DELETE CASCADE
);

CREATE TABLE usermanufacturers (
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  manufacturer_id INTEGER REFERENCES manufacturers ON DELETE CASCADE
)