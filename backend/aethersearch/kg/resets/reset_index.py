from sqlalchemy.orm import Session

from aethersearch.db.document import reset_all_document_kg_stages
from aethersearch.db.models import Connector
from aethersearch.db.models import KGEntity
from aethersearch.db.models import KGEntityExtractionStaging
from aethersearch.db.models import KGEntityType
from aethersearch.db.models import KGRelationship
from aethersearch.db.models import KGRelationshipExtractionStaging
from aethersearch.db.models import KGRelationshipType
from aethersearch.db.models import KGRelationshipTypeExtractionStaging


def reset_full_kg_index__commit(db_session: Session) -> None:
    """
    Resets the knowledge graph index.
    """

    db_session.query(KGRelationship).delete()
    db_session.query(KGRelationshipType).delete()
    db_session.query(KGEntity).delete()
    db_session.query(KGRelationshipExtractionStaging).delete()
    db_session.query(KGEntityExtractionStaging).delete()
    db_session.query(KGRelationshipTypeExtractionStaging).delete()
    # Update all connectors to disable KG processing
    db_session.query(Connector).update({"kg_processing_enabled": False})

    # Only reset grounded entity types
    db_session.query(KGEntityType).filter(
        KGEntityType.grounded_source_name.isnot(None)
    ).update({"active": False})

    reset_all_document_kg_stages(db_session)

    db_session.commit()
