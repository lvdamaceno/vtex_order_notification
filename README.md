
# VTEX API Order Tracker

Este projeto foi desenvolvido para consultar a API da VTEX, verificar novos pedidos e/ou atualizações, salvar os dados em um banco de dados SQLite local e disparar notificações no Telegram quando um novo pedido é registrado ou quando ocorre uma atualização.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos principais:

- **main.py**: Arquivo principal que consome a API da VTEX, salva ou atualiza os pedidos no banco de dados.
- **notification.py**: Envia notificações via Telegram sobre novos pedidos ou atualizações.
- **vtex_api.py**: Consome a API da VTEX para obter os dados dos pedidos.
- **vtex_db.py**: Realiza operações de banco de dados, como criar a tabela e inserir ou atualizar pedidos.

## Dependências

- Python 3.8 ou superior.
- Biblioteca `requests` para fazer as requisições HTTP.
- Biblioteca `sqlite3` para manipulação do banco de dados SQLite.
- Biblioteca `python-dotenv` para carregar variáveis de ambiente a partir de um arquivo `.env`.
- Biblioteca `tabulate` para exibir os dados de forma tabular no terminal.

Você pode instalar as dependências usando o seguinte comando:

```bash
pip install requests python-dotenv tabulate
```

## Como Usar

### Configuração do Ambiente

1. Clone ou baixe o repositório para o seu computador.
2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```bash
URL="URL_da_API_VTEX"
APPKEY="Sua_AppKey_VTEX"
APPTOKEN="Seu_AppToken_VTEX"
BOTTOKEN="Token_do_seu_bot_Telegram"
CHATID="ID_do_chat_do_destinatário"
```

- **URL**: URL da API da VTEX que será consumida para obter os pedidos.
- **APPKEY** e **APPTOKEN**: Credenciais da VTEX para autenticação.
- **BOTTOKEN** e **CHATID**: Credenciais do bot do Telegram para enviar notificações.

### Executando o Projeto

1. **Consome a API da VTEX e salva os pedidos no banco de dados**:

```bash
python main.py
```

2. **Consultar e exibir os pedidos no banco de dados** (opcional):

Você pode utilizar o código abaixo para realizar consultas no banco de dados SQLite e exibir os resultados no terminal:

```python
# Exemplo de consulta para contar o número de pedidos
query_db("SELECT COUNT(orderID) FROM orders ORDER BY orderId DESC;")

# Exemplo de consulta para exibir todos os pedidos
query_db("SELECT * FROM orders ORDER BY orderId DESC;")
```

## Funcionalidade do Projeto

- **Consulta de Pedidos**: A função `consumir_api_vtex()` no arquivo `vtex_api.py` consulta a API da VTEX e retorna os pedidos.
- **Armazenamento no Banco de Dados**: A função `update_or_insert_order()` no arquivo `vtex_db.py` insere ou atualiza os pedidos no banco de dados SQLite.
- **Notificações via Telegram**: A função `enviar_notificacao_telegram()` no arquivo `notification.py` envia uma mensagem ao Telegram quando um pedido é inserido ou atualizado.
- **Filtragem de Pedidos Cancelados**: O projeto ignora os pedidos que possuem o status "cancelado" no campo `statusDescription`.

## Exemplo de Notificação

Quando um novo pedido é registrado ou atualizado, o bot do Telegram envia uma notificação com informações como:

```
----------- Novo Pedido -----------
Pedido: 12345
Data: 25/04/2025 15:30:00
Cliente: João Silva
Valor: 150,00
Status: Pago
-----------------------------------
```

## Contribuindo

1. Faça um fork deste repositório.
2. Crie uma branch para a sua feature (`git checkout -b minha-feature`).
3. Faça commit das suas mudanças (`git commit -am 'Adicionando minha feature'`).
4. Push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.