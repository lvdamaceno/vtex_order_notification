# 🛒 VTEX Order Notification Bot

Um sistema automatizado que consulta pedidos da plataforma VTEX e envia alertas via Telegram quando há pedidos pendentes de faturamento.

---

## 🚀 Objetivo

O projeto foi desenvolvido para empresas que utilizam a VTEX como plataforma de e-commerce e precisam de um monitoramento **em tempo real** dos pedidos que **ainda não foram faturados**.

> Ao detectar pedidos com status pendente, o bot envia uma notificação para um grupo ou usuário específico no Telegram.

---

## ⚙️ Tecnologias utilizadas

- **Python 3.9**
- [VTEX API](https://developers.vtex.com/docs/api)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- `requests`, `dotenv`, `logging`
- `pytest` para testes automatizados

---

## 🗂 Estrutura de Pastas

```bash
vetx_order_notification/
├── main.py                          # Script principal de execução
├── .env                             # Variáveis de ambiente (não subir no Git!)
├── requirements.txt                 # Bibliotecas necessárias
├── pytest.ini                       # Configuração do pytest
├── render.yaml                      # Configuração para deploy na Render
├── vtex/                            # Módulo com funções de integração com a VTEX
│   ├── __init__.py
│   └── vtex_api.py
├── utils/                           # Funções auxiliares (horário, relatórios, etc.)
│   ├── __init__.py
│   └── utils.py
├── notifications/                  # Módulo de notificações via Telegram
│   ├── __init__.py
│   └── telegram.py
├── tests/                           # Testes automatizados
│   ├── test_env_vars.py
│   ├── test_api_vtex_real.py
│   ├── test_telegram_real.py
│   └── __init__.py
└── logs/                            # (gerado em runtime) arquivos de log do dia
```

---

## ✅ O que o bot faz?

1. Consulta a API da VTEX e coleta todos os pedidos do mês atual.
2. Filtra pedidos com status diferente de "faturado" ou "cancelado".
3. Envia mensagens personalizadas no Telegram com os dados do pedido.
4. Gera e envia um resumo com o total de pedidos pendentes, faturados e cancelados.
5. Exibe logs informativos no console (ou arquivo se configurado).

---

## 📦 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/vetx_order_notification.git
cd vetx_order_notification
```

### 2. Crie um ambiente virtual

```bash
python3.9 -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

Crie um arquivo `.env` com:

```env
URL=https://sualoja.vtexcommercestable.com.br/api/oms/pvt/orders
APPKEY=sua_app_key
APPTOKEN=seu_token
BOTTOKEN=token_do_bot_telegram
CHATID=id_do_chat_telegram
```

### 5. Execute o bot

```bash
python main.py
```

---

## 🧪 Testes

Execute todos os testes:

```bash
pytest -v
```

Execute somente testes que fazem requisições reais:

```bash
pytest -m realapi -v
```

---

## 📤 Deploy (Render)

Este projeto possui um arquivo `render.yaml` para deploy na plataforma [Render](https://render.com/), permitindo agendamento automático com `cron`.

---

## ✨ Futuras melhorias

- Integração com outras plataformas (como Discord, WhatsApp API)

---

## 📄 Licença

MIT © Vinicius Damaceno
