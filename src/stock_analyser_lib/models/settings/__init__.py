import os
import json
from typing import Dict, Tuple, Optional


CONFIG_FILE = os.environ.get('APP_CONFIG', 'config/config.json')


# Load Database Configuration
def load_config(config_file_path: str) -> Dict:
    """Loads database configuration from the caller component's config.json file."""
    if os.path.isfile(CONFIG_FILE):
        with open(config_file_path) as f:
            return json.load(f)
    return {}


CONFIG = load_config(config_file_path=CONFIG_FILE)


def get_config_from_env() -> Tuple[Optional[str], Optional[str]]:
    # Load confi DB from env variable
    financial_data_db = os.environ.get('FINANCIAL_DATA_DB')
    financial_data_db_schema = os.environ.get('FINANCIAL_DATA_DB_SCHEMA')
    return financial_data_db, financial_data_db_schema


def get_config_from_config() -> Tuple[Optional[str], Optional[str]]:
    # Load config DB from file
    financial_data_db = CONFIG.get('FINANCIAL_DATA_DB', {}).get('DBCON')
    financial_data_db_schema = CONFIG.get('FINANCIAL_DATA_DB', {}).get('SCHEMA')
    return financial_data_db, financial_data_db_schema


financial_data_db, financial_data_db_schema = get_config_from_env()

if not financial_data_db or not financial_data_db_schema:
    financial_data_db, financial_data_db_schema = get_config_from_config()

FINANCIAL_DATA_DB = financial_data_db
FINANCIAL_DATA_DB_SCHEMA = financial_data_db_schema
