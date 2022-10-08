from dataclasses import dataclass
from typing import Dict, List

import astropy.units as u
import numpy as np
from astropy.table import QTable
from demregpy import dn2dem


@u.quantity_input
def run_demreg(
    *,
    channel_names: List[str],
    counts: Dict[str, u.Quantity],
    errors: Dict[str, u.Quantity],
    response_table: QTable,
    output_temps: u.K
):
    """
    Calculate a DEM.

    counts :
        Mapping of channel to counts in that channel.
    """
    count_array = np.vstack([counts[c].to_value(u.DN) for c in channel_names]).T
    count_array = np.broadcast_to(count_array, (1,) + count_array.shape)
    error_array = np.vstack([errors[c].to_value(u.DN) for c in channel_names]).T
    error_array = np.broadcast_to(error_array, (1,) + error_array.shape)

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

    return dem, errors, logt_errors, chisq, dn_simulated