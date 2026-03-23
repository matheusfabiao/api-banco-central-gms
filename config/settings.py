import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BCB_BASE_URL = os.getenv('BCB_BASE_URL')
    DATABASE_URL = os.getenv('APP_DATABASE_URL')
    EVOLUTION_BASE_URL = os.getenv('EVOLUTION_BASE_URL')
    EVOLUTION_API_KEY = os.getenv('AUTHENTICATION_API_KEY')
    EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')
    EVOLUTION_GROUP_JID = os.getenv('EVOLUTION_GROUP_JID', '5583994210722')


settings = Settings()
