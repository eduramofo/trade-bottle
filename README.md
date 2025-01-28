# Trade Bottle

Day Trade BOT

## 1. Requirements dev

```bash
python -m pip install --upgrade pip
python -m pip install pip-tools
pip-compile --strip-extras
pip install -r requirements-dev.txt
```

## 2. CMDs

```bash
# Pega os dados
python data.py

# Limpa dos dados
python clean.py 

# Analise os dados
python analyze.py

# Server
python server.py
```
