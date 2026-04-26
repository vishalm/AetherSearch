from collections.abc import Callable
from collections.abc import Generator
from typing import Optional
from typing import Protocol

from ee.aethersearch.db.external_perm import ExternalUserGroup  # noqa
from aethersearch.access.models import DocExternalAccess  # noqa
from aethersearch.access.models import ElementExternalAccess  # noqa
from aethersearch.access.models import NodeExternalAccess  # noqa
from aethersearch.context.search.models import InferenceChunk
from aethersearch.db.models import ConnectorCredentialPair  # noqa
from aethersearch.db.utils import DocumentRow
from aethersearch.db.utils import SortOrder
from aethersearch.indexing.indexing_heartbeat import IndexingHeartbeatInterface  # noqa


class FetchAllDocumentsFunction(Protocol):
    """Protocol for a function that fetches documents for a connector credential pair.

    This protocol defines the interface for functions that retrieve documents
    from the database, typically used in permission synchronization workflows.
    """

    def __call__(
        self,
        sort_order: SortOrder | None,
    ) -> list[DocumentRow]:
        """
        Fetches documents for a connector credential pair.
        """
        ...


class FetchAllDocumentsIdsFunction(Protocol):
    """Protocol for a function that fetches document IDs for a connector credential pair.

    This protocol defines the interface for functions that retrieve document IDs
    from the database, typically used in permission synchronization workflows.
    """

    def __call__(
        self,
    ) -> list[str]:
        """
        Fetches document IDs for a connector credential pair.
        """
        ...


# Defining the input/output types for the sync functions
DocSyncFuncType = Callable[
    [
        ConnectorCredentialPair,
        FetchAllDocumentsFunction,
        FetchAllDocumentsIdsFunction,
        Optional[IndexingHeartbeatInterface],
    ],
    Generator[ElementExternalAccess, None, None],
]

GroupSyncFuncType = Callable[
    [
        str,  # tenant_id
        ConnectorCredentialPair,  # cc_pair
    ],
    Generator[ExternalUserGroup, None, None],
]

# list of chunks to be censored and the user email. returns censored chunks
CensoringFuncType = Callable[[list[InferenceChunk], str], list[InferenceChunk]]
