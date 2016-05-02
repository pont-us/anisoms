#!/usr/bin/python

"""
Reads AGICO RAN files and outputs the (sample corrected) AMS tensors.

"""

import sys, struct

header_format = '<H16s7s7s4s4s4s4s3s3s3s3s4s'
format = '<12s8f2s4h2s4h'

for filename in sys.argv[1:]:
    file = open(filename, mode='rb')
    header = file.read(64)
    headers = struct.unpack(header_format, header)
    num_recs = headers[0]-2
    for i in range(0, num_recs) :
        record = file.read(64)
    # (id, mean_sus, norm, k11, k22, k33, k12, k23, k13, c1, fol11, fol12, lin11, lin12, c2, fol21, fol22, lin21, lin22)
        fields = struct.unpack(format, record)
        name = fields[0].rstrip()
        name = name[0:-1] + '.' + name[-1:]
        print name, fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]

    file.close()
