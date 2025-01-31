# Streaming & Airflow Project Documentation

## Overview
This project consists of an Apache Airflow DAG for fetching weather data, a shell script for setting up an Airflow environment, and a Spark streaming script for real-time data processing with Apache Cassandra.

---

## Components

### `kafka_stream.py`
- Defines an **Apache Airflow DAG** for streaming weather alerts.
- Retrieves data from `https://api.weather.gov/alerts?point=<latitude>,<longitude>`.
- Uses `requests` to fetch API data.
- Stores processed data for downstream tasks.

#### Key Functions
- `get_data(i, j)`: Fetches weather alerts for a given latitude and longitude.
- `stream_data()`: Manages the streaming of collected data.

#### Dependencies
- `Airflow`
- `requests`
- `datetime`

---

### `entrypoint.sh`
- A **Bash script** that initializes an Airflow instance.
- Installs dependencies from `requirements.txt`.
- Initializes the Airflow database (`airflow db init`).
- Creates an admin user for the Airflow UI.

#### Key Steps
1. Installs Python dependencies if `requirements.txt` exists.
2. Initializes the Airflow database (`airflow db init`).
3. Creates an Airflow admin user (`airflow users create`).
4. Runs `airflow db upgrade` to ensure the database is up to date.

#### Dependencies
- **Airflow** (needs to be installed in the environment)
- **Python** (for package management)

---

### `spark_stream.py`
- A **Spark Streaming** script that processes real-time data and stores it in Cassandra.
- Defines a **keyspace** and a **table** for storing streaming data.

#### Key Functions
- `create_keyspace(session)`: Creates a Cassandra keyspace named `spark_streams`.
- `create_table(session)`: Defines the `created_users` table in Cassandra.
- Uses `pyspark.sql` to process streaming data.

#### Dependencies
- `Apache Spark`
- `pyspark`
- `cassandra-driver`
- `logging`

---

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install apache-airflow pyspark cassandra-driver requests
   ```
2. **Run the Airflow DAG:**
   ```bash
   airflow dags trigger kafka_stream
   ```
3. **Start Spark Streaming:**
   ```bash
   spark-submit spark_stream.py
   ```

---

## License
This project is licensed under [Your License Here].
