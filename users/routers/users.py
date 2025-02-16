from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..schemas import users as user_schemas
from config.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
import random
import string
router = APIRouter(
    prefix="/users"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Hashing utility with bcrypt


SECRET_KEY = settings.SECRET_KEY
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {"admin@example.com": {
    "username": "Admin",
    "password": "$2b$12$xBKj2hTLP.1Adci6ujCtzeeOazCg5gSZUKQtoBo06AESD4E0jf.H.",  # admin
    "fullname": "Administrator",
    "email": "admin@example.com",
    "date_of_birth": "2000-03-02",
    "is_admin_user": True,
    "is_staff_user": True
}}
# users = {}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        settings.logger.exception("create access token error", str(e))
        raise HTTPException(status_code=500, detail="access token exception")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             settings.ALGORITHM])
        email: str = payload.get("sub")
        is_admin: str = payload.get("is_admin")
        print(payload)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_schemas.TokenData(email=email, is_admin=is_admin)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(str(e))


def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.get("/about_me",  response_model=user_schemas.User, status_code=200)
def read_users_me(current_user: user_schemas.TokenData = Depends(get_current_user)):
    if current_user.email:
        if current_user.email in users:
            return users[current_user.email]
        else:
            raise HTTPException(status_code=404, detail="User not found")


@router.get("/generate_discount",  response_model=user_schemas.DiscountCouponData, status_code=200)
def generate_discount(current_user: user_schemas.TokenData = Depends(get_current_user)):
    if current_user.email:
        print(current_user)
        if current_user.is_admin:
            length = random.randint(8, 12)
            random_string = ''.join(random.choices(
                string.ascii_letters + string.digits, k=length))
            settings.unused_discount.append(random_string)
            return user_schemas.DiscountCouponData(coupon_code=random_string)
        else:
            raise HTTPException(
                status_code=403, detail="Only admin can generate discount")


@router.post("/", response_model=user_schemas.User, status_code=201)
def create_user(user: user_schemas.UserCreate):
    user.password = get_password_hash(user.password)
    user = user.model_dump()
    if user["email"] not in users:
        users.update({user["email"]: user})
    else:
        raise HTTPException(
            status_code=409, detail="User with existing email is already exist")
    return user


# @router.get("/", response_model=List[user_schemas.User], status_code=200)
# def read_users(skip: int = 0, limit: int = 10):
#     """
#     pagination in users dictionary
#     """
#     paged_user = {}
#     counter = 0
#     for ind, user in enumerate(users):
#         if ind < skip:
#             continue
#         paged_user.update({user:users[user]})
#         counter += 1
#         if counter > limit:
#             break
#         # users = db.query(user_model.User).offset(skip).limit(limit).all()
#     return paged_user


@router.get("/{email}", response_model=user_schemas.User, status_code=200)
def read_user(email: str):
    if email in users:
        return users[email]
    else:
        raise HTTPException(status_code=404, detail="User not found")


# @router.put("/{email}", response_model=user_schemas.User)
# def update_user(email: str, user: user_schemas.UserUpdate, status_code=200):
#     if email in users:
#         for key in users[email]:
#             if user.model_dump().get(key, None) is not None:
#                 if key == "password":
#                     setattr(users[email], key, user.create_hashed_password())
#                     continue
#                 setattr(users[email], key, user.model_dump().get(key, ""))
#         return users[email]
#     else:
#         raise HTTPException(status_code=404, detail="User not found")


@router.post("/login", response_model=user_schemas.Token, status_code=200)
def login_user(login_user: OAuth2PasswordRequestForm = Depends()):
    user = None
    if login_user.username in users:
        user = users[login_user.username]
    else:
        for email in users:
            if login_user.username == users[email]["username"]:
                user = users[email]
                break
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect email/username or password")
    else:
        if verify_password(login_user.password, user["password"]):
            print(user)
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user["email"], "is_admin": user["is_admin_user"]}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=401, detail="Incorrect email/username or password")
