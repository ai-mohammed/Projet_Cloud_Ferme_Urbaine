import os
import psycopg

# Connect to PostgreSQL server
conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)

# Create cursor
cur = conn.cursor()

# Create "Sensors" table
cur.execute("""
    CREATE TABLE Sensors (
        ID INTEGER PRIMARY KEY,
        Provider VARCHAR(255),
        Location VARCHAR(255)
    )
""")

# Create "Plants" table
cur.execute("""
    CREATE TABLE Plants (
        ID INTEGER PRIMARY KEY,
        Species VARCHAR(255),
        Optimal_Temp FLOAT[],
        Optimal_Humidity FLOAT[]
    )
""")

# Createz "Measurements" table
cur.execute("""
    CREATE TABLE Measurements (
        ID INTEGER PRIMARY KEY,
        Sensor_ID INTEGER REFERENCES Sensors(ID),
        Plant_ID INTEGER REFERENCES Plant(ID),
        Temperature FLOAT,
        Humidity FLOAT,
        Timestamp TIMESTAMP
    )
""")

# Commit
conn.commit()

# Close
cur.close()
conn.close()