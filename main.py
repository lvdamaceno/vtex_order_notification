import logging
from notifications.telegram import enviar_notificacao_telegram, notificar_pedidos_pendentes
from utils.utils import formatar_relatorio, obter_hora_atual, classificar_pedidos, configurar_logs
from vtex.vtex_api import consumir_api_vtex


def verificar_pedidos_pendentes_vtex():
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
        resumo = formatar_relatorio(hora_atual, len(pendentes), len(faturados), len(cancelados))
        logging.info(resumo)
        enviar_notificacao_telegram(resumo)
    except Exception as e:
        logging.error(f"Erro ao formatar ou enviar resumo: {e}")


if __name__ == "__main__":
    configurar_logs()
    verificar_pedidos_pendentes_vtex()
