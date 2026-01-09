from punq import Container

from src.apps.users.repositories.users import BaseUserRepository, ORMUserRepository
from src.apps.users.services.users import (
    BaseUserService,
    BaseUserValidatorService,
    ComposedUserValidatorService,
    UserService,
    UserUniqueEmailValidatorService,
    UserUniquePhoneValidatorService,
)
from src.apps.users.use_cases.create import CreateUserUseCase
from src.apps.users.use_cases.delete import DeleteUserUseCase
from src.apps.users.use_cases.get import GetUserUseCase
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from src.apps.users.use_cases.update import UpdateUserUseCase


def init_users(container: Container) -> None:
    def _build_user_validator() -> BaseUserValidatorService:
        return ComposedUserValidatorService(
            validators=[
                container.resolve(UserUniqueEmailValidatorService),
                container.resolve(UserUniquePhoneValidatorService),
            ]
        )

    # use cases
    container.register(CreateUserUseCase)
    container.register(GetUserUseCase)
    container.register(UpdateUserUseCase)
    container.register(DeleteUserUseCase)
    container.register(SetPasswordUserUseCase)

    # services
    container.register(BaseUserService, UserService)
    container.register(UserUniqueEmailValidatorService)
    container.register(UserUniquePhoneValidatorService)
    container.register(BaseUserValidatorService, factory=_build_user_validator)

    # repositories
    container.register(BaseUserRepository, ORMUserRepository)
