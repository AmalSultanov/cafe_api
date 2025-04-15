import os

from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = os.getenv('SQL_DATABASE_URL')
