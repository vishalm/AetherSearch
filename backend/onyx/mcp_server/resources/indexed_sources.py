"""Resources that expose metadata for the AetherSearch MCP server."""

from __future__ import annotations

import json

from aethersearch.mcp_server.api import mcp_server
from aethersearch.mcp_server.utils import get_indexed_sources
from aethersearch.mcp_server.utils import require_access_token
from aethersearch.utils.logger import setup_logger

logger = setup_logger()


@mcp_server.resource(
    "resource://indexed_sources",
    name="indexed_sources",
    description=(
        "Enumerate the user's document sources that are currently indexed in AetherSearch."
        "This can be used to discover filters for the `search_indexed_documents` tool."
    ),
    mime_type="application/json",
)
async def indexed_sources_resource() -> str:
    """Return the list of indexed source types for search filtering."""

    access_token = require_access_token()

    sources = await get_indexed_sources(access_token)

    logger.info(
        "AetherSearch MCP Server: indexed_sources resource returning %s entries",
        len(sources),
    )

    # FastMCP 3.2+ requires str/bytes/list[ResourceContent] — it no longer
    # auto-serializes; serialize to JSON ourselves.
    return json.dumps(sorted(sources))
