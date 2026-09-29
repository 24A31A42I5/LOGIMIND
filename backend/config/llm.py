import os

from dotenv import load_dotenv

load_dotenv()


LLM_CONFIG = {
    'provider': os.getenv('LLM_PROVIDER', 'groq'),
    'api_key': os.getenv('LLM_API_KEY', ''),
    'model': os.getenv('LLM_MODEL', 'llama-3.3-70b-versatile'),
}


def get_llm_config() -> dict:
    return LLM_CONFIG.copy()
