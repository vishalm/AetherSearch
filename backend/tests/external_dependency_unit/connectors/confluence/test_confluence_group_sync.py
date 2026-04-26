from typing import Any

from sqlalchemy.orm import Session

from ee.aethersearch.external_permissions.confluence.group_sync import confluence_group_sync
from aethersearch.configs.constants import DocumentSource
from aethersearch.connectors.models import InputType
from aethersearch.db.enums import AccessType
from aethersearch.db.enums import ConnectorCredentialPairStatus
from aethersearch.db.models import Connector
from aethersearch.db.models import ConnectorCredentialPair
from aethersearch.db.models import Credential
from shared_configs.contextvars import get_current_tenant_id
from tests.daily.connectors.confluence.models import ExternalUserGroupSet

# In order to get these tests to run, use the credentials from Bitwarden.
# Search up "ENV vars for local and Github tests", and find the Confluence relevant key-value pairs.

_EXPECTED_CONFLUENCE_GROUPS = [
    ExternalUserGroupSet(
        id="confluence-admins-danswerai",
        user_emails={"chris@aethersearch.app", "yuhong@aethersearch.app"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="org-admins",
        user_emails={
            "founders@aethersearch.app",
            "chris@aethersearch.app",
            "yuhong@aethersearch.app",
            "oauth@aethersearch.app",
        },
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="confluence-users-danswerai",
        user_emails={
            "chris@aethersearch.app",
            "hagen@danswer.ai",
            "founders@aethersearch.app",
            "pablo@aethersearch.app",
            "yuhong@aethersearch.app",
            "oauth@aethersearch.app",
        },
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="jira-users-danswerai",
        user_emails={
            "hagen@danswer.ai",
            "founders@aethersearch.app",
            "pablo@aethersearch.app",
            "chris@aethersearch.app",
            "oauth@aethersearch.app",
        },
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="jira-admins-danswerai",
        user_emails={"hagen@danswer.ai", "founders@aethersearch.app", "pablo@aethersearch.app"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="confluence-user-access-admins-danswerai",
        user_emails={"hagen@danswer.ai"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="jira-user-access-admins-danswerai",
        user_emails={"hagen@danswer.ai"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="Yuhong Only No Chris Allowed",
        user_emails={"yuhong@aethersearch.app"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="All_Confluence_Users_Found_By_AetherSearch",
        user_emails={
            "chris@aethersearch.app",
            "founders@aethersearch.app",
            "hagen@danswer.ai",
            "pablo@aethersearch.app",
            "yuhong@aethersearch.app",
            "oauth@aethersearch.app",
        },
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="bitbucket-users-aethersearchai",
        user_emails={"founders@aethersearch.app", "oauth@aethersearch.app"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="bitbucket-admins-aethersearchai",
        user_emails={"founders@aethersearch.app", "oauth@aethersearch.app"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="jira-servicemanagement-users-danswerai",
        user_emails={"oauth@aethersearch.app"},
        gives_anyone_access=False,
    ),
    ExternalUserGroupSet(
        id="no yuhong allowed",
        user_emails={"hagen@danswer.ai", "pablo@aethersearch.app", "chris@aethersearch.app"},
        gives_anyone_access=False,
    ),
]


def test_confluence_group_sync(
    db_session: Session,
    confluence_connector_config: dict[str, Any],
    confluence_credential_json: dict[str, Any],
) -> None:
    connector = Connector(
        name="Test Connector",
        source=DocumentSource.CONFLUENCE,
        input_type=InputType.POLL,
        connector_specific_config=confluence_connector_config,
        refresh_freq=None,
        prune_freq=None,
        indexing_start=None,
    )
    db_session.add(connector)
    db_session.flush()

    credential = Credential(
        source=DocumentSource.CONFLUENCE,
        credential_json=confluence_credential_json,
    )
    db_session.add(credential)
    db_session.flush()
    # Expire the credential so it reloads from DB with SensitiveValue wrapper
    db_session.expire(credential)

    cc_pair = ConnectorCredentialPair(
        connector_id=connector.id,
        credential_id=credential.id,
        name="Test CC Pair",
        status=ConnectorCredentialPairStatus.ACTIVE,
        access_type=AccessType.SYNC,
        auto_sync_options=None,
    )
    db_session.add(cc_pair)
    db_session.commit()
    db_session.refresh(cc_pair)

    tenant_id = get_current_tenant_id()
    group_sync_iter = confluence_group_sync(
        tenant_id=tenant_id,
        cc_pair=cc_pair,
    )

    expected_groups = {group.id: group for group in _EXPECTED_CONFLUENCE_GROUPS}
    actual_groups = {
        group.id: ExternalUserGroupSet.from_model(external_user_group=group)
        for group in group_sync_iter
    }
    assert expected_groups == actual_groups
