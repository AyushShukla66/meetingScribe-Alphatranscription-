from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

REPORT_FOLDER = "reports"
LOG_FOLDER = "logs"
TEMP_FOLDER = "temp"