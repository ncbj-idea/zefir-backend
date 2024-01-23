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

from zefir_api.api.payload.zefir_static import StaticAggrDataResponse, StaticAggrDetails
from zefir_api.api.static_data import StaticData


def get_aggr_static_data() -> list[StaticAggrDataResponse]:
    aggr_data = StaticData.load_static_aggr_data()
    return [
        StaticAggrDataResponse(
            aggr_type=aggr_type,
            data=[
                StaticAggrDetails.create_from_dict(
                    consumption_type=consumption_type, data_dict=data_dict
                )
                for consumption_type, data_dict in data.to_dict(orient="index").items()
            ],
        )
        for aggr_type, data in aggr_data.items()
    ]
