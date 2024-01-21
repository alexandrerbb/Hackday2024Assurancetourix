"""API authentication."""


from __future__ import annotations


from typing import TYPE_CHECKING
from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from ..api_setup import new_api
from ..models import User, UserOut
from ..auth import authenticate_user, create_user, create_jwt, get_user
from ..helpers import base_model_config


if TYPE_CHECKING:
    from ..auth import JWTUserInformations


ROLES_API_PATHS = {"customer": "/apis/tickets/v1/", "admin": "/apis/admin/v1/"}
"""Accessible api paths depending on the user roles."""


api = new_api(title="ASSURTOUT API AUTH", version="1.0")


class AccessTokenResponse(BaseModel):
    """An API response containing basic informations about the user and a JWT access
    token."""

    model_config = base_model_config
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserCredentialsIn(BaseModel):
    """Input to login/register (to) a specific user account."""

    username: str = Field(max_length=36)
    password: str = Field()


@api.post("/login", response_model=None)
async def login(user_credentials: UserCredentialsIn):
    """Login with specified credentials."""
    if user := await authenticate_user(
        **user_credentials.model_dump(exclude_unset=True)
    ):
        return AccessTokenResponse(
            access_token=create_jwt(str(user.id)),
            user=await UserOut.from_tortoise_orm(user),
        )
        # We craft a "bruteforce-able" JWT.
        # The subscriber is the UUID of the user. So challengers cannot craft tokens in
        # order to access to other teams' accounts (they are not allowed to enumerate
        # users' UUIDs).
    raise HTTPException(401, "bad credentials.")


@api.post("/register", response_model=None)
async def register(user_credentials: UserCredentialsIn):
    """Register a new user."""
    if await User.exists(username=user_credentials.username):
        raise HTTPException(403, f"user `{user_credentials.username}` already exists.")
    user = await create_user(**user_credentials.model_dump(exclude_unset=True))
    return await UserOut.from_tortoise_orm(user)


# Here is a clue about what API can be called by the user depending on its user roles.
@api.get("/informations", response_model=None)
async def user_inforamations(
    user_data: JWTUserInformations = Depends(get_user(["customer", "admin"]))
) -> UserOut:
    """Get basic user informations and list reachable APIs for this user."""
    authorized_api_paths = {ROLES_API_PATHS.get(role, None) for role in user_data.roles}
    if None in authorized_api_paths:
        authorized_api_paths.remove(None)
    return (await UserOut.from_tortoise_orm(user_data.user)).model_dump() | {
        "authorizedApiPaths": authorized_api_paths
    }
