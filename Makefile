SHELL := /bin/bash
.PHONY: run
PYTHONPATH=.

run:
	find -name '*.pyc' -delete
	find -name __pycache__ -delete
	python src/main.py
