"""Persona mapping utility for demo user identities and org structure.

Maps frontend persona selections (work_area + level) to demo user profiles
with name and email for sandbox provisioning.

Also provides organizational structure data and content generators for org_info files.
Single source of truth for both local and Kubernetes sandbox provisioning.
"""

from typing import TypedDict


class PersonaInfo(TypedDict):
    """Type for persona information."""

    name: str
    email: str


# Persona mapping: work_area -> level -> PersonaInfo
PERSONA_MAPPING: dict[str, dict[str, PersonaInfo]] = {
    "engineering": {
        "ic": {
            "name": "Jiwon Kang",
            "email": "jiwon_kang@netherite-extraction.aethersearch.app",
        },
        "manager": {
            "name": "Javier Morales",
            "email": "javier_morales@netherite-extraction.aethersearch.app",
        },
    },
    "sales": {
        "ic": {
            "name": "Megan Foster",
            "email": "megan_foster@netherite-extraction.aethersearch.app",
        },
        "manager": {
            "name": "Valeria Cruz",
            "email": "valeria_cruz@netherite-extraction.aethersearch.app",
        },
    },
    "product": {
        "ic": {
            "name": "Michael Anderson",
            "email": "michael_anderson@netherite-extraction.aethersearch.app",
        },
        "manager": {
            "name": "David Liu",
            "email": "david_liu@netherite-extraction.aethersearch.app",
        },
    },
    "marketing": {
        "ic": {
            "name": "Rahul Patel",
            "email": "rahul_patel@netherite-extraction.aethersearch.app",
        },
        "manager": {
            "name": "Olivia Reed",
            "email": "olivia_reed@netherite-extraction.aethersearch.app",
        },
    },
    "executives": {
        "ic": {
            "name": "Sarah Mitchell",
            "email": "sarah_mitchell@netherite-extraction.aethersearch.app",
        },
        "manager": {
            "name": "Sarah Mitchell",
            "email": "sarah_mitchell@netherite-extraction.aethersearch.app",
        },
    },
    "other": {
        "manager": {
            "name": "Ralf Schroeder",
            "email": "ralf_schroeder@netherite-extraction.aethersearch.app",
        },
        "ic": {
            "name": "John Carpenter",
            "email": "john_carpenter@netherite-extraction.aethersearch.app",
        },
    },
}

# Organization structure - maps managers to their direct reports
ORGANIZATION_STRUCTURE: dict[str, dict[str, list[str]]] = {
    "engineering": {
        "javier_morales@netherite-extraction.aethersearch.app": [
            "tyler_jenkins@netherite-extraction.aethersearch.app",
            "jiwon_kang@netherite-extraction.aethersearch.app",
            "brooke_spencer@netherite-extraction.aethersearch.app",
            "andre_robinson@netherite-extraction.aethersearch.app",
        ],
        "isabella_torres@netherite-extraction.aethersearch.app": [
            "ryan_murphy@netherite-extraction.aethersearch.app",
            "jason_morris@netherite-extraction.aethersearch.app",
            "kevin_sullivan@netherite-extraction.aethersearch.app",
        ],
    },
    "sales": {
        "valeria_cruz@netherite-extraction.aethersearch.app": [
            "megan_foster@netherite-extraction.aethersearch.app",
            "mina_park@netherite-extraction.aethersearch.app",
            "james_choi@netherite-extraction.aethersearch.app",
            "camila_vega@netherite-extraction.aethersearch.app",
        ],
        "layla_farah@netherite-extraction.aethersearch.app": [
            "arjun_mehta@netherite-extraction.aethersearch.app",
            "sneha_reddy@netherite-extraction.aethersearch.app",
            "irene_shen@netherite-extraction.aethersearch.app",
        ],
    },
    "product": {
        "david_liu@netherite-extraction.aethersearch.app": [
            "michael_anderson@netherite-extraction.aethersearch.app",
            "kenji_watanabe@netherite-extraction.aethersearch.app",
            "sofia_ramirez@netherite-extraction.aethersearch.app",
        ],
    },
    "marketing": {
        "olivia_reed@netherite-extraction.aethersearch.app": [
            "rahul_patel@netherite-extraction.aethersearch.app",
            "yuna_lee@netherite-extraction.aethersearch.app",
            "peter_yamamoto@netherite-extraction.aethersearch.app",
        ],
    },
    "executives": {
        "sarah_mitchell@netherite-extraction.aethersearch.app": [
            "daniel_hughes@netherite-extraction.aethersearch.app",
            "amanda_brooks@netherite-extraction.aethersearch.app",
            "ananya_gupta@netherite-extraction.aethersearch.app",
        ],
    },
    "other": {
        "ralf_schroeder@netherite-extraction.aethersearch.app": [
            "john_carpenter@netherite-extraction.aethersearch.app",
        ],
    },
}

# AGENTS.md content for org_info directory
ORG_INFO_AGENTS_MD = """# AGENTS.md

This file provides information about which organizational information sources are available:

There are two files available that provide important information about the user's company and the user themselves.


## User Identity

The file `user_identity_profile.txt` contains the user's profile.

## Organizational Structure

The file `organization_structure.json` contains a json with the organization's groups, managers, and their reports.
"""


def get_persona_info(work_area: str | None, level: str | None) -> PersonaInfo | None:
    """Get persona info from work area and level.

    Args:
        work_area: User's work area (e.g., "engineering", "product", "sales")
        level: User's level (e.g., "ic", "manager")

    Returns:
        PersonaInfo with name and email, or None if no matching persona
    """
    if not work_area:
        return None

    work_area_lower = work_area.lower().strip()
    level_lower = (level or "manager").lower().strip()

    work_area_mapping = PERSONA_MAPPING.get(work_area_lower)
    if not work_area_mapping:
        return None

    return work_area_mapping.get(level_lower)


def generate_user_identity_content(persona: PersonaInfo) -> str:
    """Generate user identity profile content.

    Args:
        persona: PersonaInfo with name and email

    Returns:
        Content for user_identity_profile.txt
    """
    return f"Your name is {persona['name']}. Your email is {persona['email']}. You are working at Netherite Extraction Corp.\n"
