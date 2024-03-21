# Openingbookserver

This is a naive Python3 reimplementation of a program called "obooksrv" which can be found here: <https://github.com/gkalab/obooksrv>

This program reads in a binary opening book in polyglot format and offers a query via HTTP-API.

The project provided a opening book as test data with the file name `opening.data`. It is included in this folder to be used as the standard opening book

# Modified `python-chess` module

The opening book file `opening.data` seems to have a special format, which the standard `python-chess` module can't handle.

It was necessary to modify the `python-chess` v1.10 module to accept the `opening.data` file.

All modification is done inside the file `polyglot.py` and mainly only consists of modifying the memory map to read out additional bytes per entry and return a fifth value called `entry.n`.
