##
# Mapping Tool API
#
# @file
# @version 0.1


deps:
	pip install pip-tools
	pip-compile app/requirements/base.in --output-file=app/requirements/base.txt

deps-dev:
	pip install pip-tools
	pip-compile app/requirements/dev.in --output-file=app/requirements/dev.txt

build: deps-dev
	pip install -r app/requirements/dev.txt

install:
	pip install -r app/requirements/dev.txt

serve:
	python manage.py runserver

test:
	pytest --ds=app.settings.test
# end
