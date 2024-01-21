"""Custom workers for gunicorn."""


from __future__ import annotations


from uvicorn.workers import UvicornWorker


class CstmUvicornWorker(UvicornWorker):
    """Disable server header on unicorn workers."""

    def __init__(self, *args, **kwargs) -> None:
        self.CONFIG_KWARGS["server_header"] = False
        super().__init__(*args, **kwargs)
