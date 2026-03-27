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

## Estrutura

- main.py: inicializacao do aplicativo
- telas.py: logica das telas
- botoes.py: widgets customizados clicaveis
- main.kv e pasta kv/: layout das interfaces
