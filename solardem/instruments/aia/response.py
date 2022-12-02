from pathlib import Path

import astropy.units as u
import scipy.io
from astropy.table import QTable

__all__ = ["get_aia_temperature_response"]


def get_aia_temperature_response() -> QTable:
    """
    Get an AIA temperature response table.
    """
    # Taken from https://github.com/alasdairwilson/demregpy/blob/bd20406ad6df0a0b06f92bfe9f324bae7fdb816c/demregpy/tresp/aia_tresp_en.dat
    f = Path(__file__).parent.parent.parent / "data" / "aia_tresp_en.dat"
    data = scipy.io.readsav(f)

    channels = data["channels"].astype(str)
    # Strip leading A
    channels = [c[1:] for c in channels]
    T = 10 ** data["logt"] * u.K
    response = data["tr"] * u.DN * u.cm**5 / u.s / u.pix

    table = QTable()
    table["T"] = T
    for i, c in enumerate(channels):
        table[c] = response[i, :]

    return table
