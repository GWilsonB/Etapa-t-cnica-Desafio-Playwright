import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://front.serverest.dev").rstrip("/")
API_URL = os.getenv("API_URL", "https://serverest.dev").rstrip("/")
