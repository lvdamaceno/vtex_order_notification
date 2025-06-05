import logging
import os
from datetime import datetime, timezone, timedelta
from typing import Optional
from notifications.telegram import enviar_notificacao_telegram

import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def converter_data_iso_para_br(data_iso: str) -> str:
    """Converte data em ISO 8601 para formato brasileiro com fuso de Brasília."""
    try:
        if '+' in data_iso:
            parte_data, parte_fuso = data_iso.split('+')
            parte_data = parte_data[:26]  # até microssegundos
            data_iso_corrigido = f"{parte_data}+{parte_fuso}"
        else:
            data_iso_corrigido = data_iso

        dt = datetime.fromisoformat(data_iso_corrigido)
        dt_brasilia = dt.astimezone(timezone(timedelta(hours=-3)))
        return dt_brasilia.strftime('%d/%m/%Y %H:%M:%S')

    except Exception as e:
        logging.error(f"❌ Erro ao converter data ISO '{data_iso}': {e}")
        return "Data inválida"


def formatar_pedido_pendente(
    orderid: str,
    creationdate: str,
    clientname: str,
    totalvalue: str,
    totalitems: int,
    statusdescription: str
) -> str:
    """Formata uma mensagem de pedido pendente para envio via Telegram."""
    data_formatada = converter_data_iso_para_br(creationdate)
    return (
        "----------- Pedido Pendente -----------\n"
        f"Pedido: {orderid}\n"
        f"Data: {data_formatada}\n"
        f"Cliente: {clientname}\n"
        f"Valor: {totalvalue}\n"
        f"Quantidade: {totalitems}\n"
        f"Status: {statusdescription}\n"
    )


def notificar_pedido(acao: str, objeto_notificacao: Optional[str]) -> None:
    """Envia uma notificação apenas se a ação for insert ou update e houver mensagem."""
    if acao in ("insert", "update") and objeto_notificacao:
        enviar_notificacao_telegram(objeto_notificacao)
