import pytest
from vtex_api import consumir_api_vtex


def test_conexao_real_com_api_vtex():
    """
    Teste de integração: garante que a chamada real à API VTEX
    retorna uma lista válida de pedidos do mês atual.
    """
    pedidos = consumir_api_vtex()

    assert pedidos is not None, "❌ A função retornou None — erro na comunicação ou autenticação."
    assert isinstance(pedidos, list), "❌ A resposta não é uma lista."

    if pedidos:
        pedido = pedidos[0]
        assert "orderId" in pedido, "❌ 'orderId' não encontrado no pedido."
        assert "creationDate" in pedido, "❌ 'creationDate' não encontrado no pedido."
        assert "status" in pedido, "❌ 'status' não encontrado no pedido."

    print(f"✅ Teste passou: {len(pedidos)} pedidos retornados.")
