from punq import Container

from src.apps.authentication.services.auth import AuthValidatorService, BaseAuthValidatorService


def init_auth(container: Container) -> None:
    # services
    container.register(BaseAuthValidatorService, AuthValidatorService)
