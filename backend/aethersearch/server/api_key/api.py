from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from aethersearch.auth.permissions import require_permission
from aethersearch.db.api_key import ApiKeyDescriptor
from aethersearch.db.api_key import fetch_api_keys
from aethersearch.db.api_key import insert_api_key
from aethersearch.db.api_key import regenerate_api_key
from aethersearch.db.api_key import remove_api_key
from aethersearch.db.api_key import update_api_key
from aethersearch.db.engine.sql_engine import get_session
from aethersearch.db.enums import Permission
from aethersearch.db.models import User
from aethersearch.server.api_key.models import APIKeyArgs

router = APIRouter(prefix="/admin/api-key")


@router.get("")
def list_api_keys(
    _: User = Depends(require_permission(Permission.FULL_ADMIN_PANEL_ACCESS)),
    db_session: Session = Depends(get_session),
) -> list[ApiKeyDescriptor]:
    return fetch_api_keys(db_session)


@router.post("")
def create_api_key(
    api_key_args: APIKeyArgs,
    user: User = Depends(require_permission(Permission.FULL_ADMIN_PANEL_ACCESS)),
    db_session: Session = Depends(get_session),
) -> ApiKeyDescriptor:
    return insert_api_key(db_session, api_key_args, user.id)


@router.post("/{api_key_id}/regenerate")
def regenerate_existing_api_key(
    api_key_id: int,
    _: User = Depends(require_permission(Permission.FULL_ADMIN_PANEL_ACCESS)),
    db_session: Session = Depends(get_session),
) -> ApiKeyDescriptor:
    return regenerate_api_key(db_session, api_key_id)


@router.patch("/{api_key_id}")
def update_existing_api_key(
    api_key_id: int,
    api_key_args: APIKeyArgs,
    _: User = Depends(require_permission(Permission.FULL_ADMIN_PANEL_ACCESS)),
    db_session: Session = Depends(get_session),
) -> ApiKeyDescriptor:
    return update_api_key(db_session, api_key_id, api_key_args)


@router.delete("/{api_key_id}")
def delete_api_key(
    api_key_id: int,
    _: User = Depends(require_permission(Permission.FULL_ADMIN_PANEL_ACCESS)),
    db_session: Session = Depends(get_session),
) -> None:
    remove_api_key(db_session, api_key_id)
