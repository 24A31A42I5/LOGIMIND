import os

from dotenv import load_dotenv

load_dotenv()


HINDSIGHT_CONFIG = {
    'api_url': os.getenv('HINDSIGHT_API_URL', ''),
    'api_key': os.getenv('HINDSIGHT_API_KEY', ''),
    'bank_id': os.getenv('HINDSIGHT_BANK_ID', 'logimind-distributor-hub-01'),
}


def is_hindsight_configured() -> bool:
    return bool(HINDSIGHT_CONFIG['api_url'] and HINDSIGHT_CONFIG['api_key'])
