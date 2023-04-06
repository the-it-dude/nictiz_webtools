##
# Mapping Tool API
#
# @file
# @version 0.1


deps-base:
	pip-compile app/requirements/base.in --output-file=app/requirements/base.txt

deps-prod:
	pip-compile app/requirements/prod.in --output-file=app/requirements/prod.txt

deps-dev:
	pip-compile app/requirements/dev.in --output-file=app/requirements/dev.txt

deps-docs:
	pip-compile app/requirements/docs.in --output-file=app/requirements/docs.txt

deps: deps-base deps-prod deps-dev deps-docs

build: deps-dev
	pip install -r app/requirements/dev.txt

install:
	pip install -r app/requirements/dev.txt

install-docs:
	pip install -r app/requirements/docs.txt

serve:
	python manage.py runserver

serve-docker:
	docker-compose up

test:
	pytest --ds=app.settings.test

build-docs:
	cd docs && make html
# end
