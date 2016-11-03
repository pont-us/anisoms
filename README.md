# anisoms: a Python library for reading AMS data

## Introduction

AGICO kappabridges write AMS (anisotropy of magnetic susceptibility)
data in two formats: ASC and RAN. The first is an ASCII file formatted
for easy perusal; the second is a compact binary format. Neither format
is entirely straightforward to read for further processing. 
`anisoms` is a Python library which provides functions to read data
from RAN and ASC files into Python dictionaries. `anisoms` also contains
a few simple utility functions for AMS data, for example to turn AMS
tensors into principal directions.

As well as the main library `ams_lib`, the `anisoms` package contains
a few short command-line scripts. These scripts demonstrate the usage
of the `ams_lib` functions, as well as being potentially useful in
their own right.

## Usage
