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

from pathlib import Path
from unittest.mock import Mock

import pytest

from zefir_api.api.config import params_config
from zefir_api.api.loader import JsonLoaderError
from zefir_api.api.translation import NameTranslator


@pytest.fixture
def mock_network() -> Mock:
    network = Mock()
    network.generator_types = {
        "BOILER_GAS": Mock(tags=["COAL_PLANT"]),
        "Generator": Mock(tags=["Generator_tag"]),
    }
    network.storage_types = {
        "BIG_HEAT_STORAGE": Mock(tags=["HEAT_STORAGE"]),
        "Storage": Mock(tags=["Storage_tag"]),
    }
    network.fuels = {"GAS": "Gas fuel"}
    network.local_balancing_stacks = {"SF_GAS": "gas", "SF_HP": "hp"}
    network.energy_types = ["EE"]
    return network


@pytest.fixture
def name_translator(mock_network: Mock) -> NameTranslator:
    return NameTranslator(network=mock_network)


@pytest.mark.parametrize(
    "env_name, expected_result",
    [
        pytest.param(
            "TRANSLATE_JSON_TAGS_PATH",
            {
                "BOILER_GAS": "Elektrownie węglowe",
                "Generator": "Generator_tag",
                "BIG_HEAT_STORAGE": "Magazyn ciepła",
                "Storage": "Storage_tag",
            },
            id="translate tags",
        ),
        pytest.param(
            "TRANSLATE_JSON_NAMES_PATH",
            {
                "BOILER_GAS": "Kocioł na gaz ziemny",
                "Generator": "Generator",
                "BIG_HEAT_STORAGE": "Magazyn ciepła bardzo duży",
                "Storage": "Storage",
            },
            id="translate names",
        ),
        pytest.param("TRANSLATE_JSON_FUELS_PATH", {"GAS": "Gaz"}, id="translate fuels"),
        pytest.param(
            "TRANSLATE_JSON_LBS_PATH",
            {"SF_GAS": "LBS SF z gazem", "SF_HP": "LBS SF z HP"},
            id="translate lbs",
        ),
        pytest.param(
            "TRANSLATE_JSON_ENERGY_PATH",
            {"EE": "Prąd elektryczny"},
            id="translate energy",
        ),
    ],
)
def test_get_translated_data(
    name_translator: NameTranslator,
    env_name: str,
    expected_result: dict[str, str],
) -> None:
    result = getattr(
        name_translator, f"get_translated_{env_name.split('_')[-2].lower()}"
    )()
    assert result == expected_result


@pytest.mark.parametrize(
    "json_path, iter_objects, expected_result",
    [
        pytest.param(
            params_config.translate_tags_path,
            {"Generator1": "tag1", "Generator2": "HP"},
            {"Generator1": "tag1", "Generator2": "Pompy ciepła"},
            id="tags",
        ),
        pytest.param(
            params_config.translate_names_path,
            ["PV_FARM", "Generator2"],
            {
                "PV_FARM": "Farma paneli fotowoltaicznych",
                "Generator2": "Generator2",
            },
            id="names",
        ),
        pytest.param(
            params_config.translate_fuels_path,
            ["BIOMASS", "Fuel2"],
            {"BIOMASS": "Biomasa", "Fuel2": "Fuel2"},
            id="fuels",
        ),
        pytest.param(
            params_config.translate_lbs_path,
            ["SF_COAL", "LBS2"],
            {"SF_COAL": "LBS SF z węglem", "LBS2": "LBS2"},
            id="lbs",
        ),
        pytest.param(
            params_config.translate_energy_path,
            ["HEAT", "COLD"],
            {"HEAT": "Ciepło systemowe", "COLD": "COLD"},
            id="energy",
        ),
    ],
)
def test_get_translate(
    name_translator: NameTranslator,
    json_path: Path,
    iter_objects: dict[str, str] | list[str],
    expected_result: dict[str, str],
) -> None:
    result = name_translator._get_translate(json_path, iter_objects)
    assert result == expected_result


def test_create_mapping_dict(name_translator: NameTranslator) -> None:
    excepted = {
        "BOILER_GAS": "COAL_PLANT",
        "Generator": "Generator_tag",
        "BIG_HEAT_STORAGE": "HEAT_STORAGE",
        "Storage": "Storage_tag",
    }
    result = name_translator._create_mapping_dict()
    assert result == excepted


@pytest.mark.parametrize(
    "json_path, iter_objects",
    [
        pytest.param(
            Path("/wrong/wrong_json_translation.json"),
            {"Generator1": "tag1", "Generator2": "HP"},
            id="wrong_path",
        ),
        pytest.param(
            params_config.translate_names_path.with_suffix(".csv"),
            ["PV_FARM", "Generator2"],
            id="wrong_extension",
        ),
    ],
)
def test_get_translate_invalid_json(
    name_translator: NameTranslator,
    json_path: Path,
    iter_objects: dict[str, str] | list[str],
) -> None:
    with pytest.raises(expected_exception=JsonLoaderError) as error_msg:
        name_translator._get_translate(json_path, iter_objects)
    assert (
        str(error_msg.value) == f"Given json path {json_path} "
        "does not exists or its not a json extension"
    )
