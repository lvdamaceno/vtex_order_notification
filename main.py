import logging
from datetime import datetime

from notification import enviar_notificacao_telegram
from vtex_api import consumir_api_vtex
from vtex_db import create_table, update_or_insert_order, query_db, exec_db

logging.basicConfig(
    level=logging.INFO,  # ou DEBUG se quiser mais detalhes
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_data():
    """Salva ou atualiza os dados dos pedidos no banco de dados"""
    orders = consumir_api_vtex()

    hora_atual = datetime.now().strftime("%H:%M")

    if orders:
        # Criar tabela se não existir
        create_table()

        enviar_notificacao_telegram(f"📝 Relatório de pedidos de {hora_atual}")

        for order in orders:
            # Verificar se statusDescription contém 'cancel'
            status = order['statusDescription'].lower()
            # if any(palavra in status for palavra in ['cancel', 'faturado']):
            if any(palavra in status for palavra in ['cancel']):
                continue  # Ignorar pedidos com "cancel" e faturado no statusDescription
            # Atualizar ou inserir pedido no banco de dados
            update_or_insert_order(order)

if __name__ == "__main__":
    save_data()
    query_db("SELECT COUNT(orderID) FROM orders ORDER BY orderId DESC;")
    query_db("SELECT * FROM orders ORDER BY orderId DESC;")

    # exec_db(
    #     "UPDATE orders SET statusDescription = ? WHERE orderId = ?;",
    #     ('cancel', '1531920503129-01')
    # )

