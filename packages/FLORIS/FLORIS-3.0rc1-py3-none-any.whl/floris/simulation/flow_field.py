# Copyright 2021 NREL

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# See https://floris.readthedocs.io for documentation

from __future__ import annotations

import attrs
from attrs import define, field
import numpy as np

from floris.type_dec import (
    FromDictMixin,
    NDArrayFloat,
    floris_array_converter
)
from floris.simulation import Grid


@define
class FlowField(FromDictMixin):
    wind_speeds: NDArrayFloat = field(converter=floris_array_converter)
    wind_directions: NDArrayFloat = field(converter=floris_array_converter)
    wind_veer: float = field(converter=float)
    wind_shear: float = field(converter=float)
    air_density: float = field(converter=float)
    turbulence_intensity: float = field(converter=float)
    reference_wind_height: int = field(converter=int)

    n_wind_speeds: int = field(init=False)
    n_wind_directions: int = field(init=False)

    u_initial: NDArrayFloat = field(init=False, default=np.array([]))
    v_initial: NDArrayFloat = field(init=False, default=np.array([]))
    w_initial: NDArrayFloat = field(init=False, default=np.array([]))
    u: NDArrayFloat = field(init=False, default=np.array([]))
    v: NDArrayFloat = field(init=False, default=np.array([]))
    w: NDArrayFloat = field(init=False, default=np.array([]))

    turbulence_intensity_field: NDArrayFloat = field(init=False, default=np.array([]))

    @wind_speeds.validator
    def wind_speeds_validator(self, instance: attrs.Attribute, value: NDArrayFloat) -> None:
        """Using the validator method to keep the `n_wind_speeds` attribute up to date."""
        self.n_wind_speeds = value.size

    @wind_directions.validator
    def wind_directions_validator(self, instance: attrs.Attribute, value: NDArrayFloat) -> None:
        """Using the validator method to keep the `n_wind_directions` attribute up to date."""
        self.n_wind_directions = value.size

    def initialize_velocity_field(self, grid: Grid) -> None:

        # Create an initial wind profile as a function of height. The values here will
        # be multiplied with the wind speeds to give the initial wind field.
        # Since we use grid.z, this is a vertical plane for each turbine
        # Here, the profile is of shape (# turbines, N grid points, M grid points)
        # This velocity profile is 1.0 at the reference wind height and then follows wind shear as an exponent.
        # NOTE: the convention of which dimension on the TurbineGrid is vertical and horizontal is
        # determined by this line. Since the right-most dimension on grid.z is storing the values
        # for height, using it here to apply the shear law makes that dimension store the vertical
        # wind profile.
        wind_profile_plane = (grid.z / self.reference_wind_height) ** self.wind_shear

        # Create the sheer-law wind profile
        # This array is of shape (# wind directions, # wind speeds, grid.template_array)
        # Since generally grid.template_array may be many different shapes, we use transposes
        # here to do broadcasting from left to right (transposed), and then transpose back.
        # The result is an array the wind speed and wind direction dimensions on the left side
        # of the shape and the grid.template array on the right
        self.u_initial = (self.wind_speeds[None, :].T * wind_profile_plane.T).T
        self.v_initial = np.zeros(np.shape(self.u_initial), dtype=self.u_initial.dtype)
        self.w_initial = np.zeros(np.shape(self.u_initial), dtype=self.u_initial.dtype)

        self.u = self.u_initial.copy()
        self.v = self.v_initial.copy()
        self.w = self.w_initial.copy()

    def finalize(self, unsorted_indices):
        self.u = np.take_along_axis(self.u, unsorted_indices, axis=2)
        self.v = np.take_along_axis(self.v, unsorted_indices, axis=2)
        self.w = np.take_along_axis(self.w, unsorted_indices, axis=2)
