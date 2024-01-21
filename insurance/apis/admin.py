"""Admin API."""


from __future__ import annotations


from fastapi import Depends, Path, HTTPException
from ..api_setup import new_api
from ..auth import get_user
from ..models import User


api = new_api(
    title="ASSURTOUT TICKETING ADMINISTRATION API",
    version="1.0",
    dependencies=[Depends(get_user(["admin"]))],
)


async def get_user_from_id(user_id: str = Path(alias="user_id")) -> User:
    """
    Args:
        user_id (str, optional): Path(alias="user_id").

    Raises:
        HTTPException: 404 if user doesn't exists.

    Returns:
        User: the associated user.
    """
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(404)
    return user


@api.post("/{user_id}", response_model=None)
async def send_secret_message(user: User = Depends(get_user_from_id)):
    """Transmit secret message to the agent."""

    user.send_secret_message = True
    await user.save()
    return {"message": f"Sent message to {user.username}"}
