#!/usr/bin/python

import fileinput

got_one = False
for line in fileinput.input():

    parts = line.split()
    if (len(parts)>1 and parts[1] == 'ANISOTROPY'):
        name = parts[0]
    if (len(parts)>0 and parts[0] == '716'):
        print name, parts[2]
