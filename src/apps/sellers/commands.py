from dataclasses import dataclass

from src.apps.common.commands import BaseUpdateCommand
from src.apps.common.types import UNSET, Unset


@dataclass(frozen=True, eq=False)
class CreateSellerCommand:
    user_id: int | None
    name: str
    description: str


@dataclass(frozen=True, eq=False)
class UpdateSellerCommand(BaseUpdateCommand):
    user_id: int | None
    name: str | Unset = UNSET
    description: str | Unset = UNSET


@dataclass(frozen=True, eq=False)
class DeleteSellerCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class GetSellerCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class GetSellerByIdCommand:
    seller_id: int
