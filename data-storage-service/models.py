import os
import psycopg

host=os.getenv("postgtres-server")
port=os.getenv("5432")
database=os.getenv("POSTGRES_DB")
user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")

# Connect to PostgreSQL server
conn = psycopg.connect(f"dbname='{database}' user='{user}' host='{host}' port='{port}' password='{password}'")

# Create cursor
cur = conn.cursor()

# Create "Sensors" table

cur.execute("""
    CREATE TABLE IF NOT EXISTS Sensors (
        ID INTEGER PRIMARY KEY,
        Provider VARCHAR(255),
        Location VARCHAR(255)
    )
""")

# Create "Plants" table
cur.execute("""
    CREATE TABLE IF NOT EXISTS Plants (
        ID INTEGER PRIMARY KEY,
        Species VARCHAR(255),
        Optimal_Temp FLOAT[],
        Optimal_Humidity FLOAT[]
    )
""")

# Createz "Measurements" table
cur.execute("""
    CREATE TABLE IF NOT EXISTS Measurements (
        ID INTEGER PRIMARY KEY,
        Sensor_ID INTEGER REFERENCES Sensors(ID),
        Plant_ID INTEGER REFERENCES Plants(ID),
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