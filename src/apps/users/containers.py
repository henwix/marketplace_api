from punq import Container

from src.apps.users.repositories.users import BaseUserRepository, ORMUserRepository
from src.apps.users.services.users import (
    BaseUserService,
    UserService,
)
from src.apps.users.use_cases.create import CreateUserUseCase
from src.apps.users.use_cases.delete import DeleteUserUseCase
from src.apps.users.use_cases.get import GetUserUseCase
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from src.apps.users.use_cases.update import UpdateUserUseCase


def init_users(container: Container) -> None:
    # use cases
    container.register(CreateUserUseCase)
    container.register(GetUserUseCase)
    container.register(UpdateUserUseCase)
    container.register(DeleteUserUseCase)
    container.register(SetPasswordUserUseCase)

    # services
    container.register(BaseUserService, UserService)

    # repositories
    container.register(BaseUserRepository, ORMUserRepository)
