from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from sqlalchemy.orm import Session

from aethersearch.auth.permissions import require_permission
from aethersearch.auth.users import current_curator_or_admin_user
from aethersearch.background.celery.versioned_apps.client import app as client_app
from aethersearch.configs.app_configs import DISABLE_VECTOR_DB
from aethersearch.configs.constants import AetherSearchCeleryPriority
from aethersearch.configs.constants import AetherSearchCeleryTask
from aethersearch.db.document_set import check_document_sets_are_public
from aethersearch.db.document_set import delete_document_set as db_delete_document_set
from aethersearch.db.document_set import fetch_all_document_sets_for_user
from aethersearch.db.document_set import get_document_set_by_id
from aethersearch.db.document_set import insert_document_set
from aethersearch.db.document_set import mark_document_set_as_to_be_deleted
from aethersearch.db.document_set import update_document_set
from aethersearch.db.engine.sql_engine import get_session
from aethersearch.db.enums import Permission
from aethersearch.db.models import User
from aethersearch.server.features.document_set.models import CheckDocSetPublicRequest
from aethersearch.server.features.document_set.models import CheckDocSetPublicResponse
from aethersearch.server.features.document_set.models import DocumentSetCreationRequest
from aethersearch.server.features.document_set.models import DocumentSetSummary
from aethersearch.server.features.document_set.models import DocumentSetUpdateRequest
from aethersearch.utils.variable_functionality import fetch_ee_implementation_or_noop
from shared_configs.contextvars import get_current_tenant_id

router = APIRouter(prefix="/manage")


@router.post("/admin/document-set")
def create_document_set(
    document_set_creation_request: DocumentSetCreationRequest,
    user: User = Depends(current_curator_or_admin_user),
    db_session: Session = Depends(get_session),
    tenant_id: str = Depends(get_current_tenant_id),
) -> int:
    fetch_ee_implementation_or_noop(
        "aethersearch.db.user_group", "validate_object_creation_for_user", None
    )(
        db_session=db_session,
        user=user,
        target_group_ids=document_set_creation_request.groups,
        object_is_public=document_set_creation_request.is_public,
        object_is_new=True,
    )
    try:
        document_set_db_model, _ = insert_document_set(
            document_set_creation_request=document_set_creation_request,
            user_id=user.id,
            db_session=db_session,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not DISABLE_VECTOR_DB:
        client_app.send_task(
            AetherSearchCeleryTask.CHECK_FOR_VESPA_SYNC_TASK,
            kwargs={"tenant_id": tenant_id},
            priority=AetherSearchCeleryPriority.HIGH,
        )

    return document_set_db_model.id


@router.patch("/admin/document-set")
def patch_document_set(
    document_set_update_request: DocumentSetUpdateRequest,
    user: User = Depends(current_curator_or_admin_user),
    db_session: Session = Depends(get_session),
    tenant_id: str = Depends(get_current_tenant_id),
) -> None:
    document_set = get_document_set_by_id(db_session, document_set_update_request.id)
    if document_set is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document set {document_set_update_request.id} does not exist",
        )

    fetch_ee_implementation_or_noop(
        "aethersearch.db.user_group", "validate_object_creation_for_user", None
    )(
        db_session=db_session,
        user=user,
        target_group_ids=document_set_update_request.groups,
        object_is_public=document_set_update_request.is_public,
        object_is_owned_by_user=user
        and (document_set.user_id is None or document_set.user_id == user.id),
    )
    try:
        update_document_set(
            document_set_update_request=document_set_update_request,
            db_session=db_session,
            user=user,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not DISABLE_VECTOR_DB:
        client_app.send_task(
            AetherSearchCeleryTask.CHECK_FOR_VESPA_SYNC_TASK,
            kwargs={"tenant_id": tenant_id},
            priority=AetherSearchCeleryPriority.HIGH,
        )


@router.delete("/admin/document-set/{document_set_id}")
def delete_document_set(
    document_set_id: int,
    user: User = Depends(current_curator_or_admin_user),
    db_session: Session = Depends(get_session),
    tenant_id: str = Depends(get_current_tenant_id),
) -> None:
    document_set = get_document_set_by_id(db_session, document_set_id)
    if document_set is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document set {document_set_id} does not exist",
        )

    # check if the user has "edit" access to the document set.
    # `validate_object_creation_for_user` is poorly named, but this
    # is the right function to use here
    fetch_ee_implementation_or_noop(
        "aethersearch.db.user_group", "validate_object_creation_for_user", None
    )(
        db_session=db_session,
        user=user,
        object_is_public=document_set.is_public,
        object_is_owned_by_user=user
        and (document_set.user_id is None or document_set.user_id == user.id),
    )

    try:
        mark_document_set_as_to_be_deleted(
            db_session=db_session,
            document_set_id=document_set_id,
            user=user,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if DISABLE_VECTOR_DB:
        db_session.refresh(document_set)
        db_delete_document_set(document_set, db_session)
    else:
        client_app.send_task(
            AetherSearchCeleryTask.CHECK_FOR_VESPA_SYNC_TASK,
            kwargs={"tenant_id": tenant_id},
            priority=AetherSearchCeleryPriority.HIGH,
        )


"""Endpoints for non-admins"""


@router.get("/document-set")
def list_document_sets_for_user(
    user: User = Depends(require_permission(Permission.BASIC_ACCESS)),
    db_session: Session = Depends(get_session),
    get_editable: bool = Query(
        False, description="If true, return editable document sets"
    ),
) -> list[DocumentSetSummary]:
    document_sets = fetch_all_document_sets_for_user(
        db_session=db_session, user=user, get_editable=get_editable
    )
    return [DocumentSetSummary.from_model(ds) for ds in document_sets]


@router.get("/document-set-public")
def document_set_public(
    check_public_request: CheckDocSetPublicRequest,
    _: User = Depends(require_permission(Permission.BASIC_ACCESS)),
    db_session: Session = Depends(get_session),
) -> CheckDocSetPublicResponse:
    is_public = check_document_sets_are_public(
        document_set_ids=check_public_request.document_set_ids, db_session=db_session
    )
    return CheckDocSetPublicResponse(is_public=is_public)
