import logging
from datetime import datetime
import pytz

from notification import enviar_notificacao_telegram, notificar_pedido
from utils import formatar_relatorio_com_pre
from vtex_api import consumir_api_vtex
from vtex_db import create_table, update_or_insert_order, query_db, exec_db

logging.basicConfig(
    level=logging.INFO,  # ou DEBUG se quiser mais detalhes
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_data():
    """Salva ou atualiza os dados dos pedidos no banco de dados"""
    orders = consumir_api_vtex()

    fuso_br = pytz.timezone('America/Sao_Paulo')
    hora_atual = datetime.now(fuso_br).strftime("%H:%M")

    if not orders:
        logging.info("🚫 Nenhum pedido retornado pela API.")
        return

    # Criar tabela se não existir
    create_table()

    # Contadores
    inseridos = 0
    atualizados = 0
    nao_modificados = 0
    ignorados = 0

    for order in orders:
        status = order['statusDescription'].lower()
        if any(palavra in status for palavra in ['cancel']):
            ignorados += 1
            continue

        acao, objeto = update_or_insert_order(order)

        if acao == "insert":
            inseridos += 1
            notificar_pedido(acao, objeto)
        elif acao == "update":
            atualizados += 1
            notificar_pedido(acao, objeto)
        elif acao == "nochange":
            nao_modificados += 1

    resumo = formatar_relatorio_com_pre(hora_atual, inseridos, atualizados, nao_modificados, ignorados)
    logging.info(resumo)
    enviar_notificacao_telegram(resumo)


if __name__ == "__main__":
    save_data()
    # query_db("SELECT COUNT(orderID) FROM orders ORDER BY orderId DESC;")
    # query_db("SELECT * FROM orders ORDER BY orderId DESC;")
    # exec_db(
    #     "UPDATE orders SET statusDescription = ? WHERE orderId = ?;",
    #     ('cancel', '1531920503129-01')
    # )

