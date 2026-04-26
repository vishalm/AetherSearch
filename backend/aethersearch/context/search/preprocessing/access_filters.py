from sqlalchemy.orm import Session

from aethersearch.access.access import get_acl_for_user
from aethersearch.context.search.models import IndexFilters
from aethersearch.db.models import User


def build_access_filters_for_user(user: User, session: Session) -> list[str]:
    user_acl = get_acl_for_user(user, session)
    return list(user_acl)


def build_user_only_filters(user: User, db_session: Session) -> IndexFilters:
    user_acl_filters = build_access_filters_for_user(user, db_session)
    return IndexFilters(
        source_type=None,
        document_set=None,
        time_cutoff=None,
        tags=None,
        access_control_list=user_acl_filters,
    )
