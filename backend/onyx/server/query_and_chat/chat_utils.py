from aethersearch.file_processing.file_types import AetherSearchMimeTypes
from aethersearch.file_store.models import ChatFileType


def mime_type_to_chat_file_type(mime_type: str | None) -> ChatFileType:
    if mime_type is None:
        return ChatFileType.PLAIN_TEXT

    if mime_type in AetherSearchMimeTypes.IMAGE_MIME_TYPES:
        return ChatFileType.IMAGE

    if mime_type in AetherSearchMimeTypes.TABULAR_MIME_TYPES:
        return ChatFileType.TABULAR

    if mime_type in AetherSearchMimeTypes.DOCUMENT_MIME_TYPES:
        return ChatFileType.DOC

    return ChatFileType.PLAIN_TEXT
