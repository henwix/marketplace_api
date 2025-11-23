DC = docker compose
LOGS = docker logs
EXEC = docker exec -it
APP_DEV_FILE = docker_compose/backend.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = mp-backend-dev
MANAGE_PY = python manage.py
ENV = --env-file .env


.PHONY: app
app:
	${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} down

.PHONY: app-restart
app-restart:
	${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} down && ${DC} -f ${APP_DEV_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} shell_plus

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest
