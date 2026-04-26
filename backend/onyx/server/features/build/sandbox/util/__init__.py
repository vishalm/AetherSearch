"""Template and configuration utilities for sandbox environments.

Contains utilities for:
- Building sandbox templates (Next.js, venv)
- Generating agent instructions (AGENTS.md)
- Generating opencode configuration
"""

from aethersearch.server.features.build.sandbox.util.agent_instructions import (
    build_knowledge_sources_section,
)
from aethersearch.server.features.build.sandbox.util.agent_instructions import (
    build_skills_section,
)
from aethersearch.server.features.build.sandbox.util.agent_instructions import (
    build_user_context,
)
from aethersearch.server.features.build.sandbox.util.agent_instructions import (
    extract_skill_description,
)
from aethersearch.server.features.build.sandbox.util.agent_instructions import (
    generate_agent_instructions,
)
from aethersearch.server.features.build.sandbox.util.agent_instructions import (
    get_provider_display_name,
)
from aethersearch.server.features.build.sandbox.util.opencode_config import (
    build_opencode_config,
)

__all__ = [
    "build_knowledge_sources_section",
    "build_opencode_config",
    "build_skills_section",
    "build_user_context",
    "extract_skill_description",
    "generate_agent_instructions",
    "get_provider_display_name",
]
