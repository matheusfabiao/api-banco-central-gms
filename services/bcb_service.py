from http import HTTPStatus

import requests

from config.database import database
from config.logger import Logger
from config.settings import settings
from models.normative import Normative
from services.whatsapp_service import WhatsappService
from utils.normative_data_utils import format_normative_data
from utils.normative_list import NORMATIVE_LIST


class BcbService:
    def __init__(self):
        self.__base_url = settings.BCB_BASE_URL
        self.__headers = {'User-Agent': 'curl/7.81.0', 'Accept': '*/*'}
        self.__whatsapp_service = WhatsappService()
        self.__logger = Logger(__name__)

    def __get_normatives(self):
        self.__logger.info('Fetching normatives...')
        response = requests.get(url=self.__base_url, headers=self.__headers)

        if response.status_code != HTTPStatus.OK:
            raise Exception(f'Error: {response.status_code} - {response.text}')

        return response.json().get('Rows', [])

    def handle_data(self):
        data = self.__get_normatives()
        if not data:
            raise ValueError('No normatives found')
        raw_normatives = []
        session_generator = database.get_session()
        session = next(session_generator)
        try:
            for normative in data:
                normative_id = normative.get('listItemId')
                normative_type = normative.get('TipodoNormativoOWSCHCS')
                query = session.get(Normative, normative_id)
                self.__logger.debug(f'Query: {query}')
                if query or normative_type not in NORMATIVE_LIST:
                    continue
                raw_normatives.append(normative)
            normatives = format_normative_data(raw_normatives)
            self.__logger.info(f'Found {len(normatives)} new normatives')
            for normative in normatives:
                new_normative = Normative(**normative)
                self.__logger.debug(f'New normative: {new_normative.title}')
                session.add(new_normative)
                self.__whatsapp_service.send_message(new_normative)
            session.commit()
        finally:
            session_generator.close()
        return normatives
