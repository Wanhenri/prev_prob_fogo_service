# 🔥 prev\_prob\_fogo\_service

Sistema de previsão de probabilidade de fogo utilizando FastAPI e Python 3.12.

---

## 📦 Estrutura Inicial do Projeto

```bash
poetry new prev_prob_fogo
cd prev_prob_fogo
```

Estrutura gerada:

```
prev_prob_fogo/
├── prev_prob_fogo/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── poetry.lock
└── README.md
```

---

## ⚙️ Configuração do Ambiente

### ✅ Versão do Python

O projeto utiliza **Python 3.12.10**. Recomenda-se o uso do `pyenv`:

```bash
pyenv local 3.12.10
```

### ✅ pyproject.toml

Atualize as dependências principais para:

```toml
[tool.poetry.dependencies]
python = "3.12.*"
fastapi = {extras = ["standard"], version = "^0.115.14"}
```

### ✅ Instalação de Dependências

```bash
poetry install
```

Isso gerará o arquivo `poetry.lock` automaticamente.

---

## 🚀 Executando a Aplicação

Ative o ambiente virtual com:

```bash
poetry shell
```

E execute o servidor:

```bash
fastapi dev prev_prob_fogo/app.py
```

---

## 📚 Documentação da API

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧠 Ferramentas e Qualidade de Código

### 🧹 Ruff (Lint + Formatter)

Instalação:

```bash
poetry add --group dev ruff
```

#### Configuração no `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
extend-exclude = ['migrations']

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

#### Comandos úteis:

```bash
ruff check .             # Verifica erros de lint
ruff check . --fix       # Corrige automaticamente
ruff format .            # Formata com aspas simples
```

📄 Documentação: [https://docs.astral.sh/ruff](https://docs.astral.sh/ruff)

---

### ✅ Pytest (Testes)

Instalação:

```bash
poetry add --group dev pytest pytest-cov
```

#### Configuração:

```toml
[tool.pytest.ini_options]
pythonpath = ''
addopts = '-p no:warnings'
```

---

### 🧪 Taskipy (Scripts automatizados)

Instalação:

```bash
poetry add --group dev taskipy
```

#### Configuração:

```toml
[tool.taskipy.tasks]
run = 'fastapi dev prev_prob_fogo/app.py'
test = 'pytest --cov=prev_prob_fogo -vv'
post_test = 'coverage html'
lint = 'ruff check . && ruff check . --diff'
format = 'ruff check . --fix && ruff format'

# Para uso com cadeia de testes:
pre_test = 'task lint'
test = 'pytest --cov=prev_prob_fogo -vv'
post_test = 'coverage html'
```

> 🔁 **Observação para Linux**: troque `&&` por `;` caso necessário.

📈 Listar tasks disponíveis:

```bash
task --list
```

---

## 📽️ .gitignore

Gere um `.gitignore` para Python com:

```bash
pipx install ignr
ignr -p python > .gitignore
```

---

## 🔗 GitHub

Inicialize o repositório e conecte ao GitHub:

```bash
git init
git remote add origin https://github.com/Wanhenri/prev_prob_fogo_service.git
git push --set-upstream origin main
```

---

## ✅ Resumo da Cadeia de Comandos

```bash
task lint
task test
task format
```

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---
