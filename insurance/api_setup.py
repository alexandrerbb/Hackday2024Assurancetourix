"""FastAPI setup."""


from __future__ import annotations


from fastapi import FastAPI, Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException, RequestValidationError


DEBUG: bool = False
# Turn this False on production.


def new_api(*args, **kwargs) -> FastAPI:
    """
    Returns:
        FastAPI: the configurated API.
    """
    kwargs["openapi_url"] = None  # Overwrite kwags.

    app = FastAPI(*args, responses={422: {}} | kwargs.pop("responses", {}), **kwargs)

    if not DEBUG:

        @app.exception_handler(RequestValidationError)
        async def handle_422(*__) -> Response:
            """Remove help on 422 exceptions."""
            return Response(status_code=422)  # No info leaks here.

        @app.get("/openapi.json", include_in_schema=False)
        async def get_openapi():
            """OpenAPI file follows the same authentication rules than other endpoints.
            So we have to re-define its route here."""
            return app.openapi()  # Fix empty `openapi_schema`.

        # A clue about the right OpenAPI file path.
        @app.get("/openapi.yml", include_in_schema=False)
        @app.get("/openapi.yaml", include_in_schema=False)
        async def get_openapi_file_path(request: Request):
            """Redirect to the correct OpenAPI file path."""
            api_path = request.scope["root_path"]
            if api_path is None or not isinstance(api_path, str):
                raise HTTPException(
                    500, "Cannot generate redirection for `/openapi.json` properly."
                )
                # If there is an error, it should give the clue anyway.
            return RedirectResponse(f"{api_path}/openapi.json", 301)

    return app
