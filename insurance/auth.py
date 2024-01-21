# pylint: disable=raise-missing-from
"""API authentication functions."""


from datetime import datetime, timedelta
from typing import Callable, NamedTuple
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import TypeAdapter, ValidationError
from passlib.context import CryptContext
from jose import JWTError, jwt
from .models import User


WEAK_SECRET = "braxton300507thompson"
# This word is in rockyou. For this challenge, JWT tokens should be vulnerables to
# bruteforce.
ALGORITHM = "HS256"  # A symetric algorithm.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="register")

roles_type_adapter = TypeAdapter(list[str])
"""Pydantic validations for roles in JWT token."""


async def authenticate_user(username: "str", password: "str") -> "User | False":
    """Authenticate an ``User``.

    Args:
        username (str): the username.
        password (str): the password.

    Returns:
        User | False: False if no user found, else return the ``User`` instance.
    """
    user = await User.filter(username=username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password_hash):
        return False
    return user


async def create_user(username: "str", password: "str", **kwargs) -> "User":
    """Create a new ``User``.

    Args:
        username (str): the username.
        password (str): the password.

    Returns:
        Coroutine: the created user.
    """
    return await User.create(
        username=username, password_hash=pwd_context.hash(password), **kwargs
    )


class JWTUserInformations(NamedTuple):
    """Retrived user informations after decoding a JWT token."""

    user: User
    roles: list[str]


def get_user(roles: "list[str]") -> "Callable[..., JWTUserInformations]":
    """
    Returns a authentication / authorization function for a list of authorized roles.

    This function authenticates, check access roles and returns the specified user
    informations (``User`` object and its roles) depending on the JWT token specified in
    Authorization header.

    This function could be used in fastapi's ``Depends``.

    Args:
        roles (list, optional): A list of roles authorized to access the ressource.

    Raises:
        credentials_exception: If authentication failed.

    Returns:
        Callable[..., JWTUserInformations]: The function.
    """
    credentials_exception = HTTPException(
        401, "couldn't validate credentials (token is maybe timed out)."
    )

    async def getter(token: "str" = Depends(oauth2_scheme)) -> "JWTUserInformations":
        try:
            payload = jwt.decode(token, WEAK_SECRET, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub", None)
            if user_id is None:
                raise credentials_exception
            try:
                token_roles: list = roles_type_adapter.validate_python(
                    payload.get("roles")
                )
            except ValidationError:
                raise credentials_exception
            if len(set(roles) & set(token_roles)) == 0:
                # Check if user have a suffiscient role.
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await User.filter(id=user_id).first()
        if user is None:
            raise credentials_exception
        return JWTUserInformations(user, token_roles)

    return getter


def create_jwt(sub: "str") -> "str":
    """Encode a JWT for a specified subscriber.

    Args:
        sub (str): a subscriber.

    Returns:
        str: the JWT.
    """
    return jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "sub": sub,
            "roles": ["customer"],
        },
        WEAK_SECRET,
        algorithm=ALGORITHM,
    )
