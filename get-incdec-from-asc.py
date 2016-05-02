#!/usr/bin/python

import fileinput

got_one = False
for line in fileinput.input():

    parts = line.split()
    if (len(parts)>1 and parts[1] == 'ANISOTROPY'):
        name = parts[0]
    if (got_one):
        got_one = False
        i1 = float(parts[2])
        i2 = float(parts[3])
        i3 = float(parts[4])
        name = name[0:-1] + '.' + name[-1:]
        print name, i1, d1, i2, d2, i3, d3
    if (len(parts) > 0 and parts[0] == "Specimen"):
        got_one = True
        d1 = float(parts[2])
        d2 = float(parts[3])
        d3 = float(parts[4])
