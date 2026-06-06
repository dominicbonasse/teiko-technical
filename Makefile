VENV_BIN = .venv/Scripts
PYTHON = $(VENV_BIN)/python
PIP = $(VENV_BIN)/pip

.PHONY: setup pipeline dashboard

setup:
	python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

pipeline:
	$(PYTHON) load_data.py
	$(PYTHON) analyze.py

dashboard:
	$ streamlit run app.py