import os
from dotenv import load_dotenv
import requests

load_dotenv()


def consumir_api_vtex():
    """Consome a API da VTEX e retorna os pedidos"""
    url = f"{os.getenv('URL')}?per_page=100"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': os.getenv('APPKEY'),
        'X-VTEX-API-AppToken': os.getenv('APPTOKEN')
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Dados recebidos com sucesso!")
            data = response.json()  # Retorna os dados JSON da resposta
            return data['list']
        else:
            print(f"Erro ao fazer a requisição: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")
        return None
