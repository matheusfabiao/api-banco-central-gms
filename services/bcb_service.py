from http import HTTPStatus

import requests
from sqlalchemy.dialects.postgresql import insert

from config.database import database
from config.settings import settings
from models.normative import Normative
from utils.normative_data_utils import format_normative_data
from utils.normative_list import NORMATIVE_LIST


class BcbService:
    def __init__(self):
        self.__base_url = settings.BCB_BASE_URL
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        self.__session = database.get_session()

    def __get_normatives(self):
        response = requests.get(url=self.__base_url, headers=self.__headers)

        if response.status_code != HTTPStatus.OK:
            raise Exception(f'Error: {response.status_code} - {response.text}')

        return response.json().get('Rows', [])

    def handle_data(self):
        data = self.__get_normatives()
        if not data:
            raise ValueError('No normatives found')
        normatives = [
            normative
            for normative in data
            if normative.get('TipodoNormativoOWSCHCS') in NORMATIVE_LIST
        ]
        if not normatives:
            return []
        new_normatives = format_normative_data(normatives)
        stmt = insert(Normative).values(new_normatives)
        stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
        session = next(self.__session)
        session.execute(stmt)
        session.commit()
        return new_normatives
