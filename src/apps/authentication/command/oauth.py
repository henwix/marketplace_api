from dataclasses import dataclass


@dataclass
class OAuthGetUrlCommand:
    provider: str
