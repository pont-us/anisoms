#!/usr/bin/python

import fileinput
from optparse import OptionParser
import sys

parser = OptionParser(usage = "usage: %prog [options] inputfile")

parser.add_option('-d', '--dip', dest='formdip', default='0',
                  help='set formation dip', metavar='DEGREES')
parser.add_option('-a', '--azimuth', dest='formaz', default='0',
                  help='set formation azimuth', metavar='DEGREES')
parser.add_option('-m', '--magdec', dest='magdec', default='0',
                  help='set magnetic declination', metavar='DEGREES')
parser.add_option('-x', '--extended', dest='extended',
                  action="store_true", default=False,
                  help='append sample and formation data')
parser.add_option('-g', '--geographic', dest='geog',
                  action="store_true", default=False,
                  help='read geographic (not specimen) tensor')
parser.add_option('-t', '--dot', dest='dot',
                  action="store_true", default=False,
                  help='add a dot before last character of sample name')
parser.add_option('-p', '--params', dest='params',
                  action="store_true", default=False,
                  help='write P\' and T parameters, not tensor data')
(opt, args) = parser.parse_args()

tensor_label = 'Specimen'
if opt.geog: tensor_label = 'Geograph'
s_az, s_dip = 0,0
in_stream = sys.stdin
if len(args)>0: in_stream = open(args[0], 'r')

Pj, T = -99,-99
factors_line = -1
got_one = False
i=0
for line in in_stream:
    parts = line.split()
    if len(parts)>1:
        if parts[1] == 'ANISOTROPY': name = parts[0]
        if parts[0] == 'Azi': s_az = parts[1]
        if parts[0] == 'Dip': s_dip = parts[1]
    if (got_one):
        got_one = False
        k12 = float(parts[5])
        k23 = float(parts[6])
        k13 = float(parts[7])
        if opt.dot: name = name[0:-1] + '.' + name[-1:]
        fields = (name, k11, k22, k33, k12, k23, k13)
        if (opt.extended):
            more_fields = (s_az, s_dip, opt.formaz, opt.formdip, opt.magdec)
            fields += more_fields
        if opt.params: fields = (name, Pj, T)
        print ' '.join(map(str, fields))
    if (len(parts) > 0 and parts[0] == tensor_label):
        got_one = True
        k11 = float(parts[5])
        k22 = float(parts[6])
        k33 = float(parts[7])
    if 'Anisotropy factors' in line:
        factors_line = i+4
    if i==factors_line:
        Pj, T = parts[3], parts[4]
    i += 1

in_stream.close()
