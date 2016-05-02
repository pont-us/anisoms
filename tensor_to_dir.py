#!/usr/bin/python

import fileinput
from ams_lib import *

for line in fileinput.input():
    ks = map(float, line.split())
    ds = PrincipalDirs(ks)
    print ds.p1.to_decinc()
