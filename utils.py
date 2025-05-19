from datetime import datetime

def mes_ano_tual():
    agora = datetime.now()
    meses_pt = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
    }
    mes_atual = datetime.now().month
    ano = str(agora.year)[-2:]
    mes = meses_pt[mes_atual].capitalize()
    resp = f"{mes}/{ano}"
    return resp

def formatar_relatorio_com_pre(hora_atual, inseridos, atualizados, nao_modificados, ignorados):
    linhas = [
        f"Relatório de pedidos",
        f"{hora_atual} - {mes_ano_tual()}",
        f"➤ Inseridos:     {inseridos}",
        f"➤ Atualizados:   {atualizados}",
        f"➤ Faturados:     {nao_modificados}",
        f"➤ Cancelados:    {ignorados}"
    ]

    conteudo = "\n".join(linhas)
    return f"<pre>{conteudo}</pre>"
