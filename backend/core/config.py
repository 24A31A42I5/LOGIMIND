import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = 'LOGIMIND'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
MONGODB_URI = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI', '')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'logimind')


def is_demo_mode() -> bool:
	return not bool(MONGODB_URI)
