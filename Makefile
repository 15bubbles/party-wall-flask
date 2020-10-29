FLASK_APP=party_wall/app.py

install:
	pip install poetry
	poetry install

start:
	docker-compose up

dbinit:
	poetry run flask db init

dbmigrate:
	poetry run flask db migrate

dbupgrade:
	poetry run flask db upgrade

lint:
	poetry run pylint party_wall --max-line-length=100

typing:
	poetry run mypy party_wall 

format:
 poetry run black --skip-string-normalization --line-length 100 party_wall

test:
	poetry run pytest party_wall.tests
