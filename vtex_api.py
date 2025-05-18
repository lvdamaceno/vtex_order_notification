import logging
import os
from datetime import datetime, timedelta
from logging import Logger
from urllib.parse import quote

from dotenv import load_dotenv
import requests

load_dotenv()

def consumir_api_vtex():
    """Consome a API da VTEX e retorna os pedidos"""

    # Data atual (UTC)
    hoje = datetime.utcnow()

    # Primeiro dia do mês atual
    primeiro_dia_mes = hoje.replace(day=1)

    # Formato esperado pela VTEX
    formato_vtex = "%Y-%m-%dT%H:%M:%S.000Z"
    inicio = primeiro_dia_mes.strftime(formato_vtex)
    fim = hoje.strftime(formato_vtex)

    # Monta intervalo e codifica
    intervalo = f"creationDate:[{inicio} TO {fim}]"
    filtro = quote(intervalo)

    url = f"{os.getenv('URL')}?per_page=100&f_creationDate={filtro}"
    logging.info(f"url: {url}")

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': os.getenv('APPKEY'),
        'X-VTEX-API-AppToken': os.getenv('APPTOKEN')
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logging.info("Dados recebidos com sucesso!")
            data = response.json()  # Retorna os dados JSON da resposta
            return data['list']
        else:
            logging.warning(f"Erro ao fazer a requisição: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Ocorreu um erro: {e}")
        return None

