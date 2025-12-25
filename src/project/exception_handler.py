from logging import Logger

import orjson
from django.db.utils import settings
from punq import Container
from rest_framework import status
from rest_framework.views import Response, exception_handler

from src.apps.common.exceptions import ServiceException
from src.project.containers import get_container


def api_exception_handler(exc, context):
    if isinstance(exc, ServiceException):
        container: Container = get_container()
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exc.message, extra={'log_meta': orjson.dumps(exc).decode()})
        return Response(data=exc.response(), status=exc.status_code)

    response = exception_handler(exc, context)
    if response is not None:
        return response

    if settings.DEBUG is False:
        return Response(
            data={'detail': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
