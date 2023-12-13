import os
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zefir_api.api.router.root import root_router
from zefir_api.api.router.zefir_aggregate import zefir_agg_router
from zefir_api.api.router.zefir_data import zefir_data_router
from zefir_api.api.router.zefir_map import zefir_map_router
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
