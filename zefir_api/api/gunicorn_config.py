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
