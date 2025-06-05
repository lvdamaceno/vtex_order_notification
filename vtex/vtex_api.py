import requests
import logging
import os
from typing import List, Optional
from dotenv import load_dotenv
from utils.utils import obter_intervalo_data_atual

load_dotenv()

VTEX_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


def construir_headers_vtex() -> dict:
    """Monta os headers necessários para autenticação na API VTEX"""
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': os.getenv('APPKEY'),
        'X-VTEX-API-AppToken': os.getenv('APPTOKEN')
    }


def construir_url_base() -> str:
    """Monta a URL base da API com o filtro de data já aplicado"""
    base_url = os.getenv('URL')
    if not base_url:
        raise ValueError("URL da API VTEX não está definida no .env")
    filtro_data = obter_intervalo_data_atual(VTEX_DATE_FORMAT)
    return f"{base_url}?per_page=100&f_creationDate={filtro_data}"


def obter_pedidos_da_api(base_url: str, headers: dict) -> List[dict]:
    """Consulta todas as páginas da API VTEX e retorna todos os pedidos"""
    todos_pedidos = []
    pagina = 1
    total_paginas = 1

    while pagina <= total_paginas:
        try:
            url_paginada = f"{base_url}&page={pagina}"
            logging.info(f"🔄 Consultando página {pagina} da API VTEX...")
            response = requests.get(url_paginada, headers=headers)

            if response.status_code != 200:
                logging.warning(f"⚠️ Erro ao consultar página {pagina}: código {response.status_code}")
                break

            resposta_json = response.json()
            pedidos = resposta_json.get("list", [])
            todos_pedidos.extend(pedidos)

            if pagina == 1:
                total_paginas = resposta_json.get("paging", {}).get("pages", 1)
                logging.info(f"📄 Total de páginas a consultar: {total_paginas}")

            pagina += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Erro na requisição da página {pagina}: {e}")
            break
        except ValueError as e:
            logging.error(f"❌ Erro ao interpretar JSON da página {pagina}: {e}")
            break

    logging.info(f"✅ Total de pedidos coletados: {len(todos_pedidos)}")
    return todos_pedidos


def consumir_api_vtex() -> Optional[List[dict]]:
    """Função principal para consumir a API da VTEX"""
    try:
        url_base = construir_url_base()
        headers = construir_headers_vtex()
        pedidos = obter_pedidos_da_api(url_base, headers)
        return pedidos
    except Exception as e:
        logging.error(f"❌ Erro ao consumir API VTEX: {e}")
        return None
