from uuid import UUID

from celery import shared_task
from celery import Task

from ee.aethersearch.background.celery_utils import should_perform_chat_ttl_check
from aethersearch.configs.app_configs import JOB_TIMEOUT
from aethersearch.configs.constants import AetherSearchCeleryTask
from aethersearch.db.chat import delete_chat_session
from aethersearch.db.chat import get_chat_sessions_older_than
from aethersearch.db.engine.sql_engine import get_session_with_current_tenant
from aethersearch.server.settings.store import load_settings
from aethersearch.utils.logger import setup_logger

logger = setup_logger()


@shared_task(
    name=AetherSearchCeleryTask.PERFORM_TTL_MANAGEMENT_TASK,
    ignore_result=True,
    soft_time_limit=JOB_TIMEOUT,
    bind=True,
    trail=False,
)
def perform_ttl_management_task(
    self: Task, retention_limit_days: int, *, tenant_id: str  # noqa: ARG001
) -> None:
    task_id = self.request.id
    if not task_id:
        raise RuntimeError("No task id defined for this task; cannot identify it")

    user_id: UUID | None = None
    session_id: UUID | None = None
    try:
        with get_session_with_current_tenant() as db_session:

            old_chat_sessions = get_chat_sessions_older_than(
                retention_limit_days, db_session
            )

        for user_id, session_id in old_chat_sessions:
            try:
                with get_session_with_current_tenant() as db_session:
                    delete_chat_session(
                        user_id,
                        session_id,
                        db_session,
                        include_deleted=True,
                        hard_delete=True,
                    )
            except Exception:
                logger.exception(
                    "Failed to delete chat session "
                    f"user_id={user_id} session_id={session_id}, "
                    "continuing with remaining sessions"
                )

    except Exception:
        logger.exception(
            f"delete_chat_session exceptioned. user_id={user_id} session_id={session_id}"
        )
        raise


@shared_task(
    name=AetherSearchCeleryTask.CHECK_TTL_MANAGEMENT_TASK,
    ignore_result=True,
    soft_time_limit=JOB_TIMEOUT,
)
def check_ttl_management_task(*, tenant_id: str) -> None:
    """Runs periodically to check if any ttl tasks should be run and adds them
    to the queue"""

    settings = load_settings()
    retention_limit_days = settings.maximum_chat_retention_days
    with get_session_with_current_tenant() as db_session:
        if should_perform_chat_ttl_check(retention_limit_days, db_session):
            perform_ttl_management_task.apply_async(
                kwargs=dict(
                    retention_limit_days=retention_limit_days, tenant_id=tenant_id
                ),
            )
