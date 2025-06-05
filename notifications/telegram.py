import logging
import requests
import os
from dotenv import load_dotenv

from utils.utils import formatar_pedido_pendente

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


# Função para enviar notificação para o Telegram
def enviar_notificacao_telegram(mensagem):
    token = os.getenv('BOTTOKEN')  # Seu Token do Bot
    chat_id = os.getenv('CHATID')  # O chat_id do destinatário
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Dados a serem enviados
    payload = {
        'chat_id': chat_id,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }

    # Enviar a requisição para o Telegram
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("Notificação enviada com sucesso!")
            return True
        else:
            logging.warning(f"Falha ao enviar notificação: {response}")
            logging.warning(f"Falha ao enviar notificação: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Ocorreu um erro: {e}")
        return None


def notificar_pedidos_pendentes(pedidos: list) -> None:
    """Envia notificação para cada pedido pendente."""
    for pedido in pedidos:
        try:
            valor_em_centavos = pedido["totalValue"] * 0.01
            totalvalue = f"R$ {valor_em_centavos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            pedido_data = [pedido["orderId"], pedido["creationDate"], pedido["clientName"], totalvalue,
                           pedido["totalItems"], pedido["statusDescription"]]
            mensagem = formatar_pedido_pendente(pedido_data)
            enviar_notificacao_telegram(mensagem)
        except Exception as e:
            logging.error(f"Erro ao notificar pedido {pedido.get('orderId', 'desconhecido')}: {e}")
