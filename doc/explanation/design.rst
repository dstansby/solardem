Package design
==============
The design of ``solardem`` is influenced by the following ideas:

1. Implementing DEM inversion code is hard...
2. ...but writing a full blown Python package is also hard.
3. Different inversion codes have different inputs and outputs.


Points 1 and 2 lead ``solardem`` to support
- wrapping externally developed codes
- also being a home for any codes that anyone wants to contribute.

Points 3 make it tricky if not impossible to design a common input/output interface for computing DEMs, so each inversion code is allowed to have its own input and output interface.
