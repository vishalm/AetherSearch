import pytest

from aethersearch.auth.email_utils import build_user_email_invite
from aethersearch.auth.email_utils import send_email
from aethersearch.configs.constants import AuthType
from aethersearch.configs.constants import AETHERSEARCH_DEFAULT_APPLICATION_NAME
from aethersearch.db.engine.sql_engine import SqlEngine
from aethersearch.server.runtime.aethersearch_runtime import AetherSearchRuntime


@pytest.mark.skip(
    reason="This sends real emails, so only run when you really want to test this!"
)
def test_send_user_email_invite() -> None:
    SqlEngine.init_engine(pool_size=20, max_overflow=5)

    application_name = AETHERSEARCH_DEFAULT_APPLICATION_NAME

    aethersearch_file = AetherSearchRuntime.get_emailable_logo()

    subject = f"Invitation to Join {application_name} Organization"

    FROM_EMAIL = "noreply@aethersearch.app"
    TO_EMAIL = "support@aethersearch.app"
    text_content, html_content = build_user_email_invite(
        FROM_EMAIL, TO_EMAIL, AETHERSEARCH_DEFAULT_APPLICATION_NAME, AuthType.CLOUD
    )

    send_email(
        TO_EMAIL,
        subject,
        html_content,
        text_content,
        mail_from=FROM_EMAIL,
        inline_png=("logo.png", aethersearch_file.data),
    )
