#!/usr/bin/python3

"""
A program to produce comparative plots of AMS data from RAN and ASC
files, to check whether the ASC files have an acceptable level of
accuracy.
"""

from pyx import canvas, path
import sys
from ams_lib import directions_from_ran, directions_from_asc_tensors

def main():
    filename = sys.argv[1]
    ran = directions_from_ran(filename+'.RAN')
    asc = directions_from_asc_tensors(filename+'.ASC')

    print(ran)
    c = canvas.canvas()
    c.stroke(path.circle(0, 0, 10))
    for v in ran.values(): v.plot(c)
    for k in ran.keys():
        v1 = ran[k]
        v2 = asc[k]
        v1.plot(c, other=v2)
    c.writePDFfile("ran")

    c = canvas.canvas()
    c.stroke(path.circle(0, 0, 10))
    for v in asc.values(): v.plot(c)
    c.writePDFfile("asc")

if __name__=="__main__":
    main()
