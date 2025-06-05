import pytest
from notification import enviar_notificacao_telegram


def test_envio_telegram_simples():
    """
    Teste real: envia uma mensagem para o Telegram usando o bot configurado no .env.
    O teste passa se não houver erro e a API responder com sucesso (HTTP 200).
    """
    mensagem = "🔔 Teste direto com Pytest sem flags - VTEX integração"
    sucesso = enviar_notificacao_telegram(mensagem)

    assert sucesso is not None, "❌ A função não retornou resultado"
    assert sucesso is True, "❌ A mensagem não foi enviada com sucesso"
