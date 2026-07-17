import os
from dotenv import load_dotenv

loaded = load_dotenv()

print("Loaded:", loaded)
print("Current Folder:", os.getcwd())
print("ENV:", os.getenv("GEMINI_KEY"))