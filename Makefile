PY?=.venv/bin/python
PIP?=.venv/bin/pip

.PHONY: help init install run clean

help:
	@echo "make init     # create venv and install dependencies"
	@echo "make install  # install dependencies into existing .venv"
	@echo "make run      # run the app (uses .venv)"
	@echo "make clean    # remove created files (database.db, .venv)"

init:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install:
	$(PIP) install -r requirements.txt

run:
	$(PY) -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

clean:
	rm -rf .venv database.db
