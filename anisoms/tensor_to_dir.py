#!/usr/bin/python3

""" Convert AMS tensors to principal directions

Input: tensors, one to a line, six elements separated by whitespace
Output: corresponding principal direction for each tensor

Example usage:

./params_from_asc.py -p tensor test_data/D_200.ASC | cut -d' ' -f2-7 | ./tensor_to_dir.py

"""

import fileinput
from anisoms import PrincipalDirs

for line in fileinput.input():
    ks = map(float, line.split())
    ds = PrincipalDirs.from_tensor(ks)
    print(*ds.p1.to_decinc())
