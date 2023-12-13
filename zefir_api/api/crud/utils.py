import pandas as pd
from pyzefir.model.network import Network
from zefir_analytics import ZefirEngine


class NotFoundInNetworkError(Exception):
    ...


def _find_bus_by_energy_type(
    network: Network, gen_name: str, energy_type: str
) -> str | None:
    for bus_name in network.generators[gen_name].buses:
        if network.buses[bus_name].energy_type == energy_type:
            return bus_name
    return None


def _find_lbs_by_bus(network: Network, bus_name: str, energy_type: str) -> str | None:
    for lbs in network.local_balancing_stacks.values():
        if bus_name in lbs.buses[energy_type]:
            return lbs.name
    return None


def get_aggr_by_generator_name(gen_name: str, ze: ZefirEngine, energy_type: str) -> str:
    network = ze.network
    if not (
        bus_name := _find_bus_by_energy_type(
            network=network, gen_name=gen_name, energy_type=energy_type
        )
    ):
        return "not_found_energy_type"

    if not (
        lbs_name := _find_lbs_by_bus(
            network=network, bus_name=bus_name, energy_type=energy_type
        )
    ):
        raise NotFoundInNetworkError("Lbs not found")

    for aggr in network.aggregated_consumers.values():
        if lbs_name in aggr.available_stacks:
            return aggr.name
    raise NotFoundInNetworkError("Aggr not Found")


def flatten_multiindex(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(
        index=df.index.names[0],
        columns=df.index.names[1],
        values=df.columns[0],
        aggfunc="first",
    )


def get_row_amount_of_device_in_agg(
    fractions: dict[str, pd.DataFrame], n_consumers: dict[str, pd.DataFrame]
) -> dict[str, pd.DataFrame]:
    """per agg fraction multiply by n_consumers"""
    amount_dict = dict()
    for fraction_name, fraction_df in fractions.items():
        amount_dict[fraction_name] = fraction_df.multiply(
            n_consumers[fraction_name], axis=0
        ).dropna()
    return amount_dict


def translate_df_by_map(df: pd.DataFrame, mapping_dict: dict[str, str]) -> pd.DataFrame:
    df.index = df.index.map(mapping_dict)
    return df.groupby(df.index).sum()
