import os
from dotenv import dotenv_values

config = dotenv_values(".env")

GEMINI_API_KEY = config.get("GEMINI_API_KEY")

print("Gemini Key Loaded:", GEMINI_API_KEY)