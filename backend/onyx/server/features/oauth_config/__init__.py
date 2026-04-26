"""OAuth configuration feature module."""

from aethersearch.server.features.oauth_config.api import admin_router
from aethersearch.server.features.oauth_config.api import router

__all__ = ["admin_router", "router"]
