# anisoms: a Python library for reading AMS data

## Introduction

AGICO kappabridges write AMS (anisotropy of magnetic susceptibility) data in
two formats: ASC and RAN. The first is an ASCII file formatted for easy
perusal; the second is a compact binary format. Neither format is entirely
straightforward to read for further processing. anisoms provides a Python
library with functions to read and plot data from RAN and ASC files into
Python dictionaries. As well as the main library `anisoms`, the package also
contains a few short command-line scripts. These scripts demonstrate the usage
of the anisoms API, as well as being potentially useful in their own right.

Documentation for anisoms is available on
[readthedocs](https://anisoms.readthedocs.io/en/latest/).

## AMS file formats

The file formats are described in more detail in user manuals for
AGICO equipment (AGICO, 2003; AGICO, 2009).

The RAN file contains a limited amount of data for each sample, most crucially
the orientation tensor. In the RAN file, this tensor is given only in the
geographic co-ordinate system (not, as might be expected, in the "raw"
specimen co-ordinate system). A RAN file is sometimes used in conjunction with
a GED ("geological data") file, which contains some additional sample data
such as orientation conventions and additional co-ordinate systems; currently,
anisoms does not read GED files.

The structure of the ASC file corresponds to the format of the data displayed
on the screen during usage of the SUSAR, SUSAM, or SAFYR program, and varies
slightly according to the program version and measurement settings. The ASC
file contains a more extensive range of data than the RAN file, including
anisotropy as both tensors and principal directions, in all the co-ordinate
systems which were specified during measurement.

## anisoms usage

This is a brief overview; the API is fully detailed by the docstrings in
the source code and
[on readthedocs](https://anisoms.readthedocs.io/en/latest/anisoms.html).

The functions `read_ran` and `read_asc` read a file of the respective types
and return a nested dictionary structure containing the data from the file.

The `Direction` class represents a direction in three-dimensional space, and
includes a method to plot itself on an equal-area plot using the pyx graphics
library.

The `PrincipalDirs` class represents the three principal directions of an
anisotropy tensor. It can be initialized from the directions themselves or
from a tensor.

The `directions_from_ran`, `directions_from_asc_tensors`, and
`directions_from_asc_directions` functions read a data file and return a
corresponding dictionary containing a `PrincipalDirs` object for each sample in
the file.

The `corrected_anisotropy_factor` function calculates the corrected anisotropy
factor (*P′* or *P*<sub>j</sub>) (Jelínek, 1981; Hrouda, 1982).

## Overview of scripts

- `ams-asc-to-csv` converts AMS data from ASC format to CSV format.
- `ams-params-from-asc` prints selected parameters from an ASC file.
- `ams-plot` plots AMS directions from ASC and RAN files.
- `ams-print-ran-tensor` reads RAN files and prints their AMS tensors.
- `ams-tensor-to-dir` prints the first principal directions of supplied tensors.

More detailed documentation for the scripts is available in their
docstrings, in their output when run with a `--help` argument, and
[on readthedocs](https://anisoms.readthedocs.io/en/latest/cli-tools.html).

## Precision considerations

In the RAN file, the components of the orientation tensor are stored as
32-bit floating point numbers, which have a precision of around 7 significant
figures. In the ASC file, they are given as decimals with 5 significant figures
of precision. So, for maximal precision, the tensors should be read from the
RAN file; since the RAN file only gives tensors in the geographic co-ordinate
system, they may have to be rotated into the desired co-ordinate system after
reading. `anisoms` currently focuses on data reading, and does not provide
functions for these rotations, but it does provide a function for converting
tensors to principal directions.

When obtaining principal directions solely from an ASC file, the most precise
method is to read directly the directions stored there, rather than reading
the tensor and calculating directions from it. I have confirmed this by
comparing both methods with the directions calculated from the high-precision
tensor in the corresponding RAN file. The principal directions stored in the
ASC file are presumably calculated directly from the full-precision floats.
Calculating principal directions from the GED tensor is still more precise
than reading the directions from the ASC file, since the latter are rounded to
the nearest degree.

## License

Copyright 2019 Pontus Lurcock; released under the [GNU General Public License,
version 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

## References

AGICO, 2003. *KLY-3 / KLY-3S / CS-3 / CS-L / CS-23 user’s guide*, Brno, Czech
Republic: Advanced Geoscience Instruments Co.
https://www.agico.com/downloads/documents/manuals/kly3-man.pdf

AGICO, 2009. *MFK1-FA / CS4 / CSL, MFK1-A / CS4 / CSL, MFK1-FB, MFK1-B user’s
guide* 4th ed., Brno, Czech Republic: Advanced Geoscience Instruments Co.
https://www.agico.com/downloads/documents/manuals/mfk1-man.pdf

Hrouda, F., 1982. Magnetic anisotropy of rocks and its application in geology
and geophysics. *Geophysical Surveys*, 5, pp.37–82.

Jelínek, V., 1981. Characterization of the magnetic fabric of rocks.
*Tectonophysics*, 79, pp.T63–T67.
