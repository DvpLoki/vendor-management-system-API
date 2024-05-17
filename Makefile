freeze:
	pip freeze > requirements.txt

venv:
	python -m venv venv

run:
	python manage.py runserver

m:
	python manage.py makemigrations && python manage.py migrate

test:
	pytest -v

d-build:
	docker build --tag vendor-api .
d-run:
	docker run  vendor-api

dc-up:
	docker-compose up --build	

schema:
	python manage.py spectacular --file schema.yml
db-graph:
	python manage.py graph_models  -o docs/models.dot

.PHONY: freeze venv run m test d-build d-run dc-up schema db-graph
