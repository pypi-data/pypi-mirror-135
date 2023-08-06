=======================================
engi1020: Engineering 1020 library
=======================================

This library wraps several other libraries and re-exports them.
This makes for a messy namespace, but that simplifies the business of importing
libraries for very new students, as they only need to write

::
    from engi1020 import *

The libraries (re-)imported by this library are:

https://matplotlib.org/api/pyplot_api.html[`matplotlib.pyplot`]
  A plotting library using a MATLAB-like API

https://pypi.org/project/nanpy[`nanpy`]
  A Python library for interacting with an Arduino board
