# pylint: disable=too-few-public-methods,missing-class-docstring
"""Database models."""


from __future__ import annotations


from datetime import datetime
from typing import TYPE_CHECKING
from tortoise import Model
from tortoise.fields import (
    IntField,
    CharField,
    TextField,
    BooleanField,
    DatetimeField,
    UUIDField,
    ReverseRelation,
    ForeignKeyField,
)
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import Field
from .helpers import truncate, PdtModel, base_model_config


if TYPE_CHECKING:
    from tortoise.queryset import QuerySet, QuerySetSingle


class TicketResponseOption(Model):
    """Response options for a specified response to a customer message."""

    name = CharField(max_length=25, pk=True)
    description = TextField()
    ticket_response = ForeignKeyField(
        "models.CustomerMessageResponse", null=True, related_name="options"
    )
    start_exchange = BooleanField(default=False)

    class PydanticMeta:
        exclude = ["ticket_response", "start_exchange"]


class CustomerMessageResponse(Model):
    """A response to a customer message dependending on its selected option."""

    id = IntField(pk=True)
    responds_to = ForeignKeyField("models.TicketResponseOption")
    message = TextField()


class CustomerMessage(Model):
    """A message from a customer to the customer service."""

    id = IntField(pk=True)
    message = TextField()
    ticket = ForeignKeyField("models.Ticket", related_name="customer_messages")
    option = ForeignKeyField("models.TicketResponseOption")
    time = DatetimeField(auto_now_add=True)

    class PydanticMeta:
        exclude = ["id", "option"]


class Ticket(Model):
    """A ticket (a full exchange) to the ticket support."""

    id = IntField(pk=True)
    owner = ForeignKeyField("models.User", related_name="tickets")
    customer_messages: ReverseRelation["CustomerMessage"]

    def last_customer_message(self) -> QuerySetSingle[CustomerMessage]:
        """
        Returns:
            CustomerMessage: The last ``CustomerMessage`` related to that ticket.
        """
        return self.customer_messages.order_by("-time").first()

    class PydanticMeta:
        exclude = ["owner"]


class User(Model):
    """An API user."""

    id = UUIDField(pk=True)
    username = CharField(30, unique=True)
    password_hash = CharField(max_length=128)
    send_secret_message = BooleanField(default=False)
    tickets = ReverseRelation["Ticket"]

    class PydanticMeta:
        exclude = ["password_hash", "send_secret_message"]


async def response_of_customer_message(
    customer_message: CustomerMessage,
) -> CustomerMessageResponse:
    """Get the customer service response of a customer message.

    Args:
        customer_message (CustomerMessage): the customer message.

    Returns:
        CustomerMessageResponse: the response of that customer message.
    """
    return await CustomerMessageResponse.get(responds_to=await customer_message.option)


async def ticket_available_options(ticket: Ticket) -> QuerySet[TicketResponseOption]:
    """
    Get the available response options for a ticket.

    Args:
        ticket (Ticket): A ticket.

    Returns:
        QuerySet[TicketResponseOption]: A ``QuerySet`` of available response options.
    """
    last_message = await ticket.last_customer_message()
    last_response = await response_of_customer_message(last_message)
    return TicketResponseOption.filter(ticket_response=last_response).all()


TicketOut = pydantic_model_creator(Ticket, model_config=base_model_config)


class TicketFullOut(PdtModel):
    """Complete informations about a ticket."""

    id: int
    last_message: str = Field(max_length=50)
    last_response: str = Field(max_length=50)
    date: datetime

    @classmethod
    async def from_tortoise_orm(cls, itm: Ticket) -> TicketFullOut:
        """
        Args:
            ticket (Ticket): a ``Ticket``.

        Returns:
            TicketOut: its corresponding ``TicketFullOut``.
        """
        last_message = await itm.last_customer_message()
        last_response = await response_of_customer_message(last_message)
        return cls(
            id=itm.id,
            date=last_message.time,
            last_message=truncate(last_message.message),
            last_response=truncate(last_response.message),
        )


class CustomerMessageOut(PdtModel):
    """Informations about a customer message and its response."""

    time: datetime
    message: str
    response: str
    selected_option: str

    @classmethod
    async def from_tortoise_orm(cls, itm: CustomerMessage) -> CustomerMessageOut:
        """
        Args:
            customer_message (CustomerMessage): a ``CustomerMessage``.

        Returns:
            CustomerMessageOut: its corresponding ``CustomerMessageOut``.
        """
        response = await response_of_customer_message(itm)
        return cls(
            message=itm.message,
            time=itm.time,
            response=response.message,
            selected_option=(await itm.option).description,
        )


TicketResponseOptionOut = pydantic_model_creator(
    TicketResponseOption, model_config=base_model_config
)
UserOut = pydantic_model_creator(User, model_config=base_model_config)
