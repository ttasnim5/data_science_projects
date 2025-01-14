# fetch_openaq_data.py
import requests
import pandas as pd
import os

def fetch_openaq_data(output_file='./data/openaq_data.csv'):
    """Fetches air quality data from OpenAQ API and saves it to a CSV file."""

    # ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    headers = {
        'accept': 'application/json',
        'X-API-Key': '619165802c7df673a32f7a12c57d2a6bdb514b944843c037733a4458b3fda9c5',
    }
    params = {
        'limit': '1000',
    }
    response = requests.get('https://api.openaq.org/v3/sensors/3919/years', params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    results = response.json().get('results', [])
    df = pd.json_normalize(results)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

fetch_openaq_data()