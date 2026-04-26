import generated.aethersearch_openapi_client.aethersearch_openapi_client as aethersearch_api  # ty: ignore[unresolved-import]

from tests.integration.common_utils.constants import API_SERVER_URL

api_config = aethersearch_api.Configuration(host=API_SERVER_URL)
