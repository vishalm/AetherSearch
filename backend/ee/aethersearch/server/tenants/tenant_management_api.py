from fastapi import APIRouter
from fastapi import Depends

from ee.aethersearch.server.tenants.models import TenantByDomainResponse
from ee.aethersearch.server.tenants.provisioning import get_tenant_by_domain_from_control_plane
from aethersearch.auth.permissions import require_permission
from aethersearch.auth.users import User
from aethersearch.db.enums import Permission
from aethersearch.utils.logger import setup_logger
from shared_configs.contextvars import get_current_tenant_id

logger = setup_logger()

router = APIRouter(prefix="/tenants")

FORBIDDEN_COMMON_EMAIL_SUBSTRINGS = [
    "gmail",
    "outlook",
    "yahoo",
    "hotmail",
    "icloud",
    "msn",
    "hotmail",
    "hotmail.co.uk",
]


@router.get("/existing-team-by-domain")
def get_existing_tenant_by_domain(
    user: User = Depends(require_permission(Permission.BASIC_ACCESS)),
) -> TenantByDomainResponse | None:
    domain = user.email.split("@")[1]
    if any(substring in domain for substring in FORBIDDEN_COMMON_EMAIL_SUBSTRINGS):
        return None

    tenant_id = get_current_tenant_id()

    return get_tenant_by_domain_from_control_plane(domain, tenant_id)
