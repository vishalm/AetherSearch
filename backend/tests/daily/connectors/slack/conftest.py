import os
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from pytest import FixtureRequest
from slack_sdk import WebClient

from aethersearch.connectors.credentials_provider import AetherSearchStaticCredentialsProvider
from aethersearch.connectors.slack.connector import SlackConnector
from shared_configs.contextvars import get_current_tenant_id


@pytest.fixture
def mock_slack_client() -> MagicMock:
    mock = MagicMock(spec=WebClient)
    return mock


@pytest.fixture
def slack_connector(
    request: FixtureRequest,
    mock_slack_client: MagicMock,
    slack_credentials_provider: AetherSearchStaticCredentialsProvider,
) -> Generator[SlackConnector]:
    channel: str | None = request.param if hasattr(request, "param") else None
    connector = SlackConnector(
        channels=[channel] if channel else None,
        channel_regex_enabled=False,
        use_redis=False,
    )
    connector.client = mock_slack_client
    connector.set_credentials_provider(credentials_provider=slack_credentials_provider)
    yield connector


@pytest.fixture
def slack_credentials_provider() -> AetherSearchStaticCredentialsProvider:
    CI_ENV_VAR = "SLACK_BOT_TOKEN"
    LOCAL_ENV_VAR = "AETHERSEARCH_BOT_SLACK_BOT_TOKEN"

    slack_bot_token = os.environ.get(CI_ENV_VAR, os.environ.get(LOCAL_ENV_VAR))
    if not slack_bot_token:
        raise RuntimeError(
            f"No slack credentials found; either set the {CI_ENV_VAR} env-var or the {LOCAL_ENV_VAR} env-var"
        )

    return AetherSearchStaticCredentialsProvider(
        tenant_id=get_current_tenant_id(),
        connector_name="slack",
        credential_json={
            "slack_bot_token": slack_bot_token,
        },
    )
