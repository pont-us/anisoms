#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A library to read and manipulate AMS data from AGICO instruments."""

import sys
import re
import struct
from collections import OrderedDict
from math import sqrt, fabs, cos, sin, radians, atan2, degrees, log, exp

from numpy import argsort
from numpy.linalg import eigh
from pyx import path
import pyx

header_format = "<H16s7s7s4s4s4s4s3s3s3s3s4s"
data_format = "<12s8f2s4h2s4h"


class Direction:
    """A direction in three-dimensional space"""

    def __init__(self, components):
        """Create a direction from an (x, y, z) triplet"""
        self.x, self.y, self.z = components

    @classmethod
    def from_polar_degrees(cls, dec, inc):
        """Create a direction from declination and inclination in degrees"""
        dr = radians(dec)
        ir = radians(inc)
        return Direction((cos(ir) * cos(dr),
                          cos(ir) * sin(dr),
                          sin(ir)))

    @classmethod
    def make_lower_hemisphere(cls, x, y, z):
        """Create a lower-hemisphere direction from an (x, y, z) triplet.

        If z<0, the co-ordinates will be flipped when creating the
        Direction object."""
        if z < 0:
            x, y, z = -x, -y, -z
        return Direction((x, y, z))

    def project(self, scale=10):
        """Return a Lambert azimuthal equal-area projection of this direction
        """
        x, y, z = self.x, self.y, self.z
        h2 = x * x + y * y
        if h2 > 0:
            L = sqrt(1 - fabs(z))
        else:
            L = sqrt(h2)
        return y * L * scale, x * L * scale

    def plot(self, canvas, shape="s"):
        """Plot this direction on a pyx canvas.

        The direction will be transformed onto a Lambert equal-area 
        projection and plotted as a square, circle, or triangle
        (shape parameter: s, c, or t).
        """
        (x, y) = self.project()
        if shape == "s":
            canvas.stroke(path.rect(x - 0.1, y - 0.1, 0.2, 0.2))
        elif shape == "t":
            s = 0.15
            canvas.stroke(path.path(path.moveto(x, y + s),
                                    path.rlineto(-0.866 * s, -1.5 * s),
                                    path.rlineto(2 * .866 * s, 0),
                                    path.closepath()))
        elif shape == "c":
            canvas.stroke(path.circle(x, y, 0.1))

    def to_decinc(self):
        """Convert this direction to declination/inclination (degrees)"""
        x, y, z, = self.x, self.y, self.z
        dec = degrees(atan2(y, x))
        if dec < 0:
            dec += 360
        inc = degrees(atan2(z, sqrt(x * x + y * y)))
        return dec, inc


class PrincipalDirs:
    """A set of three principal directions"""

    def __init__(self, p1, p2, p3, tensor=None):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.tensor = tensor

    @classmethod
    def from_tensor(cls, tensor):
        """Make principal directions from a tensor.

        Any upward pointing directions are flipped, so all resulting
        directions are in the lower hemisphere (z>0).
        """
        (k11, k22, k33, k12, k23, k13) = tensor
        matrix = [[k11, k12, k13], [k12, k22, k23], [k13, k23, k33]]
        vals, vecs = eigh(matrix)
        perm = argsort(-vals)
        sorted_vecs = vecs[:, perm]
        dirs = [Direction.make_lower_hemisphere(*sorted_vecs[:, i])
                for i in (0, 1, 2)]
        return PrincipalDirs(dirs[0], dirs[1], dirs[2],
                             tensor=tensor)

    def plot(self, canvas, other=None):
        """Plot these directions on a pyx canvas.

        Plot these directions using standard AMS conventions: Lambert
        equal-area projection; major direction as a square; intermediate
        direction as a triangle; minor direction as a circle. If the
        "other" argument is provided, additionally draw a line from each
        direction in this PrincipalDirs object to its corresponding direction
        in the other PrincipalDirs object; this is intended to provide a
        visual comparison between pairs of PrincipalDirs objects, in
        particular when the directions are close to one another.
        """
        self.p1.plot(canvas, "s")
        self.p2.plot(canvas, "t")
        self.p3.plot(canvas, "c")
        if other is not None:
            for p in "p1", "p2", "p3":
                v1 = getattr(self, p).project()
                v2 = getattr(other, p).project()
                canvas.stroke(path.line(v1[0], v1[1], v2[0], v2[1]),
                              [pyx.style.linecap.round])

    def to_decinc_string(self):
        """Convert to a string of declination/inclination pairs.

        Output string is formatted as:

        dec1 inc1 dec2 inc2 dec3 inc3
        """
        di1 = self.p1.to_decinc()
        di2 = self.p2.to_decinc()
        di3 = self.p3.to_decinc()
        return "%3.3f %3.3f %3.3f %3.3f %3.3f %3.3f" % \
               (di1[0], di1[1], di2[0], di2[1], di3[0], di3[1])

    def to_decinc_tuples(self):
        """Return a 3-tuple of 2-tuples of declination/inclination pairs"""
        return self.p1.to_decinc(), self.p2.to_decinc(), self.p3.to_decinc()


def read_ran(filename):
    """Read AMS data from a RAN file.

    Returns a tuplet of (header_data, sample_data).

    header_data is an ordered dictionary, indexed by header field name,
    with an entry for each header data field.

    sample_data is an ordered dictionary, indexed by sample name, with
    an entry for each sample. Each entry in this dictionary is itself an
    ordered dictionary, indexed by sample data field name, with an entry
    for each item of sample data.

    Header field key names: ``num_recs``, ``int``, ``locality``, ``long``
    ``lat``, ``rock``, ``strati``, ``litho``, ``regio``, ``orient``. All
    of these have string values, except ``num_recs``, which has an ``int``
    value.
    
    Sample field key names: ``name``, ``mean_susceptibility``, ``frequency``,
    ``field``, ``tensor``, ``C1``, ``FOLI1``, ``LINE1``,
    ``C2``, ``FOLI2``, ``LINE2``
    """
    samples = OrderedDict()
    with open(filename, mode="rb") as fh:
        header = fh.read(64)
        headers = struct.unpack(header_format, header)
        #   0        1     2    3    4      5     6     7         8   9
        # N+2 LOCALITY LONGI LATI ROCK STRATI LITHO REGIO ORIENT.P. EOL
        num_recs = headers[0] - 2
        h = OrderedDict()
        h["num_recs"] = num_recs
        h["locality"], h["long"], h["lat"], h["rock"], h["strati"], \
            h["litho"], h["regio"] = headers[1:8]
        h["orient"] = headers[8:12]
        for i in range(0, num_recs):
            s = OrderedDict()
            record = fh.read(64)
            f = struct.unpack(data_format, record)
            name = f[0].rstrip().decode()
            #   0         1     2    3    4    5    6    7    8
            # (id, mean_sus, norm, k11, k22, k33, k12, k23, k13,
            #  c1, fol11, fol12, lin11, lin12, c2, fol21, fol22, lin21, lin22)
            samples[name] = s
            s["name"] = name
            s["mean_susceptibility"] = f[1]
            s["frequency"] = f[2] // 1000
            s["field"] = f[2] % 1000
            s["tensor"] = f[3:9]
            s["C1"], s["FOLI1"], s["LINE1"], \
                s["C2"], s["FOLI2"], s["LINE2"] = f[10:16]
    return h, samples


def read_asc(filename):
    """Read AMS data from an AGICO ASC file.

    Returns an ordered dictionary indexed by sample name. All values
    are returned as strings for maximum fidelity in format conversions.
    The ASC format can vary a little, so not every possible field is
    guaranteed to be present in every sample record.

    The ``vector_data`` key points to another dictionary, indexed by
    co-ordinate system ("Specimen", "Geograph", etc.). For each co-ordinate
    system present in the ASC data for the sample, the relevant key points
    to *another* dictionary with the keys "directions" and "tensor".
    "directions" points to a list of three tuples (the principal directions).
    "tensor" points to a list of six values defining the anisotropy tensor.
    So, for instance, to get the second principal direction in the geographic
    system of the sample "jeff", one could write:

    ``read_asc(filename)["jeff"]["vector_data"]["Geograph"]["directions"][1]``

    List of keys in the sample record:
    ``name``, ``program``, ``azimuth``, ``orientation_parameters``
    ``nominal_volume``, ``dip``, ``demagnetizing_factor_used``
    ``holder_susceptibility``, ``actual_volume``, ``T1``, ``F1`` ``L1``,
    ``T2``, ``F2``, ``L2``, ``field``, ``frequency``
    ``mean_susceptibility``, ``standard_error``, ``Ftest`` ``F12test``,
    ``F23test``, ``mean_susceptibility`` ``norming_factor``,
    ``standard_error``, ``Ftest``, ``F12test`` ``F23test``,
    ``principal_suscs``, ``a95s`` ``principal_susc_errs``, ``a95_errs``,
    ``L``, ``F``, ``P`` ``primeP``, ``T``, ``U``, ``Q``, ``E``,
    ``vector_data``, ``date``.
    """
    results = OrderedDict()

    with open(filename, "r") as fh:
        lines_raw = fh.readlines()

    lines = [line.rstrip() for line in lines_raw if len(line) > 1]

    fieldss = [line.split() for line in lines]

    i = 0
    s = None
    while i < len(lines):
        line = lines[i]
        fields = fieldss[i]
        if re.search("ANISOTROPY OF SUSCEPTIBILITY", line):
            s = OrderedDict()
            name = fields[0]
            results[name] = s
            s["name"] = name
            s["program"] = re.search(r"SUSCEPTIBILITY +(.*)$", line).group(1)
        elif re.search("^Azi  ", line):
            s["azimuth"] = fields[1]
            s["orientation_parameters"] = fields[4:8]
            s["nominal_volume"] = fields[10]
        elif re.search("^Dip  ", line):
            s["dip"] = fields[1]
            s["demagnetizing_factor_used"] = fields[5]
            s["holder_susceptibility"] = fields[6]
            s["actual_volume"] = fields[10]
        elif line == ("T1          F1          L1                "
                      "T2          F2          L2"):
            s["T1"], s["F1"], s["L1"], s["T2"], s["F2"], s["L2"] = fieldss[
                i + 1]
            i += 1
        elif line == ("  Field         Mean      Standard              "
                      "Tests for anisotropy"):
            # Only present in SAFYR files
            s["field"], s["frequency"], s["mean_susceptibility"], \
                s["standard_error"], s["Ftest"], s["F12test"], s["F23test"] = \
                fieldss[i + 2]
            i += 2
        elif line == ("  Mean         Norming    Standard              "
                      "Tests for anisotropy"):
            # Only present in SUSAR files
            s["mean_susceptibility"], s["norming_factor"], \
                s["standard_error"], s["Ftest"], s["F12test"], s["F23test"] = \
                fieldss[i + 2]
            i += 2
        elif line == ("          susceptibilities                   "
                      "Ax1        Ax2        Ax3"):
            # This line is only present if the sample was measured
            # using the automatic sample rotator (as opposed to
            # 15-position static specimen measurement).

            ps1, ps2, ps3, a95_1, a95_2, a95_3 = fieldss[i + 1]
            ps1e, ps2e, ps3e, a95_1e, a95_2e, a95_3e = fieldss[i + 2][1:]

            s["principal_suscs"] = [ps1, ps2, ps3]
            s["a95s"] = [a95_1, a95_2, a95_3]
            s["principal_susc_errs"] = [ps1e, ps2e, ps3e]
            s["a95_errs"] = [a95_1e, a95_2e, a95_3e]

            i += 2

        elif line == ("          susceptibilities                   "
                      "E12        E23        E13"):
            # This line is only present if the sample was measured
            # using 15-position static specimen measurement.

            print("Warning: ignoring 15-position static measurement data",
                  file=sys.stderr)
            pass  # Not handled yet

        elif line == ("       L       F       P      'P           "
                      "T       U       Q       E"):
            s["L"], s["F"], s["P"], s["primeP"], s["T"], \
                s["U"], s["Q"], s["E"] = fieldss[i + 1]
            i += 1
        elif re.match("(Specimen|Geograph|(Pale|Tect)o [12] )  D    ", line):
            if "vector_data" not in s:
                s["vector_data"] = {}
            vector_data = {}
            coord_system = line[:8].rstrip()
            s["vector_data"][coord_system] = vector_data

            # If the co-ordinate system string contains a space, it will have
            # been split into two fields, so all subsequent fields will be
            # offset by one.
            field_offset = 0
            if " " in coord_system:
                field_offset = 1

            d1, d2, d3, k11, k22, k33 = fields[(2 + field_offset):]
            i1, i2, i3, k12, k23, k13 = fieldss[i + 1][2:]
            vector_data["directions"] = [(d1, i1), (d2, i2), (d3, i3)]
            vector_data["tensor"] = [k11, k22, k33, k12, k23, k13]
            i += 1
        elif re.match(r"\d\d-\d\d-\d\d\d\d$", line):
            s["date"] = line
        i += 1

    return results


def directions_from_ran(filename):
    """Read directions from a RAN file.

    Directions are returned in the geographical co-ordinate system, since this
    is the only system used in a RAN file.

    :param filename: an Agico RAN file to read
    :return: an ordered dictionary whose keys are sample names and
             whose values are ``PrincipalDirs`` objects
    """
    headers, samples = read_ran(filename)
    result = OrderedDict()
    for sample in samples:
        result[sample] = PrincipalDirs.from_tensor(samples[sample]["tensor"])
    return result


def directions_from_asc_tensors(filename, system_header="Geograph"):
    """Calculate principal directions from tensors in an ASC file.

    The requested co-ordinate system is specified in the same string format
    that the ASC file itself uses: ``Specimen``, ``Geograph`` ``Paleo 1``,
    ``Paleo 2``, ``Tecto 1``, or ``Tecto 2``. If any sample in the file does
    not have data for the requested co-ordinate system, an exception will be
    raised.

    :param filename: an Agico ASC file to read
    :param system_header: a string specifying the co-ordinate system to use
    :return: an ordered dictionary whose keys are sample names and
             whose values are ``PrincipalDirs`` objects
    """
    asc_data = read_asc(filename)
    result = OrderedDict()
    for sample in asc_data.values():
        components = map(float, sample["vector_data"][system_header]["tensor"])
        result[sample["name"]] = PrincipalDirs.from_tensor(components)
    return result


def directions_from_asc_directions(filename, system_header):
    """Read principal directions from an ASC file.

    The requested co-ordinate system is specified in the same string format
    that the ASC file itself uses: ``Specimen``, ``Geograph`` ``Paleo 1``,
    ``Paleo 2``, ``Tecto 1``, or ``Tecto 2``. If any sample in the file does
    not have data for the requested co-ordinate system, it will be omitted
    from the returned dictionary.

    :param filename: an Agico ASC file to read
    :param system_header: a string specifying the co-ordinate system to use
    :return: an ordered dictionary whose keys are sample names and
             whose values are ``PrincipalDirs`` objects
    """

    raw_data = read_asc(filename)
    dirss = OrderedDict()

    for sample_name in raw_data.keys():
        vector_data = raw_data[sample_name]["vector_data"]
        decs_incs = vector_data[system_header]["directions"]
        (d1, i1), (d2, i2), (d3, i3) = \
            tuple((float(d), float(i)) for (d, i) in decs_incs)
        dirs = PrincipalDirs(
            Direction.from_polar_degrees(d1, i1),
            Direction.from_polar_degrees(d2, i2),
            Direction.from_polar_degrees(d3, i3))
        dirss[sample_name] = dirs
    return dirss


def corrected_anisotropy_factor(ps1, ps2, ps3):
    """Calculate the corrected anisotropy factor (*P′* or *P*\\ :sub:`j`)

    See Jelínek, 1981, "Characterization of the magnetic fabric of
    rocks" for definition. See also Hrouda, 1982, "Magnetic anisotropy
    of rocks and its application in geology and geophysics". Notation
    for this parameter is usually *P′* or *P*\\ :sub:`j`; in the ASC file it
    is ``'P``.

    Arguments are the three principal susceptibilities in descending
    order.
    """
    e1, e2, e3 = log(ps1), log(ps2), log(ps3)
    e = (e1 + e2 + e3) / 3.
    ssq = (e1 - e) ** 2. + (e2 - e) ** 2. + (e3 - e) ** 2.
    return exp(sqrt(2 * ssq))
