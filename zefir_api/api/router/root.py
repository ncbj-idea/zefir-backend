# NCBR_backend
# Copyright (C) 2023-2024 Narodowe Centrum Badań Jądrowych
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
