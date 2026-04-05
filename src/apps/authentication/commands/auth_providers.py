from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class GetConnectedAuthProvidersCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class DisconnectAuthProviderCommand:
    user_id: int | None
    provider: str
