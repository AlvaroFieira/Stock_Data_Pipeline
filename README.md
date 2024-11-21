
# Alpha Vantage Stock Data Pipeline

## Project Overview
This project builds a data pipeline using Apache Airflow and AWS to fetch, transform, and visualize real-time stock price data. 

## Project Components
It integrates the following components:

1. **Airflow** for orchestrating ETL workflows.
2. **AWS S3** for storing raw and transformed stock data.
3. **AWS EC2** for fetching data from stock APIs.

## Setup

1. **AWS Setup**:
- Create an S3 bucket for storing raw and transformed stock data.
- Set up IAM roles and policies for Airflow, EC2 and S3 to access AWS services.
- Launch an EC2 instance and create a new key pair.
- Add user's IP address to the EC2 instance's inbound rules under the Security tab.
- Connect to the instance using ubuntu and run the following commands:
	```bash
	sudo apt update
	sudo apt upgrade
	sudo apt install python3-pip
	sudo apt install python3-venv
	python3 -m venv airflow_venv
	source airflow_venv/bin/activate
	pip3 install pandas
	pip3 install s3fs
	pip3 install boto3 
	pip3 install requests
	pip3 install apache-airflow
	airflow standalone

2. **Airflow Setup**:
- Paste the Public IPv4 DNS address followed by the port (:8080) into your browser and enter the user and password displayed in the EC2 instance connection.
- Configure SSH host within VS code by adding the following into the hosts file, and then selection `linux`, as this is the platform where the instance is running:
	```bash
	Host {host name}
    		Hostname {public IPv4 address}
    		User ubuntu
    		IdentityFile {path to .pem keypair file generated during the creation of the instance}
- In VS Code open `airflow.cfg` and set the dags location to the following: `dags_folder = /home/ubuntu/airflow/dags`
- Create DAG files in this location.
- Open terminal and run the following commands:
    ```bash
    source airflow_venv/bin/activate
    sudo snap install aws-cli --classic
    aws configure
- Paste your AWS account's access key and secret key, which can be generated under security credentials when clicking on your account in AWS.

## Environment Variables:
- **S3_BUCKET**: name of S3 bucket.
- **S3_KEY_PREFIX_RAW**: folder where the raw json data will be pasted.
- **S3_KEY_PREFIX_TRANSFORMED**: folder where the transformed data will be pasted.
- **ALPHA_VANTAGE_API_KEY**: alpha vantage API key.
- **ALPHA_VANTAGE_API_URL**: alpha vantage API endpoint.

## Script Components

1. `stock_data_pipeline_dag.py`
The Airflow Directed Acyclic Graph (DAG) that orchestrates the entire data pipeline. It schedules and runs tasks for fetching stock data and transforming it.

2. `fetch_stock_data.py`
A script that fetches real-time stock data from the Alpha Vanguard public API. It stores the raw JSON data into an S3 bucket under the stock-data/ prefix.

3. `transform_stock_data.py`
This script processes the raw stock data, cleaning and transforming it into a more usable format (e.g., CSV). The cleaned data is then uploaded to S3 under the transformed-data/ prefix.
