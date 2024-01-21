"""APIs."""


from .admin import api as admin_api
from .auth import api as auth_api
from .tickets import api as tickets_api


__all__ = ["admin_api", "auth_api", "tickets_api"]
