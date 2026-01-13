from dataclasses import dataclass

from src.apps.common.types import UNSET


@dataclass
class BaseEntity:
    def update(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k) and v is not UNSET:
                setattr(self, k, v)
