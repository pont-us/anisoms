#!/usr/bin/python

'''
A program to produce comparative plots of AMS data from RAN and ASC
files, to check whether the ASC files have an acceptable level of
accuracy.
'''

from pyx import *
from math import sqrt, fabs, cos, sin, radians
import sys, struct

header_format = '<H16s7s7s4s4s4s4s3s3s3s3s4s'
format = '<12s8f2s4h2s4h'

class Direction:

    def __init__(self, dec, inc):
        self.dec, self.inc = dec, inc

    def project(self):
        (x, y, z) = self.toCart()
        h2 = x*x + y*y
        if (h2 > 0): L = sqrt(1 - fabs(z))
        else: L = sqrt(h2)
        return (y * L, x * L)

    def toCart(self):
        dr = radians(self.dec)
        ir = radians(self.inc)
        return (cos(ir) * cos(dr), cos(ir) * sin(dr), sin(ir))

class PrincipalDirs:

    def __init__(self, p1, p2, p3):
        self.p1, self.p2, self.p3 = p1, p2, p3

    def plot(self, c):
        (x, y) = self.p1.project()
        c.fill(path.rect(x*10-0.05, y*10-0.05, 0.1, 0.1))
        (x, y) = self.p2.project()
        c.fill(path.path(path.moveto(x*10, y*10),
                         path.rmoveto(0,0.1),
                         path.rlineto(-0.11547, -0.2),
                         path.rlineto(0.23094, 0)))
        (x, y) = self.p3.project()
        c.fill(path.circle(x*10, y*10, 0.1))

def read_ran(filename):
    result = {}
    file = open(filename, mode='rb')
    header = file.read(64)
    headers = struct.unpack(header_format, header)
    num_recs = headers[0]-2
    for i in range(0, num_recs) :
        record = file.read(64)
        f = struct.unpack(format, record)
        name = f[0].rstrip()
        # name = name[0:-1] + '.' + name[-1:]
        #   0         1     2    3    4    5    6    7    8
        # (id, mean_sus, norm, k11, k22, k33, k12, k23, k13,
        #  c1, fol11, fol12, lin11, lin12, c2, fol21, fol22, lin21, lin22)
        result[name] = f[3:8]
    file.close()
    return result

def read_asc(filename):
    result = {}
    got_one = False
    file = open(filename, 'r')
    for line in file.readlines():
        parts = line.split()
        if (got_one):
            got_one = False
            i1 = float(parts[2])
            i2 = float(parts[3])
            i3 = float(parts[4])
            print d1, i1
            dirs = PrincipalDirs(Direction(d1, i1), Direction(d2, i2),
                                 Direction(d3, i3))
            dirs.plot(canvas)
        if (len(parts) > 0 and parts[0] == "Geograph"):
            got_one = True
            d1 = float(parts[2])
            d2 = float(parts[3])
            d3 = float(parts[4])
    file.close()
    return result

filename = sys.argv[1]
ran = read_ran(filename+'.RAN')
asc = read_asc(filename+'.ASC')


canvas = canvas.canvas()
canvas.stroke(path.circle(0, 0, 10))
canvas.writePDFfile("plot")
