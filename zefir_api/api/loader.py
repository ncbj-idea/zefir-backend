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

import json
from pathlib import Path


class JsonLoaderError(Exception):
    ...


class JsonLoader:
    @staticmethod
    def _validate_json_env_path(json_path: Path) -> None:
        if not json_path.exists() or json_path.suffix.lower() != ".json":
            raise JsonLoaderError(
                f"Given json path {json_path} does not exists or its not a json extension"
            )

    @staticmethod
    def _load_json(json_path: Path) -> dict[str, str]:
        JsonLoader._validate_json_env_path(json_path)
        with open(json_path, "r", encoding="utf-8") as json_file:
            translate_dict = json.load(json_file)
        return translate_dict
