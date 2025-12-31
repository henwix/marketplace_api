from logging import Logger

import orjson
from rest_framework import status
from rest_framework.views import Response, exception_handler

from src.apps.common.exceptions import ServiceException
from src.project.containers import resolve_depends


def api_exception_handler(exc, context):
    if isinstance(exc, ServiceException):
        logger: Logger = resolve_depends(Logger)
        logger.error(msg=exc.message, extra={'log_meta': orjson.dumps(exc).decode()})
        return Response(data=exc.response(), status=exc.status_code)

    response = exception_handler(exc, context)
    if response is not None:
        return response

    logger: Logger = resolve_depends(Logger)
    logger.error(
        msg='Unhandled exception',
        exc_info=exc,
        extra={'log_meta': orjson.dumps({'exception': exc.__class__.__name__, 'detail': str(exc)}).decode()},
    )
    return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
