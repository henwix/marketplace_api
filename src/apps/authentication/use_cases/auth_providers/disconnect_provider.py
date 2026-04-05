from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.commands.auth_providers import DisconnectAuthProviderCommand
from src.apps.authentication.exceptions.auth_providers import (
    AuthProvidersNotFoundError,
    UnableToDisconnectAuthProviderError,
)
from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.authentication.services.auth_providers import (
    BaseAuthProviderMustExistValidatorService,
    BaseAuthProviderService,
)
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class DisconnectAuthProviderUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService
    auth_provider_service: BaseAuthProviderService
    auth_provider_must_exist_validator_service: BaseAuthProviderMustExistValidatorService

    def execute(self, command: DisconnectAuthProviderCommand) -> None:
        self.auth_validator_service.validate(user_id=command.user_id)
        self.auth_provider_must_exist_validator_service.validate(provider=command.provider)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        with transaction.atomic():
            auth_providers = self.auth_provider_service.get_many_by_user_id_for_update(user_id=user.id)
            auth_providers_count = len(auth_providers)
            if auth_providers_count == 0:
                raise AuthProvidersNotFoundError
            if auth_providers_count == 1 and not user.has_usable_password:
                raise UnableToDisconnectAuthProviderError(provider=command.provider)
            self.auth_provider_service.try_delete_by_user_id_and_provider(user_id=user.id, provider=command.provider)
