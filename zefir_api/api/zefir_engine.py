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

import re
from typing import Final

from zefir_analytics import ZefirEngine

from zefir_api.api.config import params_config


def create_zefir_engines() -> dict[int, ZefirEngine]:
    scenarios_folder = params_config.source_path / "scenarios"
    return {
        int(id_.group()): ZefirEngine(
            source_path=params_config.source_path,
            result_path=params_config.result_path / scenario_name.name,
            parameter_path=params_config.parameter_path,
            scenario_name=scenario_name.name,
        )
        for scenario_name in scenarios_folder.iterdir()
        if (id_ := re.search(r"\d+", scenario_name.name)) is not None
    }


ze: Final = create_zefir_engines()
