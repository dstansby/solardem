channels = ["94", "131", "171", "193", "211", "335"]
import astropy.units as u

dn_in = [
    326.11015434,
    313.31711078,
    2663.51032758,
    11361.19773432,
    8700.35614133,
    1208.36625462,
]
edn_in = [14.94543538, 12.67184957, 32.12696435, 61.39593311, 51.38885685, 15.53907416]
counts = {c: dn * u.DN for c, dn in zip(channels, dn_in)}
errors = {c: dn * u.DN for c, dn in zip(channels, edn_in)}


from solardem.aia import get_aia_temperature_response

aia_t_resp = get_aia_temperature_response()

import numpy as np

from solardem.demreg import run_demreg

mint = 5.7
maxt = 7.2
dlogt = 0.05
temperatures = 10 ** np.arange(mint, maxt + dlogt, dlogt) * u.K
dem_data = run_demreg(
    channel_names=channels,
    counts=counts,
    errors=errors,
    response_table=aia_t_resp,
    output_temps=temperatures,
)

dem_data.peek()
