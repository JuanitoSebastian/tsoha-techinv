CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  password TEXT,
  role INTEGER
);

CREATE TABLE equipment (
  id SERIAL PRIMARY KEY,
  model TEXT,
  manufacturer_id INTEGER REFERENCES manufacturers
);

CREATE TABLE manufacturers (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE inventory (
  id SERIAL PRIMARY KEY,
  model_id INTEGER REF
)
