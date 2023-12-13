import json
import os
from pathlib import Path
from typing import Final

from pyzefir.model.network import Network

from zefir_api.api.utils import get_resources
from zefir_api.api.zefir_engine import ze


class NameTranslatorError(Exception):
    ...


class NameTranslator:
    def __init__(self, network: Network) -> None:
        self._network = network
        self._translated_tags = self.get_translated_tags()
        self._translated_names = self.get_translated_names()
        self._translated_fuels = self.get_translated_fuels()
        self._translated_lbs = self.get_translated_lbs()
        self._translated_energy = self.get_translated_energy()

    @property
    def translated_tags(self) -> dict[str, str]:
        return self._translated_tags

    @property
    def translated_names(self) -> dict[str, str]:
        return self._translated_names

    @property
    def translated_fuels(self) -> dict[str, str]:
        return self._translated_fuels

    @property
    def translated_lbs(self) -> dict[str, str]:
        return self._translated_lbs

    @property
    def translated_energy(self) -> dict[str, str]:
        return self._translated_energy

    @staticmethod
    def _validate_json_env_path(env_name: str, default_path: str | Path) -> Path:
        json_path = os.getenv(env_name, default_path)
        if not Path(json_path).exists() or Path(json_path).suffix.lower() != ".json":
            raise NameTranslatorError(
                f"Given json path {json_path} does not exists or its not a json extension"
            )
        return Path(json_path)

    def _create_mapping_dict(self) -> dict[str, str]:
        result_list = [
            {name: item.tags[0] for name, item in element.items() if item.tags}
            for element in [
                self._network.generator_types,
                self._network.storage_types,
            ]
        ]
        return {name: tag for result in result_list for name, tag in result.items()}

    @staticmethod
    def _load_json(env_name: str, default_path: str | Path) -> dict[str, str]:
        json_path = NameTranslator._validate_json_env_path(env_name, default_path)
        with open(json_path, "r", encoding="utf-8") as json_file:
            translate_dict = json.load(json_file)
        return translate_dict

    def _get_translate(
        self, env_name: str, default_path: str | Path, iter_objects: dict | list
    ) -> dict[str, str]:
        translate_dict = self._load_json(env_name, default_path)
        if isinstance(iter_objects, dict):
            return {
                tech_type: translate_dict.get(tag_name, tag_name)
                for tech_type, tag_name in iter_objects.items()
            }
        if isinstance(iter_objects, list):
            return {name: translate_dict.get(name, name) for name in iter_objects}

    def get_translated_tags(self) -> dict[str, str]:
        return self._get_translate(
            env_name="TRANSLATE_JSON_TAGS_PATH",
            iter_objects=self._create_mapping_dict(),
            default_path=get_resources("translation/tags_translation.json"),
        )

    def get_translated_names(self) -> dict[str, str]:
        return self._get_translate(
            env_name="TRANSLATE_JSON_NAMES_PATH",
            iter_objects=[
                *self._network.generator_types.keys(),
                *self._network.storage_types.keys(),
            ],
            default_path=get_resources("translation/names_translation.json"),
        )

    def get_translated_fuels(self) -> dict[str, str]:
        return self._get_translate(
            env_name="TRANSLATE_JSON_FUELS_PATH",
            iter_objects=[*self._network.fuels.keys()],
            default_path=get_resources("translation/fuel_translation.json"),
        )

    def get_translated_lbs(self) -> dict[str, str]:
        return self._get_translate(
            env_name="TRANSLATE_JSON_LBS_PATH",
            iter_objects=[*self._network.local_balancing_stacks.keys()],
            default_path=get_resources("translation/lbs_translation.json"),
        )

    def get_translated_energy(self) -> dict[str, str]:
        return self._get_translate(
            env_name="TRANSLATE_JSON_ENERGY_PATH",
            iter_objects=self._network.energy_types,
            default_path=get_resources("translation/energy_translation.json"),
        )


translator: Final = NameTranslator(next(iter(ze.values())).network)
