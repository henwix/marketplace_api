.PHONY: all

DC = docker compose
LOGS = docker logs
EXEC = docker exec -it
APP_DEV_FILE = docker_compose/backend.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = mp-backend-dev
MANAGE_PY = python manage.py
ENV = --env-file .env


app:
	${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} up --build -d

app-logs:
	${LOGS} ${APP_CONTAINER} -f

app-down:
	${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} down

app-restart:
	${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} down && ${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} up --build -d

app-shell:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} shell_plus

makemigrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic

test:
	${EXEC} ${APP_CONTAINER} pytest
