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

import tempfile
from pathlib import Path

import pytest

from zefir_api.api.config import ConfigParams, ConfigParser


@pytest.fixture
def config_parser_mock() -> ConfigParser:
    return ConfigParser()


@pytest.fixture
def temporary_config_file() -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_config_file_path = Path(temp_dir) / "temp_config.ini"
        config_file_content = """
        [names]
        production_ee_name = Electricity
        production_heat_name = Heating
        """

        with open(temp_config_file_path, "w") as temp_config_file:
            temp_config_file.write(config_file_content)

        yield str(temp_config_file_path)


def test_default_config_params() -> None:
    config_params = ConfigParams()
    assert config_params.production_cold_name == "COLD"
    assert config_params.tags_to_drop == ["KSE", "KSE_CONN", "HD_CONN"]
    assert config_params.usage_heat_name == "HEAT"


def test_load_config_with_valid_file(temporary_config_file: str) -> None:
    config_params = ConfigParser().load_config(temporary_config_file)

    assert config_params.production_ee_name == "Electricity"
    assert config_params.production_heat_name == "Heating"
