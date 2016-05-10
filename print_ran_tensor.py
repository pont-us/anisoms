#!/usr/bin/python

"""
Reads AGICO RAN files and outputs the (sample corrected) AMS tensors.
"""

import sys
from ams_lib import *

for filename in sys.argv[1:]:
    dirs = read_ran(filename)
    for name in dirs:
        name2 = name[0:-1] + '.' + name[-1:]
        f = dirs[name].tensor
        print name2, f[0], f[1], f[2], f[3], f[4], f[5]
