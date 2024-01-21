"""Insurance Challenge."""


from __future__ import annotations


import logging
from typing import TYPE_CHECKING
from os import path
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware, cors
from starlette.responses import HTMLResponse
from tortoise.contrib.starlette import register_tortoise
from . import apis


if TYPE_CHECKING:
    from starlette.requests import Request


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s - %(levelname)s ] - %(message)s"
)


ROOT_DIR = path.dirname(path.abspath(__file__))


SPA_HTML_CONTENTS = ""


with open(
    path.join(ROOT_DIR, "static", "index.html"), "r", encoding="utf-8"
) as spa_html_file:
    SPA_HTML_CONTENTS = spa_html_file.read()


async def spa_html(__: Request):
    """Returns the HTML file for frontend app."""
    return HTMLResponse(SPA_HTML_CONTENTS)


# The challenge is made of several APIs to understand in order to solve it.
#
# The front ends gives basic informations about the API paths to try. Then the
# challenger should take a look in `openapi.json` endpoints to understand what API
# endpoints could be called.
app = Starlette(
    routes=[
        Mount("/apis/admin/v1", apis.admin_api, name="admin API"),
        Mount("/apis/auth/v1", apis.auth_api, name="auth API"),
        Mount("/apis/tickets/v1", apis.tickets_api, name="tickets API"),
        Mount(
            "/assets",
            app=StaticFiles(directory=path.join(ROOT_DIR, "static", "assets")),
            name="frontend",
        ),
        Route("/{path:path}", endpoint=spa_html),
    ],
    middleware=[
        Middleware(
            cors.CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)

register_tortoise(
    app,
    # db_url="postgres://user:azerty@localhost/database-challenge",
    db_url="sqlite://database.db",
    modules={"models": ["insurance.models"]},
    generate_schemas=False,
)  # We have cyclic foreign keys, schemas couldn't be generate automatically.
