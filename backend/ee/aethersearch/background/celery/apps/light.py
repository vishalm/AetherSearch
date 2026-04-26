from aethersearch.background.celery.apps import app_base
from aethersearch.background.celery.apps.light import celery_app

celery_app.autodiscover_tasks(
    app_base.filter_task_modules(
        [
            "ee.aethersearch.background.celery.tasks.doc_permission_syncing",
            "ee.aethersearch.background.celery.tasks.external_group_syncing",
        ]
    )
)
