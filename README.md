# EAD Fracionado

Aplicacao desktop simples em Kivy para navegacao entre telas de login, criacao de conta e areas internas do sistema.

## Melhorias aplicadas

- limpeza da inicializacao do app e dos imports
- validacao basica de login e criacao de conta
- feedback visual nas telas para sucesso e erro
- ajuste dos widgets customizados para evitar conflito com o Button nativo do Kivy
- preenchimento inicial das telas Home e Box com estados vazios mais claros

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Login e Criacao de Conta com Databricks

O app agora pode autenticar usuarios e criar contas diretamente em uma tabela no Databricks SQL Warehouse.

Defina as variaveis de ambiente antes de rodar o app:

```bash
set DATABRICKS_SERVER_HOSTNAME=<seu-workspace>.cloud.databricks.com
set DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<warehouse-id>
set DATABRICKS_TOKEN=<seu-token>
set DATABRICKS_CATALOG=<catalogo-opcional>
set DATABRICKS_SCHEMA=<schema-opcional>
set DATABRICKS_USERS_TABLE=users
```

Estrutura esperada da tabela de usuarios:

```sql
CREATE TABLE IF NOT EXISTS users (
  email STRING,
  senha_hash STRING,
  senha_salt STRING,
  criado_em TIMESTAMP
)
USING DELTA;
```

Se `DATABRICKS_CATALOG` e `DATABRICKS_SCHEMA` forem preenchidos, a tabela sera lida como `catalog.schema.users`.

## Estrutura

- main.py: inicializacao do aplicativo
- telas.py: logica das telas
- auth_databricks.py: autenticacao e criacao de conta no Databricks
- botoes.py: widgets customizados clicaveis
- main.kv e pasta kv/: layout das interfaces
