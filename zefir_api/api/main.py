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

import os
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zefir_api.api.router.root import root_router
from zefir_api.api.router.zefir_aggregate import zefir_agg_router
from zefir_api.api.router.zefir_data import zefir_data_router
from zefir_api.api.router.zefir_map import zefir_map_router
from zefir_api.api.router.zefir_static import zefir_static_router
from zefir_api.api.utils import get_api_prefix, get_api_version

if os.getenv(key="USE_PROXY", default="").lower() == "true":
    settings = dict(
        title="Zefir API",
        version=get_api_version(),
        servers=[{"url": get_api_prefix()}],
        root_path=get_api_prefix(),
    )
else:
    settings = dict(
        title="Zefir API",
        version=get_api_version(),
    )

app: Final = FastAPI(**settings)

request_origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=request_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(zefir_data_router)
app.include_router(zefir_agg_router)
app.include_router(zefir_map_router)
app.include_router(zefir_static_router)
