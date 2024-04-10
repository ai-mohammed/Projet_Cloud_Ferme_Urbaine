import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulation de chargement de données
def load_sensor_data():
    now = datetime.now()
    data = pd.DataFrame({
        'sensor_id': ['sensor1', 'sensor2', 'sensor3', 'sensorCustom'],
        'plant_id': [1, 1, 2, 2],
        'timestamp': [now - timedelta(minutes=5), now - timedelta(days=1), now - timedelta(minutes=10), now],
        'temperature': [295.15, 310.15, 285.15, 288.15],  # Kelvin
        'humidity': [45, 15, 80, 50],  # Pourcentage
    })
    return data

# Fonctions pour l'analyse de l'état des plantes
def analyze_plant_health(data):
    health_issues = []
    for _, row in data.iterrows():
        issues = []
        if not (288.15 <= row['temperature'] <= 298.15):  # Plages optimales de température
            issues.append('temperature')
        if not (30 <= row['humidity'] <= 70):  # Plages optimales d'humidité
            issues.append('humidity')
        if issues:
            health_issues.append({'plant_id': row['plant_id'], 'issues': issues})
    return health_issues

# Fonctions pour vérifier l'état des capteurs
def analyze_sensor_status(data):
    sensor_issues = []
    latest_data_time = data['timestamp'].max()
    for sensor_id, group in data.groupby('sensor_id'):
        if (latest_data_time - group['timestamp'].max()) > timedelta(hours=1):
            sensor_issues.append({'sensor_id': sensor_id, 'issue': 'no recent data'})
    return sensor_issues

def main():
    data = load_sensor_data()
    plant_health_issues = analyze_plant_health(data)
    sensor_status_issues = analyze_sensor_status(data)

    if plant_health_issues:
        print("Plant health issues detected:")
        for issue in plant_health_issues:
            print(f"Plant {issue['plant_id']}: {' and '.join(issue['issues'])} issue(s)")

    if sensor_status_issues:
        print("\nSensor issues detected:")
        for issue in sensor_status_issues:
            print(f"Sensor {issue['sensor_id']}: {issue['issue']}")

    if not plant_health_issues and not sensor_status_issues:
        print("No plant health or sensor issues detected.")

if __name__ == "__main__":
    main()
