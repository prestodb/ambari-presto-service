.PHONY: clean-pyc clean-build clean-test test clean help

help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove test artifacts"
	@echo "test - run all unit tests located in the tests directory"
	@echo "clean - remove all files and folders that are not checked into the repo"
	@echo "dist - package and build integration code in a tar.gz"
	@echo "help - display this help menu"

clean: clean-pyc clean-build clean-test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	rm -fr build/
	rm -fr dist/

clean-test:
	rm -rf .tox/

test: clean-test
	tox -- -s tests

dist: clean-build clean-pyc
	python setup.py bdist
	ls -l dist