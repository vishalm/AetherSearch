"""Unit-test conftest — shared fixtures for the entire unit suite.

The unit suite must not touch external services (Postgres, Redis, Vespa, etc).
A subtle hazard breaks that contract: importing certain modules
(e.g. ``aethersearch.chat.process_message`` via the celery client import chain)
calls ``set_is_ee_based_on_env_variable()`` at import time. With the default
``LICENSE_ENFORCEMENT_ENABLED=true``, this flips ``global_version._is_ee`` to
True for the rest of the pytest session, causing later unit tests to take the
EE code path — which loads EE implementations that talk to Redis.

This fixture snapshots and restores the EE flag around every unit test so
import-time side effects from one test cannot leak into the next.
"""

from collections.abc import Generator

import pytest

from aethersearch.utils.variable_functionality import fetch_versioned_implementation
from aethersearch.utils.variable_functionality import global_version


@pytest.fixture(autouse=True)
def _isolate_ee_version_state() -> Generator[None, None, None]:
    # Force the safe default for unit tests. Tests that need EE must opt in via
    # the `enable_ee` fixture (defined in backend/tests/conftest.py), which
    # flips the flag for the test body and restores it on teardown.
    if global_version._is_ee:
        global_version._is_ee = False
    fetch_versioned_implementation.cache_clear()
    yield
