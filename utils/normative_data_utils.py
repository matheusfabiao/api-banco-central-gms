import urllib.parse
import zlib
from datetime import datetime

from bs4 import BeautifulSoup

from models.normative import BcbNormative, CvmNormative


def __format_date(date_str: str) -> str:
    """
    Converte uma string de data em um objeto datetime.
    """
    date = date_str.replace('string;#', '').strip()
    return datetime.strptime(date, '%d/%m/%Y %H:%M')


def __unformat_date(date: datetime) -> str:
    """
    Converte um objeto datetime, de formato "%Y-%m-%d %H:%M:%S" para uma string
    no formato "%d/%m/%Y %H:%M".
    """
    return f'{date.day}/{date.month}/{date.year} às {date.strftime("%H:%M")}'


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
    base_url = 'https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo'
    return f'{base_url}?tipo={normative_type}&numero={number}'


def format_cvm_url(sufix: str) -> str:
    """
    Formata a URL do normativo CVM.
    https://conteudo.cvm.gov.br/legislacao/resolucoes/resol243.html
    """
    return f'https://conteudo.cvm.gov.br/legislacao/{sufix}'


def format_bcb_normative_data(normatives: list[dict]) -> list[dict]:
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


def __get_bcb_normative_color(normative: BcbNormative) -> str:
    """
    Retorna a cor do normativo.
    """
    if normative.normative_type.lower().startswith('resolução'):
        return '🔴'
    elif normative.normative_type.lower().startswith('instrução normativa'):
        return '🔵'
    else:
        return '🟢'


def format_bcb_message(normative: BcbNormative) -> str:
    """
    Formata a mensagem do normativo.
    """
    message = f'{__get_bcb_normative_color(normative)} *{normative.title}*\n'
    message += f'Publicado em: {__unformat_date(normative.date)}\n'
    message += f'\n*Ementa:*\n{normative.content}\n'
    message += f'\nResponsável: *{normative.responsible}*\n'
    message += f'\n🔗 *Link Oficial:*\n{normative.url}\n'
    return message


def generate_cvm_id(url: str) -> int:
    """
    Gera um ID numérico único (32-bit integer) baseado na URL da norma.
    """

    MAX_SIGNED_INT32 = 0x7FFFFFFF
    UINT32_OFFSET = 0x100000000

    crc = zlib.crc32(url.encode('utf-8'))
    if crc > MAX_SIGNED_INT32:
        return crc - UINT32_OFFSET
    return crc


def format_cvm_date(date_str: str) -> datetime:
    """
    Tenta converter a string de data da CVM para um objeto datetime.
    """
    date_str = date_str.strip()
    formats = ['%d/%m/%Y %H:%M', '%d/%m/%Y', '%Y-%m-%d']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.now()


def __get_cvm_normative_color(normative: CvmNormative) -> str:
    """
    Retorna a cor do normativo.
    """
    if normative.normative_type.lower().startswith('resoluções'):
        return '🔴'
    elif normative.normative_type.lower().startswith('instruções'):
        return '🔵'
    else:
        return '🟢'


def format_cvm_message(normative: CvmNormative) -> str:
    """
    Formata a mensagem do normativo.
    """
    message = f'{__get_cvm_normative_color(normative)} *{normative.title}*\n'
    message += f'Publicado em: {__unformat_date(normative.date)}\n'
    message += f'\n*Ementa:*\n{normative.content}\n'
    message += f'\n🔗 *Link Oficial:*\n{normative.url}\n'
    return message
