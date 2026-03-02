import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")