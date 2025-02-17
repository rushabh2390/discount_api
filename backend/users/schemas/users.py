from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext


class User(BaseModel):
    username: str
    password: str
    fullname: str
    email: str
    date_of_birth: datetime
    isadminuser: Optional[bool] = False
    isstaffuser: Optional[bool] = False

    @field_validator("password")
    def password_length(cls, v):
        if len(v) <= 4:
            raise ValidationError(
                "Password length must be greater than 4 characters")
        return v


class UserCreate(User):
    pass


class UserUpdate():
    username: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    email: Optional[str] = None
    isadminuser: Optional[bool] = None
    isstaffuser: Optional[bool] = None


class UserDelete(BaseModel):
    email: str


class UserLogin(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

    @field_validator("password")
    def password_length(cls, v):
        if len(v) <= 4:
            raise ValidationError(
                "Password length must be greater than 4 characters")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    is_admin: Optional[bool] = False


class DiscountCouponData(BaseModel):
    coupon_code: Optional[str] = None
