from dataclasses import dataclass

from src.apps.common.types import UNSET


@dataclass
class BaseEntity:
    def update_from_data(self, data: dict) -> None:
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def update(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k) and v is not UNSET:
                setattr(self, k, v)
