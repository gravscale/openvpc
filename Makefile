.PHONY: help alembic-revision alembic-current alembic-history alembic-apply run guidelines

help:
	@echo "Available commands:"
	@echo "alembic-revision MESSAGE - Creates an Alembic revision with the specified message"
	@echo "alembic-current - Shows the current Alembic revision"
	@echo "alembic-history - Shows the history of Alembic revisions"
	@echo "alembic-apply - Applies the latest Alembic revision"
	@echo "run - Runs the Uvicorn server"
	@echo "mysql - Connects to the MySQL database"
	@echo "guidelines - Shows the contribution guidelines for OpenVPC"

alembic-revision:
	cd openvpc && poetry run alembic revision --autogenerate -m "$(MESSAGE)"

alembic-current:
	cd openvpc && poetry run alembic current

alembic-history:
	cd openvpc && poetry run alembic history

alembic-apply:
	cd openvpc && poetry run alembic upgrade head

run:
	cd openvpc && poetry run uvicorn openvpc.main:app --host 0.0.0.0 --port 8000 --reload

mysql:
	$(eval include dev/.env)
	$(eval export $(shell sed 's/=.*//' dev/.env))
	mysql -h $(MYSQL_HOST) -u $(MYSQL_USERNAME) -p$(MYSQL_PASSWORD) $(MYSQL_DATABASE)

requirements:
	poetry export -f requirements.txt --output requirements.txt