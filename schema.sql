CREATE TABLE Users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  password TEXT,
  role INTEGER
);

CREATE TABLE UserInventory (
  user_id INTEGER REFERENCES Users,
  inventory_id INTEGER REFERENCES Inventory
);

CREATE TABLE UserProductions (
  user_id INTEGER REFERENCES Users,
  production_id INTEGER REFERENCES Productions
);

CREATE TABLE UserReservations (
  user_id INTEGER REFERENCES Users,
  reservation_id INTEGER REFERENCES Reservations
);

CREATE TABLE Equipment (
  id SERIAL PRIMARY KEY,
  model TEXT,
  manufacturer_id INTEGER REFERENCES Manufacturers
);

CREATE TABLE Manufacturers (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE Inventory (
  id SERIAL PRIMARY KEY,
  model_id INTEGER REFERENCES Equipment
  serialnum TEXT
  available BOOLEAN
);

CREATE TABLE Productions (
  id SERIAL PRIMARY KEY,
  name TEXT,
  start TIMESTAMP,
  end TIMESTAMP
);

CREATE TABLE Reservations (
  id SERIAL PRIMARY KEY,
  production_id INTEGER REFERENCES Productions,
  inventory_id INTEGER REFERENCES Inventory
);