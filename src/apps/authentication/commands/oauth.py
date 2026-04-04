from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class OAuthGetLoginUrlCommand:
    provider: str


@dataclass(frozen=True, eq=False)
class OAuthVerifyCommand:
    user_id: int | None
    code: str
    state: str
    provider: str


@dataclass(frozen=True, eq=False)
class OAuthGetConnectedProvidersCommand:
    user_id: int | None
