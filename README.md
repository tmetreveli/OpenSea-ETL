# OpenSea-ETL collections Project

This project is designed to collect data from the OpenSea API, store it in a PostgreSQL database, and upload it to AWS S3. It utilizes Python for scripting, asynchronous requests for efficiency, and custom ORM. The project is structured into several scripts for creating the database and tables, inserting and managing data, and interfacing with AWS S3 for data backups.

## Getting Started

To get this project up and running on your local machine for development and testing purposes, follow these steps.

### Prerequisites
- Python 3.8+
- PostgreSQL
- AWS Account (for S3 services)
- psycopg2 and SQLAlchemy
- aiohttp for asynchronous HTTP requests
- boto3 for AWS S3 interaction

## Setup
Clone the repositroy to your local machine
`
https://github.com/tmetreveli/OpenSea-ETL.git
`

Install required Python packages:
`
pip install -r requirements.txt
`

# Database Setup:

- Update createDatabase.py and createTable.py with your PostgreSQL credentials.
- Run createDatabase.py to create your PostgreSQL database.
- Run createTable.py to create the necessary table within the database.

# AWS Credentials:

- Update uploadS3.py with your AWS credentials (access key ID and secret access key).
- Ensure you have the correct bucket name set up in uploadS3.py.

# Update API Key:

Update utils.py with your OpenSea API key.

# Running the Application:

Run main.py to start the data collection, storage, and upload process.
`
python main.py
`

## Configuration

- Ensure that your PostgreSQL database credentials are correctly set in the scripts where database connections are established.
- Verify your AWS S3 credentials and bucket details in uploadS3.py.
- Double-check the API key in utils.py for fetching data from OpenSea.

## Usage

The main script to run is main.py, which orchestrates the data fetching, processing, and uploading. The data flow is as follows:

1. Fetching Data: Data is fetched from OpenSea using the provided API key.
2. Storing Data: Fetched data is stored in a PostgreSQL database.
3. Uploading Data: Data is then uploaded to AWS S3 for backup and further use.
