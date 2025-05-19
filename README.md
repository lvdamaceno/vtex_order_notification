# VTEX Order Notification Bot

Este projeto consulta a API da VTEX OMS, analisa o status dos pedidos em tempo real, e envia notificações via Telegram com base nos dados recebidos — sem persistência local em banco de dados.

## ✨ O que mudou?

- ✅ **Remoção do SQLite**: A aplicação agora **não depende mais de banco de dados local**.
- 🔄 **Consulta contínua via API**: O estado dos pedidos é totalmente baseado na resposta da API VTEX.
- 📬 **Notificações Telegram**: São enviadas para novos pedidos pendentes ou mudanças de status.
- 📦 **Classificação de status**: Separação entre pedidos faturados, cancelados e pendentes diretamente na memória.
- 🕒 **Relatórios por horário**: Geração de relatórios com hora atual no fuso de Brasília (UTC−3).

## 📁 Estrutura Atual do Projeto

- `main.py`: Executa o controle principal, consulta a API e envia notificações.
- `notification.py`: Contém a função de envio para o Telegram.
- `vtex_api.py`: Requisições à API VTEX com paginação e filtros por data.
- `.env`: Arquivo com variáveis de ambiente (não incluído no controle de versão).

## ⚙️ Dependências

- Python 3.8+
- `requests`
- `python-dotenv`
- `tabulate` (opcional, para logs no terminal)

```bash
pip install requests python-dotenv tabulate
```

## 🔧 Como usar

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/vtex-order-tracker.git
```

2. Crie um `.env` com:

```env
URL="https://SEU_LOJA.vtexcommercestable.com.br/api/oms/pvt/orders"
APPKEY="sua-appkey"
APPTOKEN="seu-apptoken"
BOTTOKEN="token_do_bot"
CHATID="id_do_chat"
```

3. Execute:
```bash
python main.py
```

## 🛠️ Funcionalidades

- Consulta pedidos do mês atual
- Filtro por pedidos pendentes (`status` diferente de `invoiced` e `canceled`)
- Agrupamento de pedidos por status
- Envio individual ou em lote para Telegram
- Uso de fuso horário brasileiro com `pytz` para marcar relatórios

## 🔔 Exemplo de notificação

```
----------- Novo Pedido -----------
Pedido: 12345
Data: 25/04/2025 15:30
Cliente: João Silva
Valor: R$ 150,00
Status: Aguardando pagamento
-----------------------------------
```

## 🤝 Contribuição

1. Faça um fork
2. Crie uma branch (`git checkout -b minha-feature`)
3. Commit (`git commit -m 'feat: minha melhoria'`)
4. Push (`git push origin minha-feature`)
5. Abra um Pull Request 🚀