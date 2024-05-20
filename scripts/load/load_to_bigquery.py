from google.cloud import bigquery
import os

#TO-DO
# Configure Google Cloud credentials
def configure_gcp_credentials(credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Initializing the BigQuery client
def initialize_bigquery_client():
    return bigquery.Client()

def create_dataset(client, dataset_id, location='southamerica-east1'):
    """
    Creates a dataset in BigQuery if it does not exist.
    
    Args:
        client (bigquery.Client): BigQuery client.
        dataset_id (str): ID of the dataset to be created.
        location (str): Location of the dataset.
    """
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = location
    client.create_dataset(dataset, exists_ok=True)
    
def create_table(client, dataset_id, table_id, schema):
    """
    Creates a table in BigQuery if it does not exist.
    
    Args:
        client (bigquery.Client): BigQuery client.
        dataset_id (str): ID of the dataset where the table will be created.
        table_id (str): ID of the table to be created.
        schema (list): Table schema.
    """
    table = bigquery.Table(client.dataset(dataset_id).table(table_id), schema=schema)
    client.create_table(table, exists_ok=True) 
    
def load_data_to_table(client, dataset_id, table_id, file_path):
    """
    Load data from a CSV file into a table in BigQuery.
    
    Args:
        client (bigquery.Client): BigQuery client.
        dataset_id (str): Dataset ID.
        table_id (str): Table ID.
        file_path (str): Path to CSV file.
    """
    table = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )
    with open(file_path, 'rb') as source_file:
        job = client.load_table_from_file(source_file, table, job_config=job_config)
    job.result()  # Wait until the job is completed
    
def main():
    # Path to credentials file
    credentials_path = 'credentials/bigquery-access-credentials.json'
    
    # Configure credentials
    configure_gcp_credentials(credentials_path)
    
    # Initialize the BigQuery client
    client = initialize_bigquery_client()
    
    # Dataset and table name
    dataset_id = 'steam_dataset'
    table_id = 'steam'
    
    # Create of the dataset
    create_dataset(client, dataset_id)
    
    # Table columns
    # 'name', 'release_date', 'initial_price', 
    # 'discount_price', 'reviews', 'search_filter', 'timestamp'
    
    # Table schema
    schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('release_date', 'STRING'),
        bigquery.SchemaField('initial_price', 'FLOAT'),
        bigquery.SchemaField('discount_price', 'FLOAT'),
        bigquery.SchemaField('reviews', 'INTEGER'),
        bigquery.SchemaField('search_filter', 'STRING'),
        bigquery.SchemaField('timestamp', 'TIMESTAMP'),
    ]
    
    # Create the table
    create_table(client, dataset_id, table_id, schema)
    
    # Path to CSV file
    file_path = 'data/raw/steam_data.csv'
    
    # Load data into table
    load_data_to_table(client, dataset_id, table_id, file_path)
    
    print("Data loaded into BigQuery!")

if __name__ == "__main__":
    main()