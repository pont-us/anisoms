#!/usr/bin/python

from pyx import *
from math import sqrt, fabs, cos, sin, radians
import fileinput

class Direction:

    def __init__(self, dec, inc):
        self.dec, self.inc = dec, inc

    def project(self):
        (x, y, z) = self.toCart()
        h2 = x*x + y*y
        if (h2 > 0):
            L = sqrt(1 - fabs(z))
        else:
            L = sqrt(h2)
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

canvas = canvas.canvas()
canvas.stroke(path.circle(0, 0, 10))

got_one = False
for line in fileinput.input():

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
    if (len(parts) > 0 and parts[0] == "Specimen"):
#    if (len(parts) > 0 and parts[0] == "Geograph"):
        got_one = True
        d1 = float(parts[2])
        d2 = float(parts[3])
        d3 = float(parts[4])

canvas.writePDFfile("plot")
