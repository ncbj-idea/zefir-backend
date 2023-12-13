import logging
from typing import Any

from fastapi import APIRouter

_logger = logging.getLogger(__name__)

root_router = APIRouter(prefix="")


@root_router.get("/pyzefir_version")
def get_zefir_version() -> dict[str, Any]:
    import pyzefir

    _logger.debug(f"{pyzefir.__version__}")
    return {"pyzefir version": pyzefir.__version__}


@root_router.get("/zefir_analytics_version")
def get_analytics_version() -> dict[str, Any]:
    import zefir_analytics

    _logger.debug(f"{zefir_analytics.__version__}")
    return {"zefir_analytics version": zefir_analytics.__version__}
