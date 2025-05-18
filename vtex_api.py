import logging
import os
from datetime import datetime
from urllib.parse import quote

from dotenv import load_dotenv
import requests

load_dotenv()


def consumir_api_vtex():
    """Consome a API da VTEX com paginação automática e retorna todos os pedidos do mês atual"""

    hoje = datetime.utcnow()
    primeiro_dia_mes = hoje.replace(day=1)

    formato_vtex = "%Y-%m-%dT%H:%M:%S.000Z"
    inicio = primeiro_dia_mes.strftime(formato_vtex)
    fim = hoje.strftime(formato_vtex)

    intervalo = f"creationDate:[{inicio} TO {fim}]"
    filtro = quote(intervalo)

    base_url = f"{os.getenv('URL')}?per_page=100&f_creationDate={filtro}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': os.getenv('APPKEY'),
        'X-VTEX-API-AppToken': os.getenv('APPTOKEN')
    }

    todos_pedidos = []
    pagina = 1
    total_paginas = 1  # valor inicial provisório

    try:
        while pagina <= total_paginas:
            url_paginada = f"{base_url}&page={pagina}"
            logging.info(f"🔄 Consultando página {pagina} da API VTEX...")
            response = requests.get(url_paginada, headers=headers)

            if response.status_code != 200:
                logging.warning(f"⚠️ Erro ao consultar página {pagina}: {response.status_code}")
                break

            resposta_json = response.json()

            pedidos = resposta_json.get("list", [])
            todos_pedidos.extend(pedidos)

            if pagina == 1:
                # Obtém total de páginas apenas na primeira resposta
                total_paginas = resposta_json.get("paging", {}).get("pages", 1)
                logging.info(f"📄 Total de páginas a consultar: {total_paginas}")

            pagina += 1

        logging.info(f"✅ Total de pedidos coletados: {len(todos_pedidos)}")
        return todos_pedidos

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erro durante requisição à API VTEX: {e}")
        return None