from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext


class UserBase(BaseModel):
    username: str
    password: str
    fullname: str
    email: str
    date_of_birth: datetime
    is_admin_user: Optional[bool] = False
    is_staff_user: Optional[bool] = False

    @field_validator("password")
    def password_length(cls, v):
        if len(v) <= 4:
            raise ValidationError(
                "Password length must be greater than 4 characters")
        return v


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    email: Optional[str] = None
    is_admin_user: Optional[bool] = None
    is_staff_user: Optional[bool] = None


class UserDelete(BaseModel):
    id: int


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


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