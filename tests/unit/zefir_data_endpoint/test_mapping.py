from unittest.mock import Mock

import pytest

from zefir_api.api.mapping import NameTranslator, NameTranslatorError
from zefir_api.api.utils import get_resources


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
        (
            "TRANSLATE_JSON_LBS_PATH",
            {"SF_GAS": "LBS SF z gazem", "SF_HP": "LBS SF z HP"},
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
    "env_name, default_path, iter_objects, expected_result",
    [
        pytest.param(
            "TRANSLATE_JSON_TAGS_PATH",
            "translation/tags_translation.json",
            {"Generator1": "tag1", "Generator2": "HP"},
            {"Generator1": "tag1", "Generator2": "Pompy ciepła"},
            id="tags",
        ),
        pytest.param(
            "TRANSLATE_JSON_NAMES_PATH",
            "translation/names_translation.json",
            ["PV_FARM", "Generator2"],
            {
                "PV_FARM": "Farma paneli fotowoltaicznych",
                "Generator2": "Generator2",
            },
            id="names",
        ),
        pytest.param(
            "TRANSLATE_JSON_FUELS_PATH",
            "translation/fuel_translation.json",
            ["BIOMASS", "Fuel2"],
            {"BIOMASS": "Biomasa", "Fuel2": "Fuel2"},
            id="fuels",
        ),
        pytest.param(
            "TRANSLATE_JSON_LBS_PATH",
            "translation/lbs_translation.json",
            ["SF_COAL", "LBS2"],
            {"SF_COAL": "LBS SF z węglem", "LBS2": "LBS2"},
            id="lbs",
        ),
        pytest.param(
            "TRANSLATE_JSON_ENERGY_PATH",
            "translation/energy_translation.json",
            ["HEAT", "COLD"],
            {"HEAT": "Ciepło systemowe", "COLD": "COLD"},
            id="energy",
        ),
    ],
)
def test_get_translate(
    name_translator: NameTranslator,
    env_name: str,
    default_path: str,
    iter_objects: dict[str, str] | list[str],
    expected_result: dict[str, str],
) -> None:
    result = name_translator._get_translate(
        env_name, get_resources(default_path), iter_objects
    )
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
    "env_name, default_path, iter_objects",
    [
        pytest.param(
            "TRANSLATE_JSON_TAGS_PATH",
            "tags_translation.json",
            {"Generator1": "tag1", "Generator2": "HP"},
            id="wrong_path",
        ),
        pytest.param(
            "TRANSLATE_JSON_NAMES_PATH",
            "translation/names_translation.csv",
            ["PV_FARM", "Generator2"],
            id="wrong_extension",
        ),
    ],
)
def test_get_translate_invalid_json(
    name_translator: NameTranslator,
    env_name: str,
    default_path: str,
    iter_objects: dict[str, str] | list[str],
) -> None:
    with pytest.raises(expected_exception=NameTranslatorError) as error_msg:
        name_translator._get_translate(
            env_name, get_resources(default_path), iter_objects
        )
    assert (
        str(error_msg.value) == f"Given json path {get_resources(default_path)} "
        "does not exists or its not a json extension"
    )
