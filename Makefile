#!/usr/bin/env bash

create-venv:
	python3 -m venv .env

update-requirements:
	pip freeze > ./requirements.txt

make-fixtures:
	python3 manage.py loaddata location/fixtures/2018-04-01-locations.json

make-migrations:
	python3 manage.py makemigrations
	python3 manage.py migrate

pip-install:
	pip install -r ./requirements.txt

run:
	python3 manage.py runserver 0.0.0.0:8081
