PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

dev:
	poetry run flask --app page_analyzer:app run --debug

install:
	poetry install

update:
	poetry update

build:
	poetry build

check:
	poetry check

lint:
	poetry run flake8 .
