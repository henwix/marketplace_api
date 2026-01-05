from dataclasses import dataclass


@dataclass
class CreateUserCommand:
    data: dict


@dataclass
class DeleteUserCommand:
    user_id: int | None


@dataclass
class UpdateUserCommand:
    user_id: int | None
    data: dict


@dataclass
class GetUserCommand:
    user_id: int | None


@dataclass
class SetPasswordUserCommand:
    user_id: int | None
    password: str
