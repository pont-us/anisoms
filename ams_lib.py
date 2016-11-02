#!/usr/bin/python3

"""
A library for reading and manipulating AMS data from AGICO instruments.
"""

from pyx import canvas, path
from math import sqrt, fabs, cos, sin, radians, atan2, degrees, log, exp
import struct
from numpy import argsort
from numpy.linalg import eigh
from collections import OrderedDict
import re

header_format = "<H16s7s7s4s4s4s4s3s3s3s3s4s"
data_format = "<12s8f2s4h2s4h"

class Direction:
    "A direction in three-dimensional space"

    def __init__(self, components):
        self.x, self.y, self.z = components

    @classmethod
    def from_polar_degrees(cls, dec, inc):
        dr = radians(dec)
        ir = radians(inc)
        return Direction((cos(ir) * cos(dr),
                         cos(ir) * sin(dr),
                         sin(ir)))

    @classmethod
    def make_lower_hemisphere(cls, x, y, z):
        if z<0: x, y, z = -x, -y, -z
        return Direction((x, y, z))

    def project(self, scale=10):
        x, y, z = self.x, self.y, self.z
        h2 = x*x + y*y
        if (h2 > 0): L = sqrt(1 - fabs(z))
        else: L = sqrt(h2)
        return (y * L * scale, x * L * scale)

    def plot(self, c, shape = 's'):
        (x, y) = self.project()
        if shape == 's':
            c.stroke(path.rect(x-0.1, y-0.1, 0.2, 0.2))
        elif shape == 't':
            s=0.15
            c.stroke(path.path(path.moveto(x, y+s),
                               path.rlineto(-0.866*s, -1.5*s),
                               path.rlineto(2*.866*s, 0),
                               path.lineto(x, y+s)))
        elif shape == 'c':
            c.stroke(path.circle(x, y, 0.1))

    def to_decinc(self):
        x,y,z, = self.x, self.y, self.z
        dec = degrees(atan2(y,x))
        if dec<0: dec += 360
        inc = degrees(atan2(z, sqrt(x*x + y*y)))
        return dec,inc

class PrincipalDirs:

    "A set of three principal directions"

    def __init__(self, p1, p2, p3, tensor = None):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.tensor = tensor

    @classmethod
    def from_tensor(cls, tensor):
        """Make principal directions from a tensor.

        Any upward pointing directions are flipped, so all resulting
        directions are in the lower hemisphere.
        """
        (k11, k22, k33, k12, k23, k13) = tensor
        matrix = [[k11, k12, k13], [k12, k22, k23], [k13, k23, k33]]
        vals, vecs = eigh(matrix)
        perm = argsort(-vals)
        sorted_vecs = vecs[:, perm]
        dirs = [Direction.make_lower_hemisphere(*sorted_vecs[:, i])
                for i in (0, 1, 2)]
        return PrincipalDirs(dirs[0], dirs[1], dirs[2],
                             tensor = tensor)

    def plot(self, c, other=None):
        self.p1.plot(c, 's')
        self.p2.plot(c, 't')
        self.p3.plot(c, 'c')
        if (other != None):
            for p in "p1", "p2", "p3":
                v1 = getattr(self, p).project()
                v2 = getattr(other, p).project()
                c.stroke(path.line(v1[0], v1[1], v2[0], v2[1]))

    def to_decinc_string(self):
        di1 = self.p1.to_decinc()
        di2 = self.p2.to_decinc()
        di3 = self.p3.to_decinc()
        return "%3.3f %3.3f %3.3f %3.3f %3.3f %3.3f" % \
        (di1[0], di1[1], di2[0], di2[1], di3[0], di3[1])

def directions_from_ran(filename):
    result = OrderedDict()
    with open(filename, mode='rb') as fh:
        header = fh.read(64)
        headers = struct.unpack(header_format, header)
        num_recs = headers[0]-2
        for i in range(0, num_recs):
            record = fh.read(64)
            f = struct.unpack(data_format, record)
            name = f[0].rstrip().decode()
            #   0         1     2    3    4    5    6    7    8
            # (id, mean_sus, norm, k11, k22, k33, k12, k23, k13,
            #  c1, fol11, fol12, lin11, lin12, c2, fol21, fol22, lin21, lin22)
            result[name] = PrincipalDirs.from_tensor(f[3:9])
    return result

def directions_from_asc_tensors(filename):
    asc_data = read_asc(filename)
    result = OrderedDict()
    for sample in asc_data.values():
        components = map(float, sample["vector_data"]["Geograph"]["tensor"])
        result[sample["name"]] = PrincipalDirs.from_tensor(components)
    return result

def read_asc(filename):
    results = OrderedDict()

    with open(filename, "r") as fh:
        lines_raw = fh.readlines()
    
    lines = [line.rstrip() for line in lines_raw if len(line)>1]

    fieldss = [line.split() for line in lines]

    i = 0
    s = None
    while i < len(lines):
        line = lines[i]
        fields = fieldss[i]
        if re.search("ANISOTROPY OF SUSCEPTIBILITY", line):
            s = {}
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
            s["T1"], s["F1"], s["L1"], s["T2"], s["F2"], s["L2"] = fieldss[i+1]
            i += 1
        elif line == ("  Field         Mean      Standard              "
                      "Tests for anisotropy"):
            # Only present in SAFYR files
            s["field"], s["frequency"], s["mean_susceptibility"], \
                s["standard_error"], s["Ftest"], s["F12test"], s["F23test"] = fieldss[i+2]
            i += 2
        elif line == ("  Mean         Norming    Standard              "
                      "Tests for anisotropy"):
            # Only present in SUSAR files
            s["mean_susceptibility"], s["norming_factor"], \
                s["standard_error"], s["Ftest"], s["F12test"], s["F23test"] = fieldss[i+2]
            i += 2
        elif line == ("          susceptibilities                   "
                      "Ax1        Ax2        Ax3"):
            # This line is only present if the sample was measured
            # using the automatic sample rotator (as opposed to
            # 15-position static specimen measurement).

            ps1, ps2, ps3, a95_1, a95_2, a95_3 = fieldss[i+1]
            ps1e, ps2e, ps3e, a95_1e, a95_2e, a95_3e = fieldss[i+2][1:]

            s["principal_suscs"] = [ps1, ps2, ps3]
            s["a95s"] = [a95_1, a95_2, a95_3]
            s["principal_susc_errs"] = [ps1e, ps2e, ps3e]
            s["a95_errs"] = [a95_1e, a95_2e, a95_3e]

            i += 2

        elif line == ("          susceptibilities                   "
                      "E12        E23        E13"):
            # This line is only present if the sample was measured
            # using 15-position static specimen measurement.

            pass # Not handled yet

        elif line == ("       L       F       P      'P           "
                      "T       U       Q       E"):
            s["L"], s["F"], s["P"], s["primeP"], s["T"], \
                s["U"], s["Q"], s["E"] = fieldss[i+1]
            i += 1
        elif re.match("(Specimen|Geograph|(Pale|Tect)o [12] )  D    ", line):
            if "vector_data" not in s:
                s["vector_data"] = {}
            vector_data = {}
            coord_system = line[:8].rstrip()
            s["vector_data"][coord_system] = vector_data
            # If the co-ordinate system string contains a space,
            # it will have been split into two fields, so all
            # subsequent fields will be offset by one.
            field_offset = 0
            if " " in coord_system: field_offset = 1
            d1, d2, d3, k11, k22, k33 = fields[(2 + field_offset):]
            i1, i2, i3, k12, k23, k13 = fieldss[i+1][2:]
            vector_data["directions"] = [(d1, i1), (d2, i2), (d3, i3)]
            vector_data["tensor"] = [k11, k22, k33, k12, k23, k13]
            i += 1
        elif re.match(r"\d\d-\d\d-\d\d\d\d$", line):
            s["date"] = line
        i += 1

    return results

def corrected_anisotropy_factor(ps1, ps2, ps3):
    """Calculate the corrected anisotropy factor (P' or Pj)

    See Jelínek, 1981, "Characterization of the magnetic fabric of
    rocks" for definition. See also Hrouda, 1982, "Magnetic anisotropy
    of rocks and its application in geology and geophysics". Notation
    for this parameter is usually $P'$ or $P_j$; in the ASC file it
    is "'P".

    Arguments are the three principal susceptibilities in descending
    order.
    """
    e1, e2, e3 = log(ps1), log(ps2), log(ps3)
    e = (e1+e2+e3)/3.
    ssq = (e1-e)**2.+(e2-e)**2.+(e3-e)**2.
    return exp(sqrt(2*ssq))
    
