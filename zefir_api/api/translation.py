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
from typing import Final

from pyzefir.model.network import Network

from zefir_api.api.config import params_config
from zefir_api.api.loader import JsonLoader
from zefir_api.api.zefir_engine import ze


class NameTranslator(JsonLoader):
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

    def _create_mapping_dict(self) -> dict[str, str]:
        result_list = [
            {name: item.tags[0] for name, item in element.items() if item.tags}
            for element in [
                self._network.generator_types,
                self._network.storage_types,
            ]
        ]
        return {name: tag for result in result_list for name, tag in result.items()}

    def _get_translate(
        self, json_path: Path, iter_objects: dict | list
    ) -> dict[str, str]:
        translate_dict = self._load_json(json_path)
        if isinstance(iter_objects, dict):
            return {
                tech_type: translate_dict.get(tag_name, tag_name)
                for tech_type, tag_name in iter_objects.items()
            }
        if isinstance(iter_objects, list):
            return {name: translate_dict.get(name, name) for name in iter_objects}

    def get_translated_tags(self) -> dict[str, str]:
        return self._get_translate(
            json_path=params_config.translate_tags_path,
            iter_objects=self._create_mapping_dict(),
        )

    def get_translated_names(self) -> dict[str, str]:
        return self._get_translate(
            json_path=params_config.translate_names_path,
            iter_objects=[
                *self._network.generator_types.keys(),
                *self._network.storage_types.keys(),
            ],
        )

    def get_translated_fuels(self) -> dict[str, str]:
        return self._get_translate(
            json_path=params_config.translate_fuels_path,
            iter_objects=[*self._network.fuels.keys()],
        )

    def get_translated_lbs(self) -> dict[str, str]:
        return self._get_translate(
            json_path=params_config.translate_lbs_path,
            iter_objects=[*self._network.local_balancing_stacks.keys()],
        )

    def get_translated_energy(self) -> dict[str, str]:
        return self._get_translate(
            json_path=params_config.translate_energy_path,
            iter_objects=self._network.energy_types,
        )


translator: Final = NameTranslator(next(iter(ze.values())).network)
