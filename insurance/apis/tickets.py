"""Tickets API."""


from __future__ import annotations


from typing import TYPE_CHECKING
from fastapi import Depends, Body, HTTPException
from pydantic import BaseModel, Field
from ..api_setup import new_api
from ..models import (
    Ticket,
    CustomerMessage,
    TicketResponseOption,
    TicketFullOut,
    CustomerMessageOut,
    TicketOut,
    TicketResponseOptionOut,
    ticket_available_options,
)
from ..auth import get_user
from ..helpers import base_model_config
from .._secret import CHALLENGE_RESPONSE


if TYPE_CHECKING:
    from ..auth import JWTUserInformations


api = new_api(
    title="ASSURTOUT TICKETING API",
    version="1.0",
    dependencies=[Depends(get_user(["customer"]))],
)


async def get_ticket(
    ticket_id: str,
    user_data: JWTUserInformations = Depends(get_user(roles=["customer"])),
) -> Ticket:
    """
    Args:
        ticket_id (str): The ID of the ticket to request.
        user (JWTUserInformations): JWT informations about an user with the ``customer``
        role. By default, uses fastapi's ``Depends``.

    Raises:
        HTTPException: if ticket doesn't exist for the current user.

    Returns:
        Ticket: A ticket.
    """
    ticket = await Ticket.filter(owner=user_data.user, id=ticket_id).first()
    if not ticket:
        raise HTTPException(403)
    return ticket


class TicketInfoExchanges(BaseModel):
    """Ticket informations and exchanges with customer service."""

    model_config = base_model_config
    id: str
    messages: list[CustomerMessageOut]
    available_options: list[TicketResponseOptionOut]

    @classmethod
    async def from_ticket(cls, ticket: Ticket) -> TicketInfoExchanges:
        """Create a new instance from a ticket model.

        Args:
            ticket (Ticket): the ticket to create response from.

        Returns:
            TicketInfoExchanges: the class object (which corresponds to a response to a
            user).
        """
        return cls(
            id=str(ticket.id),
            messages=await CustomerMessageOut.from_queryset(
                CustomerMessage.filter(ticket=ticket).order_by("time").all()
            ),
            available_options=await TicketResponseOptionOut.from_queryset(
                await ticket_available_options(ticket)
            ),
        )


class TicketIn(BaseModel):
    """Input to create a ticket or answer to tickets' customer service messages."""

    message: str = Field(max_length=250, title="The message to send.")
    option: str = Field(max_length=25, title="The name of the selected option.")

    async def get_option(self, start: bool = False) -> TicketResponseOption:
        """Check if specified ticket response option exists and returns it.

        Args:
            start (bool, optional): If the option should be a "start" option. Defaults
            to False.

        Raises:
            HTTPException: if the specified option is not found.

        Returns:
            TicketResponseOption: The ticket response option.
        """
        option = await TicketResponseOption.filter(
            name=self.option, start_exchange=start
        ).first()
        if not option:
            raise HTTPException(403)
        return option


@api.get("/", response_model=None)
async def get_tickets(
    user_data: JWTUserInformations = Depends(get_user(roles=["customer"])),
):
    """Get users' tickets."""
    return await TicketFullOut.from_queryset(user_data.user.tickets)


@api.get("/start_options", response_model=None)
async def get_start_options():
    """Get options to create a ticket."""
    return await TicketResponseOptionOut.from_queryset(
        TicketResponseOption.filter(start_exchange=True).all()
    )


@api.get("/ticket/{ticket_id}", response_model=None)
async def get_ticket_informations(ticket=Depends(get_ticket)):
    """Get informations about a ticket."""
    return await TicketInfoExchanges.from_ticket(ticket)


@api.post("/new", response_model=None)
async def create_ticket(
    ticket_input: TicketIn = Body(...),
    user_data: JWTUserInformations = Depends(get_user(roles=["customer"])),
):
    """Create a new ticket."""
    user = user_data.user
    option = await ticket_input.get_option(True)
    if (
        await Ticket.filter(owner=user).count() >= 3
    ):  # User cannot have more than 3 tickets.
        ticket_to_delete = await Ticket.filter(owner=user).order_by("id").first()
        await ticket_to_delete.delete()

    ticket = await Ticket.create(owner=user)
    await CustomerMessage.create(
        ticket=ticket, message=ticket_input.message, option=option
    )
    return await TicketOut.from_tortoise_orm(ticket)


@api.post("/ticket/{ticket_id}", response_model=None)
async def answer_ticket(
    ticket_input: TicketIn = Body(...),
    ticket=Depends(get_ticket),
    user_data: JWTUserInformations = Depends(get_user(roles=["customer"])),
):
    """Answer to a specific ticket."""
    user = user_data.user
    available_options = {
        o[0] for o in await (await ticket_available_options(ticket)).values_list("name")
    }
    selected_option = await ticket_input.get_option()

    if not selected_option.name in available_options:
        raise HTTPException(404)
        # Sent option cannot be selected.
    await CustomerMessage.create(
        message=ticket_input.message, ticket=ticket, option=selected_option
    )
    response = await TicketInfoExchanges.from_ticket(ticket)
    if user.send_secret_message:
        user.send_secret_message = False
        await user.save()
        response.messages[-1].message = CHALLENGE_RESPONSE
    return response
