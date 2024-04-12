# Urban Vertical Farm Cloud Architecture

## Project Overview
This project develops a cloud-based architecture to monitor an urban vertical farm. The system is designed to receive real-time data from various sensors, store historical data for analysis, and provide operators with a simplified interface to oversee sensor data. Additionally, it aims to detect anomalies in the data to promptly notify operators of potential issues with the sensors or crops.

## Architecture
The proposed architecture consists of several key components:

- **Data Reception API (API de Réception des Données):** Receives data from farm sensors.
- **Relational Database (Base de Données Relationnelle):** Stores historical sensor data.
- **Application Server (Serveur d'Application):** Retrieves data from the database and serves it to the user interface.
- **User Interface (Interface Utilisateur):** Allows operators to monitor and analyze sensor data.
- **Data Analysis Engine (Moteur d'Analyse de Données):** Analyzes data to identify optimal growing conditions and predict maintenance needs.
- **Alert Service (Service d'Alerte):** Sends alerts for detected anomalies in sensor data or plant growth.


### MVC Diagram :
![Architecture Proposée](https://github.com/ai-mohammed/Projet_Cloud_Ferme_Urbaine/blob/main/images/Architecture_Proposée.png)

### Sequence Diagram :
![Sequence Diagram](https://github.com/ai-mohammed/Projet_Cloud_Ferme_Urbaine/blob/main/images/Interactions_entre_les_Composants.png)