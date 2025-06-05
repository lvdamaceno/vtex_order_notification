import logging
from datetime import datetime
import pytz

from notifications.telegram import enviar_notificacao_telegram
from notification import formatar_pedido_pendente
from utils import formatar_relatorio_com_pre
from vtex_api import consumir_api_vtex

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def obter_hora_atual() -> str:
    """Retorna a hora atual no fuso horário de São Paulo."""
    fuso_br = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_br).strftime("%H:%M")


def classificar_pedidos(orders: list) -> tuple:
    """Classifica os pedidos em pendentes, faturados e cancelados."""
    pendentes = [pedido for pedido in orders if pedido["status"] not in ("invoiced", "canceled")]
    faturados = [pedido for pedido in orders if pedido["status"] == "invoiced"]
    cancelados = [pedido for pedido in orders if pedido["status"] == "canceled"]
    return pendentes, faturados, cancelados


def notificar_pedidos_pendentes(pedidos: list) -> None:
    """Envia notificação para cada pedido pendente."""
    for pedido in pedidos:
        try:
            valor_em_centavos = pedido["totalValue"] * 0.01
            totalvalue = f"R$ {valor_em_centavos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            mensagem = formatar_pedido_pendente(
                pedido["orderId"],
                pedido["creationDate"],
                pedido["clientName"],
                totalvalue,
                pedido["totalItems"],
                pedido["statusDescription"]
            )
            enviar_notificacao_telegram(mensagem)
        except Exception as e:
            logging.error(f"Erro ao notificar pedido {pedido.get('orderId', 'desconhecido')}: {e}")


def verificar_pedidos_vtex():
    """Função principal para verificar e notificar pedidos da VTEX."""
    try:
        orders = consumir_api_vtex()
    except Exception as e:
        logging.error(f"Erro ao consumir API VTEX: {e}")
        enviar_notificacao_telegram("⚠️ Erro ao acessar a API da VTEX.")
        return

    hora_atual = obter_hora_atual()

    if not orders:
        logging.info("🚫 Nenhum pedido retornado pela API.")
        return

    pendentes, faturados, cancelados = classificar_pedidos(orders)

    if not pendentes:
        logging.info("❌ Nenhum pedido pendente.")
        enviar_notificacao_telegram("❌ Nenhum pedido pendente no VTEX")
        return

    notificar_pedidos_pendentes(pendentes)

    try:
        resumo = formatar_relatorio_com_pre(hora_atual, len(pendentes), len(faturados), len(cancelados))
        logging.info(resumo)
        enviar_notificacao_telegram(resumo)
    except Exception as e:
        logging.error(f"Erro ao formatar ou enviar resumo: {e}")


if __name__ == "__main__":
    verificar_pedidos_vtex()
