from http import HTTPStatus

import requests
from sqlalchemy.dialects.postgresql import insert

from config.database import database
from config.settings import settings
from models.normative import Normative
from services.whatsapp_service import WhatsappService
from utils.normative_data_utils import format_normative_data


class BcbService:
    def __init__(self):
        self.__base_url = settings.BCB_BASE_URL
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        self.__whatsapp_service = WhatsappService()

    def __get_normatives(self):
        response = requests.get(url=self.__base_url, headers=self.__headers)

        if response.status_code != HTTPStatus.OK:
            raise Exception(f'Error: {response.status_code} - {response.text}')

        return response.json().get('Rows', [])

    def handle_data(self):
        print('Fetching normatives...')
        data = self.__get_normatives()
        if not data:
            raise ValueError('No normatives found')
        normatives = [
            normative
            for normative in data
            # if normative.get('TipodoNormativoOWSCHCS') in NORMATIVE_LIST
        ]
        if not normatives:
            return []
        new_normatives = format_normative_data(normatives)
        stmt = insert(Normative).values(new_normatives)
        stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
        stmt = stmt.returning(Normative.id)
        session_generator = database.get_session()
        session = next(session_generator)
        try:
            result = session.execute(stmt)
            inserted_normatives = [row[0] for row in result.all()]
            session.commit()
        finally:
            session_generator.close()
        normatives_to_send = [
            normative
            for normative in new_normatives
            if normative['id'] in inserted_normatives
        ]
        if normatives_to_send:
            self.__whatsapp_service.send_message(normatives_to_send)
            print(f'{len(normatives_to_send)} normatives sent to WhatsApp.')
        else:
            print('No new normatives found.')
        return normatives_to_send
