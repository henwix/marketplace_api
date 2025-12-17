from dataclasses import dataclass


@dataclass
class BaseEntity:
    def update_from_data(self, data: dict) -> None:
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
