DEMREG
======
In this tutorial we'll step through estimating a DEM using ``demreg``.
Behind the scenes this uses the `demregpy package <https://github.com/alasdairwilson/demregpy>`__ which implements the method described in `Hannah and Kontar 2012 <https://doi.org/10.1051/0004-6361/201117576>`__.

This tutotiral steps through calcuating a DEM with some fake single-pixel data.


To use DEMREG we need the following inputs:

1. Counts in a number of different channels.
2. Associated errors on these counts for the different channels.
3. The temperature response functions of each channel.


For AIA lets start by defining the six channels we'll use::

    >>> channels = ['94', '131', '171', '193', '211', '335']

Now for some fake data and errors::

    >>> import astropy.units as u
    >>>
    >>> counts = {c: 1 * u.DN for c in channels}
    >>> errors = {c: 0.1 * u.DN for c in channels}

Next lets load a temperature response table for AIA::

    >>> from solardem.instruments.aia import get_aia_temperature_response
    >>>
    >>> aia_t_resp = get_aia_temperature_response()
    >>> print(aia_t_resp)
           T                   94           ...          335
           K            cm5 DN / (pix s)    ...    cm5 DN / (pix s)
    ---------------- ---------------------- ... ----------------------
             10000.0 4.0023691175838075e-37 ...  2.317939795967547e-32
     11220.189453125  4.104838049582877e-36 ...   1.77924245649062e-31
    12589.2509765625 3.3627615326659757e-35 ...  1.063265729885801e-30
      14125.37890625 2.0550542361857843e-34 ...  4.598277927746376e-30
    15848.9248046875  8.456819862106854e-34 ...  1.247754058534968e-29
     17782.794921875 2.5312278918789225e-33 ... 2.1251689877474142e-29
       19952.6328125  7.071670918209516e-33 ...  2.869801742433164e-29
      22387.20703125 1.9977098519604384e-32 ...  3.903354668910071e-29
     25118.869140625  5.098290848387121e-32 ...   5.92660248421379e-29
      28183.81640625  9.732532503013028e-32 ...  9.113056615424276e-29
                 ...                    ... ...                    ...
         354813536.0 1.0755746321519548e-29 ...  9.761833711711219e-30
         398107520.0 1.0345182004685725e-29 ...  9.370268669713017e-30
         446683200.0  9.946781751906834e-30 ...  8.991539546129572e-30
         501187008.0  9.560402792460197e-30 ...  8.625901242393643e-30
         562341312.0  9.186088855263137e-30 ...   8.27288973185645e-30
         630957632.0  8.823730228318663e-30 ...  7.932502481469506e-30
         707946432.0  8.473055739187738e-30 ...  7.604003243571458e-30
         794327552.0  8.133827895701225e-30 ...  7.287394844474877e-30
         891250560.0  7.806080194011822e-30 ...  6.982397613441394e-30
        1000000000.0  7.489522675191613e-30 ...  6.688766099417305e-30
    Length = 101 rows

Now for the DEM::

    >>> import numpy as np
    >>> from solardem.methods.demreg import run_demreg
    >>>
    >>> temperatures = np.logspace(4, 8, 25) * u.K
    >>> demreg_output = run_demreg(channel_names=channels, counts=counts, errors=errors, response_table=aia_t_resp, output_temps=temperatures)
    >>> print(demreg_output)
    DEMREGOutput
    ------------
    25 temperatures from 10000.0 K > 100000000.0 K

Putting it all together, here's the full example (this time with some fake data that isn't just ones!):

.. plot::
    :include-source:

    import astropy.units as u
    import numpy as np

    from solardem.instruments.aia import get_aia_temperature_response
    from solardem.methods.demreg import run_demreg

    channels = ["94", "131", "171", "193", "211", "335"]
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

    aia_t_resp = get_aia_temperature_response()

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


Full map
--------
