import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv(OPENAI_API_KEY)
GAME_URL = "https://hackmerlin.io/"
MAX_TRIES_PER_LEVEL = 20
HEADLESS_MODE = False 