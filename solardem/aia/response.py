from pathlib import Path
from typing import Any

import astropy.units as u
import scipy.io
from astropy.table import QTable

from .channel import AIAChannel

__all__ = ["AIAResponseTable", "get_aia_temperature_response"]


class AIAResponseTable(QTable):  # type: ignore
    """
    A QTable with validation to check that expected column names are present.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._validate_cols()

    def _validate_cols(self) -> None:
        assert "T" in self.colnames, "No temperature column"
        for channel in AIAChannel:
            assert str(channel.value) in self.colnames, f"No column for {channel.value}"


def get_aia_temperature_response() -> AIAResponseTable:
    """
    Get an AIA temperature response table.
    """
    # Taken from https://github.com/alasdairwilson/demregpy/blob/bd20406ad6df0a0b06f92bfe9f324bae7fdb816c/demregpy/tresp/aia_tresp_en.dat
    f = Path(__file__).parent.parent / "data" / "aia_tresp_en.dat"
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

    return AIAResponseTable(table)
