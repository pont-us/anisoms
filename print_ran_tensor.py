#!/usr/bin/python3

"""
Reads AGICO RAN files and outputs the (sample corrected) AMS tensors.
"""

import sys
from ams_lib import directions_from_ran

for filename in sys.argv[1:]:
    dirs = directions_from_ran(filename)
    for name in dirs:
        f = dirs[name].tensor
        print(name, f[0], f[1], f[2], f[3], f[4], f[5])
