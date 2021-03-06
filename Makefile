FLASK_APP=party_wall/app.py

# migration message argument
message ?= ''


## INSTALLING DEPENDENCIES (FOR DEVELOPMENT)

install:
	pip install poetry
	poetry install

## STARTING BACKEND
start:
	docker-compose up

start-detached:
	docker-compose up -d


## DATABASE MANAGEMENT
dbinit:
	docker-compose run --rm backend flask db init

dbmigrate:
	docker-compose run --rm backend flask db migrate -m $(message)

dbupgrade:
	docker-compose run --rm backend flask db upgrade


## STATIC CODE ANALYSIS, LINTING, FORMATTING
lint:
	poetry run pylint party_wall

flake:
	poetry run flake8 party_wall --max-line-length=100

sort-imports:
	poetry run isort party_wall --multi-line VERTICAL_HANGING_INDENT --line-length 100

type-check:
	poetry run mypy party_wall

format:
 poetry run black --skip-string-normalization --line-length 100 party_wall
 poetry run autoflake --remove-all-unused-imports


# RUNNING TESTS, COVERAGE
test:
	poetry run pytest party_wall.tests

test-coverage:
	poetry run pytest party_wall.tests --cov --cov-report html --cov-report xml

test-unit:
	poetry run pytest party_wall.tests.unit

test-integration:
	poetry run pytest party_wall.tests.integration
