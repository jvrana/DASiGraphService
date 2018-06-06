PIP=pip3

.PHONY: docs  # necessary so it doesn't look for 'docs/makefile html'


init:
	$(PIP) install pipenv --upgrade
	pipenv install --dev --skip-lock
	pipenv lock --requirements > requirements.txt
	pipenv lock --dev --requirements > requirements_dev.txt


build:
#	pipenv lock --requirements > requirements.txt
#	pipenv lock --dev --requirements > requirements_dev.txt
	docker build . --tag dasigraphservice:testing


clean:
	rm -rf __pycache_
	rm -rf tests/__pycache__


cleanpycharmdocker:
	docker images | grep "pycharm" | awk '{print $$3}' | xargs docker rmi -f


test:
	pipenv run python -m pytest


pylint:
	pipenv run python -m pylint -E DASiGraph