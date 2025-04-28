from vtex_api import consumir_api_vtex
from vtex_db import create_table, update_or_insert_order, query_db


def save_data():
    """Salva ou atualiza os dados dos pedidos no banco de dados"""
    orders = consumir_api_vtex()
    if orders:
        # Criar tabela se não existir
        create_table()

        for order in orders:
            # Verificar se statusDescription contém 'cancel'
            if 'cancel' in order['statusDescription'].lower():
                continue  # Ignorar pedidos com "cancel" no statusDescription

            # Atualizar ou inserir pedido no banco de dados
            update_or_insert_order(order)


if __name__ == "__main__":
    save_data()
    # query_db("SELECT COUNT(orderID) FROM orders ORDER BY orderId DESC;")
    # query_db("SELECT * FROM orders ORDER BY orderId DESC;")
