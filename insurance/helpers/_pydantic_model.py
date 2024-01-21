"""A pydantic base model for custom ORM objects' corresponding pydantic models."""


from __future__ import annotations


from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from pydantic import BaseModel
from ._pydantic_config import base_model_config


if TYPE_CHECKING:
    from tortoise import Model
    from tortoise.queryset import QuerySet


class PdtModel(BaseModel, ABC):
    """A pydantic base model for custom tortoise pydantic models."""

    model_config = base_model_config

    @classmethod
    @abstractmethod
    async def from_tortoise_orm(cls, itm: type[Model]) -> type[PdtModel]:
        """From tortoise ORM object."""

    @classmethod
    async def from_queryset(cls, qs: QuerySet[type[Model]]) -> list[type[PdtModel]]:
        """
        Args:
            qs (QuerySet[type[Model]]): a ``QuerySet`` of ORM objects.

        Returns:
            list[type[PdtModel]]: its corresponding pydantic models.
        """
        return [(await cls.from_tortoise_orm(ticket)) for ticket in await qs]
