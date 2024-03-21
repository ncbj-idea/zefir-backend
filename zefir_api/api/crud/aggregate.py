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

import pandas as pd
from pyzefir.model.network import AggregatedConsumer, Network
from zefir_analytics import ZefirEngine

from zefir_api.api.crud.utils import (
    flatten_multiindex,
    get_aggr_by_generator_name,
    get_row_amount_of_device_in_agg,
)
from zefir_api.api.parameters import AggregateType, ConsumptionType
from zefir_api.api.payload.zefir_aggregate import (
    AreaData,
    UsagePerBuildingData,
    ZefirAggregateDetail,
    ZefirAggregateStacks,
    ZefirAggregateTotals,
)
from zefir_api.api.translation import translator


def _filter_by_agg_type(
    ze: ZefirEngine, aggregate_type: AggregateType
) -> list[AggregatedConsumer]:
    return [
        agg
        for agg_name, agg in ze.network.aggregated_consumers.items()
        if agg_name.startswith(aggregate_type.value.upper())
    ]


def _filter_by_consumption_type(
    aggregates: list[AggregatedConsumer],
) -> dict[str, list[AggregatedConsumer]]:
    consumption_dict: dict[str, list[AggregatedConsumer]] = {
        member.name: [] for member in ConsumptionType
    }
    for agg in aggregates:
        for member in ConsumptionType:
            if member.value in agg.name:
                consumption_dict[member.name].append(agg)
    return consumption_dict


def _get_area_data(
    aggregates: list[AggregatedConsumer], device_factor: dict[str, pd.DataFrame]
) -> list[AreaData]:
    area_objects_list: list[AreaData] = []
    for agg in aggregates:
        agg_device_factor = device_factor[agg.name]
        for lbs_name in agg.available_stacks:
            values = (agg_device_factor[lbs_name] * agg.average_area).to_list()
            area_objects_list.append(
                AreaData(
                    stack_name=translator.translated_lbs.get(lbs_name, lbs_name),
                    values=values,
                )
            )
    return area_objects_list


def _get_usage_per_building(
    ze: ZefirEngine,
    aggregates: list[AggregatedConsumer],
    gen_demand: pd.DataFrame,
    year_sample_len: int,
) -> list[UsagePerBuildingData]:
    energy_result_dict: dict[str, pd.Series] = {}
    for agg in aggregates:
        for en_type, energy_usage in agg.yearly_energy_usage.items():
            gen_demand_values = None
            if en_type in gen_demand:
                demand_df = flatten_multiindex(gen_demand[[en_type]])
                demand_df = demand_df.rename(
                    {
                        name: get_aggr_by_generator_name(
                            gen_name=name, ze=ze, energy_type=en_type
                        )
                        for name in demand_df.index
                    }
                )
                if agg.name in demand_df.index:
                    gen_demand_values = demand_df.loc[agg.name]
            energy_usage = energy_usage * agg.n_consumers
            summed_energy_usage = (
                (energy_usage + gen_demand_values)
                if gen_demand_values is not None
                else energy_usage
            )
            summed_energy_usage = summed_energy_usage[:year_sample_len]
            if en_type in energy_result_dict:
                energy_result_dict[en_type] = (
                    energy_result_dict[en_type] + summed_energy_usage
                )
            else:
                energy_result_dict[en_type] = summed_energy_usage

    return [
        UsagePerBuildingData(
            energy_type=translator.translated_energy.get(en_type, en_type),
            values=values.to_list(),
        )
        for en_type, values in energy_result_dict.items()
    ]


def _get_total_area_and_buildings_in_agg_type(
    aggregates: list[AggregatedConsumer], year_sample_len: int
) -> tuple[list[float], list[int]]:
    total_values: dict[str, pd.Series] = {}
    if not aggregates:
        return [], []
    for agg in aggregates:
        totals = {
            "buildings": agg.n_consumers[:year_sample_len],
            "area": agg.n_consumers[:year_sample_len] * agg.average_area,
        }
        for attr in totals:
            if attr in total_values:
                total_values[attr] = total_values[attr] + totals[attr]
            else:
                total_values[attr] = totals[attr]

    return (
        total_values["area"].to_list(),
        total_values["buildings"].to_list(),
    )


def _get_unique_element_type_from_buses(network: Network, buses: set[str]) -> set[str]:
    unique_types = set()
    for bus_name in buses:
        bus = network.buses[bus_name]
        for gen_name in bus.generators:
            unique_types.add(network.generators[gen_name].energy_source_type)
        for stor_name in bus.storages:
            unique_types.add(network.storages[stor_name].energy_source_type)
    return unique_types


def get_agg_totals(
    ze: ZefirEngine, aggregate_type: AggregateType
) -> ZefirAggregateTotals:
    ys_len = len(ze._year_sample)
    aggregates = _filter_by_agg_type(ze=ze, aggregate_type=aggregate_type)
    if aggregates:
        total_amount_of_buildings = (
            pd.concat([agg.n_consumers for agg in aggregates], axis=1)
            .sum(axis=1)
            .tolist()
        )[:ys_len]
        total_usable_area = (
            pd.concat(
                [agg.n_consumers * agg.average_area for agg in aggregates], axis=1
            )
            .sum(axis=1)
            .tolist()
        )[:ys_len]
        return ZefirAggregateTotals(
            total_amount_of_buildings=total_amount_of_buildings,
            total_usable_area=total_usable_area,
        )
    else:
        return ZefirAggregateTotals(
            total_amount_of_buildings=[],
            total_usable_area=[],
        )


def get_stacks_info(
    ze: ZefirEngine, aggregate_type: AggregateType
) -> list[ZefirAggregateStacks]:
    stacks_list = []
    aggregates = _filter_by_agg_type(ze=ze, aggregate_type=aggregate_type)
    for agg in aggregates:
        for lbs_name in agg.available_stacks:
            lbs = ze.network.local_balancing_stacks[lbs_name]
            type_set: set[str] = set()
            for buses in lbs.buses.values():
                type_set = type_set.union(
                    _get_unique_element_type_from_buses(ze.network, buses)
                )
                techs = [
                    translator.translated_names.get(name, name) for name in type_set
                ]
            stacks_list.append(
                ZefirAggregateStacks(
                    stack_name=translator.translated_lbs.get(lbs_name, lbs_name),
                    techs=techs,
                )
            )
    return stacks_list


def get_details(
    ze: ZefirEngine, aggregate_type: AggregateType
) -> list[ZefirAggregateDetail]:
    details_object_list: list[ZefirAggregateDetail] = []
    aggregates = _filter_by_agg_type(ze=ze, aggregate_type=aggregate_type)
    agg_consumption_filtered = _filter_by_consumption_type(aggregates)
    fractions = ze.aggregated_consumer_params.get_fractions()
    n_consumers = ze.aggregated_consumer_params.get_n_consumers()
    fraction_consumers = get_row_amount_of_device_in_agg(fractions, n_consumers)
    gen_demand = ze.source_params.get_generation_demand(level="element").dropna()
    ys_len = len(ze._year_sample)

    for consumption_type, agg_list in agg_consumption_filtered.items():
        area = _get_area_data(agg_list, fraction_consumers)
        usage_per_building = _get_usage_per_building(ze, agg_list, gen_demand, ys_len)
        total_agg_area, total_agg_building = _get_total_area_and_buildings_in_agg_type(
            agg_list, ys_len
        )
        details_object_list.append(
            ZefirAggregateDetail(
                name=consumption_type,
                area=area,
                energy_per_building=usage_per_building,
                agg_area=total_agg_area,
                agg_amount_of_building=total_agg_building,
            )
        )
    return details_object_list
