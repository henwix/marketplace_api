from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class CreateSellerCommand:
    user_id: int | None
    name: str
    description: str | None = None


@dataclass(frozen=True, eq=False)
class UpdateSellerCommand:
    user_id: int | None
    name: str | None = None
    description: str | None = None


@dataclass(frozen=True, eq=False)
class DeleteSellerCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class GetSellerCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class GetSellerByIdCommand:
    seller_id: int
