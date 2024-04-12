import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title('Dashboard des Mesures')

DATABASE_URI = 'postgresql://admin:admin@data-storage-service:5432/Urban_Farm_Monitoring'
engine = create_engine(DATABASE_URI)

data = pd.read_sql("SELECT * FROM measurements", engine)

st.write("### Données Complètes", data)

high_temp = data[data.temperature > 30]
high_humidity = data[data.humidity > 80]

st.write("### Températures Élevées", high_temp)
st.write("### Humidités Élevées", high_humidity)
