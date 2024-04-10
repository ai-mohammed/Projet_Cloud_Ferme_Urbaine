CREATE TABLE IF NOT EXISTS Sensors (
    ID INTEGER PRIMARY KEY,
    Provider VARCHAR(255),
    Location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Plants (
    ID INTEGER PRIMARY KEY,
    Species VARCHAR(255),
    Optimal_Temp FLOAT[],
    Optimal_Humidity FLOAT[]
);

CREATE TABLE IF NOT EXISTS Measurements (
    ID INTEGER PRIMARY KEY,
    Sensor_ID INTEGER REFERENCES Sensors(ID),
    Plant_ID INTEGER REFERENCES Plants(ID),
    Temperature FLOAT,
    Humidity FLOAT,
    Timestamp TIMESTAMP
);