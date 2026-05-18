from http import HTTPStatus

import requests

from config.logger import Logger
from config.settings import settings
from models.normative import BcbNormative, CvmNormative
from utils.normative_data_utils import format_bcb_message, format_cvm_message


class WhatsappService:
    def __init__(self):
        self.__base_url = settings.EVOLUTION_BASE_URL
        self.__headers = {
            'apikey': settings.EVOLUTION_API_KEY,
            'Content-Type': 'application/json',
        }
        self.__instance_name = settings.EVOLUTION_INSTANCE_NAME
        self.__group_jid = settings.EVOLUTION_GROUP_JID
        self.__logger = Logger(__name__)

    def send_bcb_message(self, normative: BcbNormative):
        self.__logger.info(
            f'Sending WhatsApp message for BCB normative: {normative.title}'
        )
        message = format_bcb_message(normative)
        self.__logger.debug(f'Message:\n{message}')
        url = f'{self.__base_url}/message/sendText/{self.__instance_name}'
        self.__logger.debug(f'URL: {url}')
        payload = {
            'number': self.__group_jid,
            'text': message,
        }
        self.__logger.debug(f'Payload: {payload}')
        response = requests.post(url, headers=self.__headers, json=payload)
        if response.status_code not in {HTTPStatus.OK, HTTPStatus.CREATED}:
            raise Exception(f'Error: {response.status_code} - {response.text}')
        self.__logger.debug(f'Response: {response.json()}')
        self.__logger.info('WhatsApp message sent successfully')
        return response.json()

    def send_cvm_message(self, normative: CvmNormative):
        self.__logger.info(
            f'Sending WhatsApp message for CVM normative: {normative.title}'
        )
        message = format_cvm_message(normative)
        self.__logger.debug(f'Message:\n{message}')
        url = f'{self.__base_url}/message/sendText/{self.__instance_name}'
        self.__logger.debug(f'URL: {url}')
        payload = {
            'number': self.__group_jid,
            'text': message,
        }
        self.__logger.debug(f'Payload: {payload}')
        response = requests.post(url, headers=self.__headers, json=payload)
        if response.status_code not in {HTTPStatus.OK, HTTPStatus.CREATED}:
            raise Exception(f'Error: {response.status_code} - {response.text}')
        self.__logger.debug(f'Response: {response.json()}')
        self.__logger.info('WhatsApp message sent successfully')
        return response.json()
