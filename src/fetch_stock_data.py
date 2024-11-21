import boto3
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/airflow/dags/.env')

# Import environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY_PREFIX_RAW = os.getenv('S3_KEY_PREFIX_RAW')
ALPHA_VANTAGE_API_URL = os.getenv('ALPHA_VANTAGE_API_URL')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def fetch_stock_data(symbol="AAPL"):
    """Fetch stock data from API and paste into AWS s3 bucket."""

    # Call API
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(ALPHA_VANTAGE_API_URL, params=params)
    data = response.json()
    
    # Save raw data locally
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    local_file = f"stock_{symbol}_{timestamp}.json"
    with open(local_file, "w") as f:
        json.dump(data, f)
    
    # Upload to S3
    s3 = boto3.client("s3")
    s3_key = f"{S3_KEY_PREFIX_RAW}{local_file}"
    s3.upload_file(local_file, S3_BUCKET, s3_key)
    print(f"Uploaded {local_file} to s3://{S3_BUCKET}/{s3_key}")
