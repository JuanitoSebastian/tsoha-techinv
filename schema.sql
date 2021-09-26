CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  password TEXT,
  role INTEGER
);

CREATE TABLE manufacturers (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE productions (
  id SERIAL PRIMARY KEY,
  name TEXT,
  starting TIMESTAMP,
  ending TIMESTAMP
);

CREATE TABLE equipment (
  id SERIAL PRIMARY KEY,
  model TEXT,
  manufacturer_id INTEGER REFERENCES manufacturers,
  visible BOOLEAN
);

CREATE TABLE inventory (
  id SERIAL PRIMARY KEY,
  model_id INTEGER REFERENCES equipment,
  serialnum TEXT,
  available BOOLEAN
);

CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  production_id INTEGER REFERENCES productions,
  inventory_id INTEGER REFERENCES inventory
);

CREATE TABLE userinventory (
  user_id INTEGER REFERENCES users,
  inventory_id INTEGER REFERENCES inventory
);

CREATE TABLE userproductions (
  user_id INTEGER REFERENCES users,
  production_id INTEGER REFERENCES productions
);

CREATE TABLE userreservations (
  user_id INTEGER REFERENCES users,
  reservation_id INTEGER REFERENCES reservations
);