poetry new prev_prob_fogo
cd prev_prob_fogo

prev_prob_fogo
    __init__.py
poetry.lock
README.md
tests
    ___init__.py

Python utilizado no projeto: 3.12.10

Definir o python dentro do diretório prev_prob_fogo
pyenv local 3.12.10

Alteraçao no pyproject.toml

[tool.poetry.dependencies]
python = "3.12.*"

execute:
poetry install

e criará o poetry.lock

Instalado:
- FastAPI


poetry shell # ativa o venv

fastapi dev fast_zero/app.py

correção de um bug:

[tool.poetry.dependencies]
python = "3.12.*"
fastapi = {extras = ["standard"], version = "^0.115.14"}

poetry update

ou 

poetry add "fastapi[standard]"

O SWAGGER

http://localhost:8000/docs

O redoc

http://localhost:8000/redoc

Ferramentas

Ruff

poetry add --group dev ruff

****Configurando o ruff

[tool.ruff]
line-length = 79
extend-exclude = ['migrations]

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']

[tool.ruff.format]
preview = true
quote-style = 'single'

documentação do ruff
documentaçao PYQCA

ruff check . # verifica os erros
ruff check . --fix #Corrige os erros

ruff format . / #formatar as aspas duplas para aspas simples

****Pytest

poetry add --group dev pytest pytest-cov

[tool.pytest.ini_options]
pythonpath = ''
addopts = '-p no:warnings'

****Taskipy

ruff check .
ruff check . --fix
ruff format
fastapi dev prev_prob_fogo/app.py
pytest --cover=prev_prob_fogo -vv
coverage html

[tool.taskipy.tasks]
run = 'fastapi dev prev_prob_fogo/app.py'
test = 'pytest --cov=prev_prob_fogo -vv'
post_test = 'coverage html'
lint = 'ruff check . && ruff check . --diff'
format = 'ruff check . --fix && ruff format'

observaçao: usuario de linux pode trocar o '&&'por ';'

cadeia de comandos

pre_test = 'task lint'
test = 'pytest --cov=prev_prob_fogo -vv'
post_test = 'coverage html'

task --list

pipx install ignr

ignr -p python > .gitignore


git remote add origin https://github.com/Wanhenri/prev_prob_fogo_service.git
git push --set-upstream origin main