import logging
import sqlite3
from tabulate import tabulate
from notification import enviar_notificacao_telegram, new_order, update_order


logging.basicConfig(
    level=logging.INFO,  # ou DEBUG se quiser mais detalhes
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_table():
    """Cria a tabela 'orders' no banco de dados, se não existir"""
    db = sqlite3.connect('vtex_orders.db')
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        orderId TEXT PRIMARY KEY,
        creationDate TEXT,
        clientName TEXT,
        totalValue REAL,
        paymentNames TEXT,
        statusDescription TEXT,
        sequence TEXT,
        isAllDelivered TEXT,
        isAnyDelivered TEXT
    );
    """)

    db.commit()
    cursor.close()
    db.close()


def convert_delivery_status(value):
    """Converte o valor de 0 ou 1 para 'não' ou 'sim'"""
    return "sim" if value == 1 else "não"


def update_or_insert_order(order):
    """Atualiza ou insere um pedido no banco de dados"""
    db = sqlite3.connect('vtex_orders.db')
    cursor = db.cursor()

    # Verificar se o pedido já existe no banco
    cursor.execute("SELECT * FROM orders WHERE orderId = ?", (order['orderId'],))
    existing_order = cursor.fetchone()

    # Convertendo status para "sim" ou "não"
    is_all_delivered = convert_delivery_status(order['isAllDelivered'])
    is_any_delivered = convert_delivery_status(order['isAnyDelivered'])

    if existing_order:
        campos_para_verificar = [
            ("statusDescription", existing_order[5], order['statusDescription']),
            ("isAllDelivered", existing_order[7], is_all_delivered),
            ("isAnyDelivered", existing_order[8], is_any_delivered),
        ]

        changes = []
        update_values = []
        set_clauses = []

        for campo, valor_antigo, valor_novo in campos_para_verificar:
            if valor_antigo != valor_novo:
                changes.append(campo)
                set_clauses.append(f"{campo} = ?")
                update_values.append(valor_novo)

        if changes:
            update_query = f"UPDATE orders SET {', '.join(set_clauses)} WHERE orderId = ?"
            update_values.append(order['orderId'])

            cursor.execute(update_query, update_values)
            db.commit()

            logging.info(f"Pedido {order['orderId']} atualizado: {', '.join(changes)}")

            updateorder = update_order(
                order['orderId'],
                order['creationDate'],
                order['clientName'],
                order['totalValue'],
                order['statusDescription'],
                ', '.join(changes)
            )
            enviar_notificacao_telegram(updateorder)
    else:
        # Inserir novo pedido no banco
        query = """INSERT INTO orders (
            orderId, creationDate, clientName, totalValue, paymentNames,
            statusDescription, sequence, isAllDelivered, isAnyDelivered
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        data = (
            order['orderId'],
            order['creationDate'],
            order['clientName'],
            order['totalValue'],
            order['paymentNames'],
            order['statusDescription'],
            order['sequence'],
            is_all_delivered,
            is_any_delivered
        )

        cursor.execute(query, data)
        db.commit()
        logging.info(f"Pedido {order['orderId']} inserido.")
        neworder = new_order(order['orderId'], order['creationDate'], order['clientName'],
                             order['totalValue'], order['statusDescription'])
        enviar_notificacao_telegram(neworder)


    cursor.close()
    db.close()


def query_db(query):
    conn = sqlite3.connect('vtex_orders.db')
    cursor = conn.cursor()

    cursor.execute(query)
    dados = cursor.fetchall()

    colunas = [descricao[0] for descricao in cursor.description]
    logging.info(tabulate(dados, headers=colunas, tablefmt="grid"))

    conn.close()

def exec_db(query: str, params: tuple = ()):
    """
    Executa uma query de escrita no banco de dados (UPDATE, INSERT, DELETE).

    :param query: Comando SQL
    :param params: Tupla de parâmetros (opcional)
    """
    conn = sqlite3.connect('vtex_orders.db')
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()
        logging.info(f"✅ Query executada com sucesso: {query.strip()}")
    except sqlite3.Error as e:
        logging.error(f"❌ Erro ao executar a query: {e}")
    finally:
        conn.close()
