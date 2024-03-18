.PHONY: help run test mysql requirements aerich-init aerich-init-db aerich-migrate aerich-upgrade aerich-downgrade

help:
	@echo "Available commands:"
	@echo "run - Runs the Uvicorn server."
	@echo "test - Runs the Pytest tests."
	@echo "mysql - Connects to the MySQL database."
	@echo "requirements - Exports the requirements to requirements.txt."
	@echo "aerich-init TEXT - Init config file and generate root migrate location."
	@echo "aerich-init-db - Generate schema and generate app migrate location."
	@echo "aerich-migrate - Generate migrate changes file."
	@echo "aerich-upgrade - Upgrade to specified version."
	@echo "aerich-downgrade - Downgrade to specified version."

run:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --proxy-headers

test:
	poetry run pytest -v .

mysql:
	$(eval include .env)
	$(eval export $(shell sed 's/=.*//' .env))
	mysql -h $(MYSQL_HOST) -u $(MYSQL_USERNAME) -p$(MYSQL_PASSWORD) $(MYSQL_DATABASE)

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls

aerich-init:
	poetry run aerich init -t $(TEXT)

aerich-init-db:
	poetry run aerich init-db

aerich-migrate:
	poetry run aerich migrate

aerich-upgrade:
	poetry run aerich upgrade

aerich-downgrade:
	poetry run aerich downgrade
