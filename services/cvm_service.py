from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from config.database import database
from config.logger import Logger
from config.settings import settings
from models.normative import CvmNormative
from services.whatsapp_service import WhatsappService
from utils.normative_data_utils import format_cvm_date, format_cvm_url, generate_cvm_id


class CvmService:
    def __init__(self):
        self.__base_url = settings.CVM_BASE_URL
        self.__headers = {'User-Agent': 'curl/7.81.0', 'Accept': '*/*'}
        self.__whatsapp_service = WhatsappService()
        self.__logger = Logger(__name__)

    def __get_normatives(self):
        self.__logger.info('Fetching CVM normatives...')

        response = requests.get(url=self.__base_url, headers=self.__headers)

        if response.status_code != HTTPStatus.OK:
            raise Exception(f'Error: {response.status_code} - {response.text}')

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('article')

    def handle_data(self):
        data = self.__get_normatives()
        if not data:
            raise ValueError('No normatives found')
        normatives = []
        session_generator = database.get_session()
        session = next(session_generator)
        try:
            for normative in data:
                title = normative.h3.a.text.strip()
                sufix_url = normative.h3.a['href']
                cvm_id = generate_cvm_id(sufix_url)

                if session.get(CvmNormative, cvm_id):
                    continue

                url = format_cvm_url(sufix_url)
                content = normative.find('div', class_='contentDesc').text.strip()
                date = normative.find('div', class_='infoItem').find('p').text.strip()
                normative_type = (
                    normative
                    .find('div', class_='infoItem')
                    .find_all('p')[1]
                    .text.strip()
                )

                self.__logger.debug(f'{title} {url} {content} {date} {normative_type}')
                normatives.append({
                    'id': cvm_id,
                    'title': title,
                    'url': url,
                    'content': content,
                    'date': format_cvm_date(date),
                    'normative_type': normative_type,
                })
            self.__logger.info(f'Found {len(normatives)} new CVM normatives')
            for normative in normatives:
                new_normative = CvmNormative(**normative)
                self.__logger.debug(f'New CVM normative: {new_normative.title}')
                session.add(new_normative)
                self.__whatsapp_service.send_cvm_message(new_normative)
            session.commit()
        finally:
            session_generator.close()
        return normatives
