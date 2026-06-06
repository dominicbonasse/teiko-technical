VENV_BIN = .venv/bin
PYTHON = $(VENV_BIN)/python
PIP = $(VENV_BIN)/pip
STREAMLIT = $(VENV_BIN)/streamlit

.PHONY: setup pipeline dashboard

setup:
	python -m venv .venv
	$(PIP) install -r requirements.txt

pipeline:
	$(PYTHON) load_data.py
	$(PYTHON) analyze.py

dashboard:
	$ streamlit run app.py