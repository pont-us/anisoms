#!/usr/bin/python

from pyx import *
from ams_lib import PrincipalDirs, Direction
from math import sqrt, fabs, cos, sin, radians
import fileinput

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
        dirs = PrincipalDirs(
            Direction.from_polar_degrees(d1, i1),
            Direction.from_polar_degrees(d2, i2),
            Direction.from_polar_degrees(d3, i3))
        dirs.plot(canvas)
    if (len(parts) > 0 and parts[0] == "Specimen"):
#    if (len(parts) > 0 and parts[0] == "Geograph"):
        got_one = True
        d1 = float(parts[2])
        d2 = float(parts[3])
        d3 = float(parts[4])

canvas.writePDFfile("plot")
