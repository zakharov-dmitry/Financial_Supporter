from datetime import timedelta, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt

from config import settings
from infastructure.oauth2 import OAuth2PasswordBearerWithCookie
from models.user import User
# from services.user_service import authenticate_user, get_user_by_email
from user_service import get_user_by_email, authenticate_user

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

router = APIRouter()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.post("/token", include_in_schema=False)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    # TODO: is the string needed???
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user_from_cookies(request: Request):
    access_token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(access_token)
    # scheme will hold "Bearer" and param will hold actual token value
    try:
        payload = jwt.decode(token=param, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    return username


async def validate_current_user_from_token(request: Request) -> Optional[User]:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials invalid")
    access_token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(access_token)
    # scheme will hold "Bearer" and param will hold actual token value
    try:
        payload = jwt.decode(token=param, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(email=username)
    if user is None:
        raise credentials_exception
    return user


def logout_delete_token(response: Response):
    response.delete_cookie("access_token")