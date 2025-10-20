import os
from dotenv import load_dotenv
load_dotenv()

SQLITE_URL = os.getenv("SQLITE_URL", "sqlite:///../db/app.db")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
MAILTRAP_HOST = os.getenv("MAILTRAP_HOST", "")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT", "2525") or 2525)
MAILTRAP_USER = os.getenv("MAILTRAP_USER", "")
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS", "")
