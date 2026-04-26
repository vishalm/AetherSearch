import os
import warnings

_AETHERSEARCH_DOCKER_ENV_STR = "AETHERSEARCH_RUNNING_IN_DOCKER"
_DANSWER_DOCKER_ENV_STR = "DANSWER_RUNNING_IN_DOCKER"


def _resolve_container_flag() -> bool:
    aethersearch_val = os.getenv(_AETHERSEARCH_DOCKER_ENV_STR)
    if aethersearch_val is not None:
        return aethersearch_val.lower() == "true"

    danswer_val = os.getenv(_DANSWER_DOCKER_ENV_STR)
    if danswer_val is not None:
        warnings.warn(
            f"{_DANSWER_DOCKER_ENV_STR} is deprecated and will be ignored in a "
            f"future release. Use {_AETHERSEARCH_DOCKER_ENV_STR} instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return danswer_val.lower() == "true"

    return False


_IS_RUNNING_IN_CONTAINER: bool = _resolve_container_flag()


def is_running_in_container() -> bool:
    return _IS_RUNNING_IN_CONTAINER
