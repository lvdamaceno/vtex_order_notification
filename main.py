import logging
from datetime import datetime
import pytz

from notification import enviar_notificacao_telegram, new_order
from utils import formatar_relatorio_com_pre
from vtex_api import consumir_api_vtex


logging.basicConfig(
    level=logging.INFO,  # ou DEBUG se quiser mais detalhes
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_data():
    orders = consumir_api_vtex()

    fuso_br = pytz.timezone('America/Sao_Paulo')
    hora_atual = datetime.now(fuso_br).strftime("%H:%M")

    if not orders:
        logging.info("🚫 Nenhum pedido retornado pela API.")
        return

    # pendentes = 1
    pendentes = sum(1 for pedido in orders if pedido["status"] not in ("invoiced", "canceled"))
    faturados = sum(1 for pedido in orders if pedido["status"] == "invoiced")
    cancelados = sum(1 for pedido in orders if pedido["status"] == "canceled")

    if pendentes == 0:
        enviar_notificacao_telegram("❌ Nenhum pedido pendente")
        logging.info("❌ Nenhum pedido pendente")
        return

    for pedido in orders:
        # if pedido["status"] not in ("canceled"):
        if pedido["status"] not in ("invoiced", "canceled"):
            orderid = pedido["orderId"]
            creationdate = pedido["creationDate"]
            clientname = pedido["clientName"]
            valor_em_centavos = pedido["totalValue"] * 0.01
            totalvalue = f"R$ {valor_em_centavos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            totalitems = pedido["totalItems"]
            statusdescription = pedido["statusDescription"]

            enviar_notificacao_telegram(new_order(orderid, creationdate, clientname, totalvalue, totalitems, statusdescription))



    resumo = formatar_relatorio_com_pre(hora_atual, pendentes, faturados, cancelados)
    logging.info(resumo)
    enviar_notificacao_telegram(resumo)

if __name__ == "__main__":
    save_data()

