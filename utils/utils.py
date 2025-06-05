import logging
from datetime import datetime, timezone, timedelta
import pytz
from urllib.parse import quote


def configurar_logs():
    logging.basicConfig(
        level=logging.INFO,  # ou DEBUG se quiser mais detalhes
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


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


def formatar_relatorio(hora_atual, pendentes, faturados, cancelados):
    linhas = [
        f"*📄 Relatório de pedidos*",
        f"{hora_atual} - {mes_ano_tual()}",
        f"*• Pendentes:* `{pendentes}`",
        f"*• Faturados:* `{faturados}`",
        f"*• Cancelados:* `{cancelados}`"
    ]

    conteudo = "\n".join(linhas)
    return conteudo


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


def converter_data_iso_para_br(data_iso: str) -> str:
    """Converte data em ISO 8601 para formato brasileiro com fuso de Brasília."""
    try:
        if '+' in data_iso:
            parte_data, parte_fuso = data_iso.split('+')
            parte_data = parte_data[:26]  # até microssegundos
            data_iso_corrigido = f"{parte_data}+{parte_fuso}"
        else:
            data_iso_corrigido = data_iso

        dt = datetime.fromisoformat(data_iso_corrigido)
        dt_brasilia = dt.astimezone(timezone(timedelta(hours=-3)))
        return dt_brasilia.strftime('%d/%m/%Y %H:%M:%S')

    except Exception as e:
        logging.error(f"❌ Erro ao converter data ISO '{data_iso}': {e}")
        return "Data inválida"


def formatar_pedido_pendente(pedido_data) -> str:
    """Formata uma mensagem de pedido pendente para envio via Telegram."""
    orderid, creationdate, clientname, totalvalue, totalitems, statusdescription = pedido_data
    data_formatada = converter_data_iso_para_br(creationdate)
    return (
        "----------- Pedido Pendente -----------\n"
        f"Pedido: {orderid}\n"
        f"Data: {data_formatada}\n"
        f"Cliente: {clientname}\n"
        f"Valor: {totalvalue}\n"
        f"Quantidade: {totalitems}\n"
        f"Status: {statusdescription}\n"
    )


def obter_intervalo_data_atual(vtex_date_format) -> str:
    """Retorna o intervalo do primeiro dia do mês até agora no formato da VTEX"""
    hoje = datetime.utcnow()
    primeiro_dia_mes = hoje.replace(day=1)

    inicio = primeiro_dia_mes.strftime(vtex_date_format)
    fim = hoje.strftime(vtex_date_format)

    intervalo = f"creationDate:[{inicio} TO {fim}]"
    return quote(intervalo)
