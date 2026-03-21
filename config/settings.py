import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BCB_BASE_URL = os.getenv('BCB_BASE_URL')
    DATABASE_URL = os.getenv('DATABASE_CONNECTION_URI')


settings = Settings()
