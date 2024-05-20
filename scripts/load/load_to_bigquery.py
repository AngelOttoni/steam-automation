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
#     test_bigquery_client()