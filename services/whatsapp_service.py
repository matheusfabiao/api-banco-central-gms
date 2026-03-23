from http import HTTPStatus

import requests

from config.settings import settings
from utils.normative_data_utils import format_message


class WhatsappService:
    def __init__(self):
        self.__base_url = settings.EVOLUTION_BASE_URL
        self.__headers = {
            'apikey': settings.EVOLUTION_API_KEY,
            'Content-Type': 'application/json',
        }
        self.__instance_name = settings.EVOLUTION_INSTANCE_NAME
        self.__group_jid = settings.EVOLUTION_GROUP_JID

    def send_message(self, new_normatives: list[dict]):
        message = format_message(new_normatives)
        url = f'{self.__base_url}/message/sendText/{self.__instance_name}'
        payload = {
            'number': self.__group_jid,
            'text': message,
        }
        response = requests.post(url, headers=self.__headers, json=payload)
        if response.status_code != HTTPStatus.OK:
            raise Exception(f'Error: {response.status_code} - {response.text}')
        return response.json()
