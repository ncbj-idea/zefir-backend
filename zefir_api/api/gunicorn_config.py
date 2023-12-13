import os

from uvicorn.workers import UvicornWorker


class Worker(UvicornWorker):
    pass


bind = "0.0.0.0:" + os.getenv("API_PORT", "5050")
worker_class = "zefir_api.api.gunicorn_config.Worker"
timeout = 120
accesslog = "-"
access_log_format = (
    "{"
    '"date": "%(t)s",'
    '"status_line": "%(r)s",'
    '"remote_address": "%(h)s",'
    '"status": "%(s)s",'
    '"response_length": "%(b)s",'
    '"request_time": "%(L)s",'
    '"referer": "%(f)s",'
    "}"
)
workers = 3
preload_app = True
