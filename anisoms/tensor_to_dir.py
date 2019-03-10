#!/usr/bin/python3

"""Print the first principal directions of supplied tensors.

Input: tensors, one to a line, six elements separated by whitespace
Output: first principal direction for each tensor (declination inclination)

Example usage::

    ./params_from_asc.py -p tensor DATAFILE.ASC | \\
        cut -d' ' -f2-7 | \\
        ./tensor_to_dir.py
"""

import fileinput
import argparse
from anisoms import PrincipalDirs


def main():
    parser = argparse.ArgumentParser(
        description="Print the first principal directions of tensors"
    )
    parser.add_argument("file", nargs="*",
                        help="text file containing one tensor per "
                             "line. If no files are given, data will "
                             "be read from the standard input.")
    args = parser.parse_args()
    for line in fileinput.input(files=args.file):
        components = map(float, line.split())
        directions = PrincipalDirs.from_tensor(components)
        print(*directions.p1.to_decinc())


if __name__ == "__main__":
    main()
