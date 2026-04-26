from pydantic import BaseModel

from aethersearch.access.models import ExternalAccess
from aethersearch.connectors.models import Document


class TeamsThread(BaseModel):
    thread: str
    external_access: ExternalAccess

    @classmethod
    def from_doc(cls, document: Document) -> "TeamsThread":
        assert (
            document.external_access
        ), f"ExternalAccess should always be available, instead got {document=}"

        return cls(
            thread=document.get_text_content(),
            external_access=document.external_access,
        )
