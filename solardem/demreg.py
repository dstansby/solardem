from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import QTable
from astropy.visualization import quantity_support
from demregpy import dn2dem
from matplotlib.axes import Axes

__all__ = ["DEMREGOutput", "run_demreg"]


@dataclass
class DEMREGOutput:
    dem: u.Quantity
    dem_errors: u.Quantity
    temps: u.Quantity
    temps_errors: u.Quantity
    chisq: np.ndarray
    dn_simulated: u.Quantity

    def __str__(self) -> str:
        logTrange = np.log10(self.temps[[0, -1]].to_value(u.K))
        return dedent(
            f"""
        DEMREGOutput
        ------------
        log(T/K) = [{logTrange[0]:.2f}, {logTrange[-1]:.2f}] in {len(self.temps) - 1} bins"""
        )

    def peek(self) -> None:
        """
        Plot the output on a fresh figure, and show the figure.
        """
        fig, ax = plt.subplots()
        self.plot(ax)
        ax.set_xscale("log")
        ax.set_yscale("log")
        plt.show()

    def plot(self, ax: Axes) -> None:
        """
        Plot the output. This will just plot the data, with no plot formatting.
        """
        quantity_support()
        ax.stairs(self.dem, self.temps)


def run_demreg(
    *,
    channel_names: List[str],
    counts: Dict[str, u.Quantity],
    errors: Dict[str, u.Quantity],
    response_table: QTable,
    output_temps: u.K,
) -> DEMREGOutput:
    """
    Calculate a DEM.

    counts :
        Mapping of channel to counts in that channel.
    errors :
        Mapping of channel to error on the counts in that channel.
    response_table :
        Temperature response table.
    output_tems :
        Temperatures to calculate the DEM at.
    """
    count_array = np.stack(
        [np.atleast_2d(counts[c].to_value(u.DN)) for c in channel_names], axis=-1
    )
    error_array = np.stack(
        [np.atleast_2d(errors[c].to_value(u.DN)) for c in channel_names], axis=-1
    )

    tresp = np.vstack(
        [
            response_table[c].to_value(u.cm**5 * u.DN / (u.pix * u.s))
            for c in channel_names
        ]
    ).T

    tresp_logt = np.log10(response_table["T"].to_value(u.K))
    tout = output_temps.to_value(u.K)

    dem, errors, logt_errors, chisq, dn_simulated = dn2dem(
        count_array,
        error_array,
        tresp,
        tresp_logt,
        tout,
    )

    DEM_UNIT = 1 / (u.cm**5 * u.K)
    return DEMREGOutput(
        dem * DEM_UNIT,
        errors * DEM_UNIT,
        output_temps,
        logt_errors * u.K,
        chisq,
        dn_simulated * u.DN,
    )
