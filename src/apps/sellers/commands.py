from dataclasses import dataclass


@dataclass
class CreateSellerCommand:
    user_id: int | None
    data: dict


@dataclass
class DeleteSellerCommand:
    user_id: int | None


@dataclass
class UpdateSellerCommand:
    user_id: int | None
    data: dict


@dataclass
class GetSellerCommand:
    user_id: int | None


@dataclass
class GetSellerByIdCommand:
    seller_id: int
