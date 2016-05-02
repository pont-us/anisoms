#!/usr/bin/python

import sys, re
from math import log, sqrt, exp

#     L       F       P      'P           T       U       Q       E

infile = sys.argv[1]
outfile = sys.argv[2]

locations = (
(0, 0, 'name'),
(16, 2, 'magsus'),
(16, 4, 'Ftest'),
(16, 5, 'F12'),
(16, 6, 'F23'),
(23, 0, 'PS1'),
(23, 1, 'PS2'),
(23, 2, 'PS3'),
(31,0, 'Lin'),
(31,1, 'Fol'),
(31,2, 'P'),
(31,3, 'P\''),
(31,4, 'T'),
(31,5, 'U'),
(31,6, 'Q'),
(31,7, 'E'))

locmap = {}
for i in range(len(locations)):
    locmap[locations[i][2]] = i

F_LIMIT = 3.9715

def pprime(ps1, ps2, ps3):
    e1, e2, e3 = log(ps1), log(ps2), log(ps3)
    e = (e1+e2+e3)/3.
    ssq = (e1-e)**2.+(e2-e)**2.+(e3-e)**2.
    return exp(sqrt(2*ssq))
    
def read_chunk(lines, offset):
    rows = []
    i = offset
    while (i < len(lines)):
        line = lines[i].strip()
        parts = line.split()
        rows.append(parts)
        if re.match(r'^\d\d-\d\d-\d\d\d\d$', line):
            break
        i += 1
    result = []
    F = None
    for (x, y, name) in locations:
        result.append(rows[x][y])
    return result, i+1

instream = open(infile)
lines = instream.readlines()
instream.close()
i = 0
rows = []
total = 0
valid = 0
while (i < len(lines)-1):
    row, i = read_chunk(lines, i)
    pp = pprime(*[float(row[locmap[x]]) for x in ('PS1', 'PS2', 'PS3')])
    row.append('%.8f' % pp)
    total += 1
    F = float(row[locmap['Ftest']])
    if F>F_LIMIT:
        valid += 1
        rows.append(row)

outstream = open(outfile, 'w')
outstream.write(','.join(zip(*locations)[2]) + ',P\'a' + '\n')
for row in rows:
    outstream.write(','.join(row)+'\n')
outstream.close()
print total, valid
