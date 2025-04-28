import sqlite3
from tabulate import tabulate
from notification import enviar_notificacao_telegram, new_order, update_order


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
        # Verificar se o pedido teve alterações
        changes = []
        update_query = "UPDATE orders SET"
        update_values = []

        # Verificar se houve alterações nos dados
        if existing_order[1] != order['creationDate']:
            changes.append("creationDate")
            update_query += " creationDate = ?,"
            update_values.append(order['creationDate'])

        if existing_order[2] != order['clientName']:
            changes.append("clientName")
            update_query += " clientName = ?,"
            update_values.append(order['clientName'])

        if abs(existing_order[3] - (order['totalValue'] * 0.01)) > 0.01:
            changes.append("totalValue")
            update_query += " totalValue = ?,"
            update_values.append(order['totalValue'] * 0.01)

        if existing_order[4] != order['paymentNames']:
            changes.append("paymentNames")
            update_query += " paymentNames = ?,"
            update_values.append(order['paymentNames'])

        if existing_order[5] != order['statusDescription']:
            changes.append("statusDescription")
            update_query += " statusDescription = ?,"
            update_values.append(order['statusDescription'])

        if existing_order[6] != order['sequence']:
            changes.append("sequence")
            update_query += " sequence = ?,"
            update_values.append(order['sequence'])

        if existing_order[7] != is_all_delivered:
            changes.append("isAllDelivered")
            update_query += " isAllDelivered = ?,"
            update_values.append(is_all_delivered)

        if existing_order[8] != is_any_delivered:
            changes.append("isAnyDelivered")
            update_query += " isAnyDelivered = ?,"
            update_values.append(is_any_delivered)

        # Se houveram mudanças, finalize a query
        if changes:
            update_query = update_query.rstrip(",")  # Remove a vírgula extra
            update_query += " WHERE orderId = ?"
            update_values.append(order['orderId'])

            cursor.execute(update_query, update_values)
            db.commit()
            print(f"Pedido {order['orderId']} atualizado: {', '.join(changes)}")
            updateorder = update_order(order['orderId'], order['creationDate'], order['clientName'],
                                    order['totalValue'], order['statusDescription'], {', '.join(changes)})
            enviar_notificacao_telegram(updateorder)
        # else:
        #     print(f"Pedido {order['orderId']} não teve alterações reais.")
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
        print(f"Pedido {order['orderId']} inserido.")
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
    print(tabulate(dados, headers=colunas, tablefmt="grid"))

    conn.close()
