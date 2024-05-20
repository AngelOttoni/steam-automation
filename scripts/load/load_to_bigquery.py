from google.cloud import bigquery
import os

#TO-DO
# Configure Google Cloud credentials
def configure_gcp_credentials(credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Initializing the BigQuery client
def initialize_bigquery_client():
    return bigquery.Client()

# Test credentials configuration and BigQuery client initialization
# def test_bigquery_client():
#     try:
#         # Configure as credenciais (altere o caminho para o seu arquivo de credenciais)
#         configure_gcp_credentials('credentials/bigquery-access-credentials.json')

#         # Inicialize o cliente do BigQuery
#         client = initialize_bigquery_client()

#         # Execute uma operação simples para testar o cliente
#         datasets = list(client.list_datasets())
#         if datasets:
#             print(f"Datasets encontrados: {[dataset.dataset_id for dataset in datasets]}")
#         else:
#             print("Nenhum dataset encontrado no projeto.")

#         print("Configuração de credenciais e inicialização do cliente bem-sucedida!")
#     except Exception as e:
#         print(f"Erro ao inicializar o cliente do BigQuery: {e}")

# if __name__ == "__main__":
    test_bigquery_client()

# Table columns
# 'name', 'release_date', 'initial_price', 
# 'discount_price', 'reviews', 'search_filter', 'timestamp'

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
    
