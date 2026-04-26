from typing import cast

from ee.aethersearch.configs.app_configs import GATED_TENANTS_KEY
from aethersearch.configs.constants import AETHERSEARCH_CLOUD_TENANT_ID
from aethersearch.redis.redis_pool import get_redis_client
from aethersearch.redis.redis_pool import get_redis_replica_client
from aethersearch.server.settings.models import ApplicationStatus
from aethersearch.server.settings.store import load_settings
from aethersearch.server.settings.store import store_settings
from aethersearch.utils.logger import setup_logger
from shared_configs.contextvars import CURRENT_TENANT_ID_CONTEXTVAR

logger = setup_logger()


def update_tenant_gating(tenant_id: str, status: ApplicationStatus) -> None:
    redis_client = get_redis_client(tenant_id=AETHERSEARCH_CLOUD_TENANT_ID)

    # Maintain the GATED_ACCESS set
    if status == ApplicationStatus.GATED_ACCESS:
        redis_client.sadd(GATED_TENANTS_KEY, tenant_id)
    else:
        redis_client.srem(GATED_TENANTS_KEY, tenant_id)


def store_product_gating(tenant_id: str, application_status: ApplicationStatus) -> None:
    try:
        token = CURRENT_TENANT_ID_CONTEXTVAR.set(tenant_id)

        settings = load_settings()
        settings.application_status = application_status
        store_settings(settings)

        # Store gated tenant information in Redis
        update_tenant_gating(tenant_id, application_status)

        if token is not None:
            CURRENT_TENANT_ID_CONTEXTVAR.reset(token)

    except Exception:
        logger.exception("Failed to gate product")
        raise


def overwrite_full_gated_set(tenant_ids: list[str]) -> None:
    redis_client = get_redis_client(tenant_id=AETHERSEARCH_CLOUD_TENANT_ID)

    pipeline = redis_client.pipeline()

    # using pipeline doesn't automatically add the tenant_id prefix
    full_gated_set_key = f"{AETHERSEARCH_CLOUD_TENANT_ID}:{GATED_TENANTS_KEY}"

    # Clear the existing set
    pipeline.delete(full_gated_set_key)

    # Add all tenant IDs to the set and set their status
    for tenant_id in tenant_ids:
        pipeline.sadd(full_gated_set_key, tenant_id)

    # Execute all commands at once
    pipeline.execute()


def get_gated_tenants() -> set[str]:
    redis_client = get_redis_replica_client(tenant_id=AETHERSEARCH_CLOUD_TENANT_ID)
    gated_tenants_bytes = cast(set[bytes], redis_client.smembers(GATED_TENANTS_KEY))
    return {tenant_id.decode("utf-8") for tenant_id in gated_tenants_bytes}


def is_tenant_gated(tenant_id: str) -> bool:
    """Fast O(1) check if tenant is in gated set (multi-tenant only)."""
    redis_client = get_redis_replica_client(tenant_id=AETHERSEARCH_CLOUD_TENANT_ID)
    return bool(redis_client.sismember(GATED_TENANTS_KEY, tenant_id))
