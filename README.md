# Steam Automation

>This repository contains scripts for extracting game data from [Steam](https://store.steampowered.com/) using some filters, and storing it in Google BigQuery. 
>
>The automation process involves web scraping, data loading into BigQuery, and then exporting it to Google Sheets for easy access and analysis.

## Structure

- `data/raw`: Contains raw and processed data.
- `credentials/`: Folder to store Google Cloud credentials.
- `scripts/`: Contains the main scripts for the ETL process.
  - `extract/`: Scripts for data extraction.
  - `load/`: Scripts for loading data into BigQuery.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `LICENSE`: Project license file.
- `README.md`: Documentation for the project.
- `requirements.txt`: Python dependencies.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/AngelOttoni/steam-automation>
   cd steam-automation
    ```

1. **Install dependencies**:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
2. **Configure Google Cloud credentials**:
    - Place your service account JSON file in the `credentials/` directory and update the path in the scripts if necessary.


## Usage

1. **Extract data from Steam**:
    
    ```bash
    python scripts/extract/steam_scraper.py
    
    ```
    
2. **Load data into BigQuery**:
    
    ```bash
    python scripts/load/load_to_bigquery.py
    
    ```
    

## License

- This project is licensed under the MIT License - see the [LICENSE](https://www.notion.so/LICENSE) file for details.

## Google Sheets

The data can be viewed at [this link](https://docs.google.com/spreadsheets/d/1Kp7dtkChV_8vaQA5d4CmSt4CxGENB1P02qAoqAyMsQE/edit?usp=sharing).