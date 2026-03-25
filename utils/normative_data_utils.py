from datetime import datetime
import urllib.parse

from bs4 import BeautifulSoup

from models.normative import Normative


def __format_date(date_str: str) -> str:
    """
    Converte uma string de data em um objeto datetime.
    """
    date = date_str.replace('string;#', '').strip()
    return datetime.strptime(date, '%d/%m/%Y %H:%M')


def __format_content(raw_content: str) -> str:
    """
    Remove tags HTML e formata o conteúdo.
    """
    soup = BeautifulSoup(raw_content, 'html.parser')
    return soup.get_text(strip=True)


def __format_number(number_str: str) -> int:
    """
    Remove pontos e vírgulas e converte para inteiro.
    """
    return int(number_str.split('.', maxsplit=1)[0])


def __format_url(number: int, normative_type: str) -> str:
    """
    Formata a URL do normativo.
    """
    return f'https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo={normative_type}&numero={number}'  # noqa: E501


def format_normative_data(normatives: list[dict]) -> list[dict]:
    """
    Formata os dados dos normativos.
    """
    return [
        {
            'id': normative.get('listItemId'),
            'title': normative.get('title'),
            'date': __format_date(normative.get('RefinableString01')),
            'content': __format_content(normative.get('AssuntoNormativoOWSMTXT')),
            'responsible': normative.get('ResponsavelOWSText'),
            'normative_type': normative.get('TipodoNormativoOWSCHCS'),
            'number': __format_number(normative.get('NumeroOWSNMBR')),
            'url': __format_url(
                __format_number(normative.get('NumeroOWSNMBR')),
                urllib.parse.quote(normative.get('TipodoNormativoOWSCHCS')),
            ),
        }
        for normative in normatives
    ]


def __get_normative_color(normative: Normative) -> str:
    """
    Retorna a cor do normativo.
    """
    if normative.normative_type.lower().startswith('resolução'):
        return '🔴'
    elif normative.normative_type.lower().startswith('instrução normativa'):
        return '🔵'
    else:
        return '🟢'


def format_message(normative: Normative) -> str:
    """
    Formata a mensagem do normativo.
    """
    message = f'{__get_normative_color(normative)} *{normative.title}*\n'
    message += f'Publicado em: {normative.date}*\n'
    message += f'Assunto: {normative.content}*\n'
    message += f'Responsável: {normative.responsible}*\n'
    message += f'🔗 *Link Oficial:* {normative.url}*\n'
    return message
