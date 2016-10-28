#!/usr/bin/python3

""" Convert AMS tensors to principal directions

Input: tensors, one to a line, six elements separated by whitespace
Output: corresponding principal direction for each tensor

Example usage:

./get-tensor-from-asc.py test_data/D_200.ASC | cut -d' ' -f2-7 | ./tensor_to_dir.py

"""

import fileinput
from ams_lib import PrincipalDirs

for line in fileinput.input():
    ks = map(float, line.split())
    ds = PrincipalDirs.from_tensor(ks)
    print(ds.p1.to_decinc())
