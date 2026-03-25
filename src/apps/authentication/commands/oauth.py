from dataclasses import dataclass


@dataclass
class OAuthGetLoginUrlCommand:
    provider: str


@dataclass
class OAuthVerifyCommand:
    user_id: int | None
    code: str
    state: str
    provider: str
