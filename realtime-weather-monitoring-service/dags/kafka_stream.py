import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

def get_data(i, j):
    import requests

    res = requests.get("https://api.weather.gov/alerts?point=" + str(i) + "," + str(j))
    if res.status_code == 200:
        res = res.json()
    return None

def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging


    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
   
    curr_time = time.time()
    i = 20
    j = -80
    while True:
        i += 1
        if i >= 48:
            i = 20
            j += -1
        elif j <= -91:
            j = -80
        
        if time.time() > curr_time + 120: #1 minute
            break
        try:
            res = get_data(i,j)
            if res is not None:
                producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue

with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
