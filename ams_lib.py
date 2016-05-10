#!/usr/bin/python

"""
A library for reading and manipulating AMS data from AGICO instruments.
"""

from pyx import canvas, path
from math import sqrt, fabs, cos, sin, radians, atan2, degrees
import struct
from numpy import argsort
from numpy.linalg import eigh

header_format = "<H16s7s7s4s4s4s4s3s3s3s3s4s"
data_format = "<12s8f2s4h2s4h"

class Direction:
    "A direction in three-dimensional space"

    def __init__(self, (x, y, z)):
        self.x, self.y, self.z = x, y, z

    @classmethod
    def from_polar_degrees(self, dec, inc):
        dr = radians(dec)
        ir = radians(inc)
        return Direction((cos(ir) * cos(dr),
                         cos(ir) * sin(dr),
                         sin(ir)))

    def project(self, scale=10):
        x, y, z = self.x, self.y, self.z
        h2 = x*x + y*y
        if (h2 > 0): L = sqrt(1 - fabs(z))
        else: L = sqrt(h2)
        return (y * L * scale, x * L * scale)

    def plot(self, c, shape = 's'):
        (x, y) = self.project()
        if shape == 's':
            c.fill(path.rect(x-0.1, y-0.1, 0.2, 0.2))
        elif shape == 't':
            c.fill(path.path(path.moveto(x, y),
                             path.rmoveto(0,0.1),
                             path.rlineto(-0.11547, -0.2),
                             path.rlineto(0.23094, 0)))
        elif shape == 'c':
            c.fill(path.circle(x, y, 0.1))

    def to_decinc(self):
        x,y,z, = self.x, self.y, self.z
        dec = degrees(atan2(y,x))
        if dec<0: dec += 360
        inc = degrees(atan2(z, sqrt(x*x + y*y)))
        return dec,inc

class PrincipalDirs:

    def __init__(self, p1, p2, p3):
        self.p1, self.p2, self.p3 = p1, p2, p3

    @classmethod
    def from_tensor(self, (k11, k22, k33, k12, k23, k13)):
        matrix = [[k11, k12, k13], [k12, k22, k23], [k13, k23, k33]]
        vals, vecs = eigh(matrix)
        perm = argsort(-vals)
        sorted_vecs = vecs[:, perm]
        return PrincipalDirs(Direction(sorted_vecs[:, 0]),
                             Direction(sorted_vecs[:, 1]),
                             Direction(sorted_vecs[:, 2]))

    def plot(self, c, other=None):
        self.p1.plot(c, 's')
        self.p2.plot(c, 't')
        self.p3.plot(c, 'c')
        if (other != None):
            v1 = self.p1.project()
            w = other.p1.project()
            a = w[0]
            b = w[1]
            c.stroke(path.line(v1[0], v1[1], a, b))

def read_ran(filename):
    result = {}
    file = open(filename, mode='rb')
    header = file.read(64)
    headers = struct.unpack(header_format, header)
    num_recs = headers[0]-2
    for i in range(0, num_recs) :
        record = file.read(64)
        f = struct.unpack(data_format, record)
        name = f[0].rstrip()
        # name = name[0:-1] + '.' + name[-1:]
        #   0         1     2    3    4    5    6    7    8
        # (id, mean_sus, norm, k11, k22, k33, k12, k23, k13,
        #  c1, fol11, fol12, lin11, lin12, c2, fol21, fol22, lin21, lin22)
        result[name] = PrincipalDirs.from_tensor(f[3:9])
    file.close()
    return result

def read_asc(filename):
    result = {}
    got_one = False
    file = open(filename, 'r')
    for line in file.readlines():
        parts = line.split()
        if len(parts)>5 and parts[5]=="SAFYR": name = parts[0]
        if (got_one):
            got_one = False
            k12 = float(parts[5])
            k23 = float(parts[6])
            k13 = float(parts[7])
            result[name] = PrincipalDirs.from_tensor((k11, k22, k33, k12, k23, k13))
        if (len(parts) > 0 and parts[0] == "Geograph"):
            got_one = True
            k11 = float(parts[5])
            k22 = float(parts[6])
            k33 = float(parts[7])
    file.close()
    return result
