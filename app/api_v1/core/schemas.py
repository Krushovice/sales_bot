from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    tg_id: int
    cost: int = None
    balance: int = None
    referrals: list | None


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdate(UserCreate):
    pass


class ProductUpdatePartial(UserCreate):
    username: str | None = None
    tg_id: int | None = None
    cost: int = None
    balance: int = None
    referrals: list | None
