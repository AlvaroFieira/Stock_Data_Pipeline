import pandas as pd
import boto3
import io
import json
import os
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/airflow/dags/.env')

# Import environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY_PREFIX_RAW = os.getenv('S3_KEY_PREFIX_RAW')
S3_KEY_PREFIX_TRANSFORMED = os.getenv('S3_KEY_PREFIX_TRANSFORMED')


def transform_stock_data():
    """Fetch Stock data from s3 bucket, transform data and upload transformed file to same bucket."""

    s3 = boto3.client("s3")
    
    # List raw files in the S3 bucket
    objects = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_KEY_PREFIX_RAW).get("Contents", [])

    for obj in objects:
        key = obj["Key"]

        if key.endswith(".json"):

            # Download raw file
            raw_file = s3.get_object(Bucket=S3_BUCKET, Key=key)
            raw_data = json.loads(raw_file["Body"].read())
            
            # Transform data
            if "Time Series (1min)" in raw_data:
                df = pd.DataFrame.from_dict(raw_data["Time Series (1min)"], orient="index")
                df.index.name = "timestamp"
                df.reset_index(inplace=True)
                
                # Save transformed data to S3
                transformed_buffer = io.StringIO()
                df.to_csv(transformed_buffer, index=False)
                transformed_key = key.replace(S3_KEY_PREFIX_RAW, S3_KEY_PREFIX_TRANSFORMED).replace(".json", ".csv")
                s3.put_object(Bucket=S3_BUCKET, Key=transformed_key, Body=transformed_buffer.getvalue())
                print(f"Transformed and saved to s3://{S3_BUCKET}/{transformed_key}")
