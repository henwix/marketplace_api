from drf_spectacular.utils import OpenApiExample


def _build_token_error_401_response_example(action: str) -> OpenApiExample:
    return OpenApiExample(
        name=f'Token is {action} error',
        response_only=True,
        status_codes=[401],
        value={
            'detail': 'Given token not valid for any token type',
            'code': 'token_not_valid',
            'messages': [
                {
                    'token_class': 'AccessToken',
                    'token_type': 'access',
                    'message': f'Token is {action}',
                },
            ],
        },
    )


def unauthorized_token_invalid_error_401_response_example() -> OpenApiExample:
    return _build_token_error_401_response_example(action='invalid')


def unauthorized_token_expired_error_401_response_example() -> OpenApiExample:
    return _build_token_error_401_response_example(action='expired')
