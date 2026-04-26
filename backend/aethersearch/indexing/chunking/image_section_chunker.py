from aethersearch.connectors.models import Section
from aethersearch.indexing.chunking.section_chunker import AccumulatorState
from aethersearch.indexing.chunking.section_chunker import ChunkPayload
from aethersearch.indexing.chunking.section_chunker import SectionChunker
from aethersearch.indexing.chunking.section_chunker import SectionChunkerOutput
from aethersearch.utils.text_processing import clean_text


class ImageChunker(SectionChunker):
    def chunk_section(
        self,
        section: Section,
        accumulator: AccumulatorState,
        content_token_limit: int,  # noqa: ARG002
    ) -> SectionChunkerOutput:
        assert section.image_file_id is not None

        section_text = clean_text(str(section.text or ""))
        section_link = section.link or ""

        # Flush any partially built text chunks
        payloads = accumulator.flush_to_list()
        payloads.append(
            ChunkPayload(
                text=section_text,
                links={0: section_link} if section_link else {},
                image_file_id=section.image_file_id,
                is_continuation=False,
            )
        )

        return SectionChunkerOutput(
            payloads=payloads,
            accumulator=AccumulatorState(),
        )
