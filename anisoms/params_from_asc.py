#!/usr/bin/python3

"""Print selected parameters from an Agico ASC file."""

import argparse
import sys

from anisoms import read_asc


def print_data(samples, parameter, system):
    for sample in samples.values():
        if system == "specimen":
            dirs = sample["vector_data"]["Specimen"]
        elif system == "geograph":
            dirs = sample["vector_data"]["Geograph"]
        else:
            sys.stderr.write("Unknown co-ordinate systerm \"{}\"".
                             format(system))
            sys.exit(1)
        if parameter == "magsus":
            print(sample["name"], sample["mean_susceptibility"])
        elif parameter == "incdec":
            d = dirs["directions"]
            print(sample["name"], d[0][1], d[0][0],
                  d[1][1], d[1][0], d[2][1], d[2][0])
        elif parameter == "tensor":
            t = dirs["tensor"]
            print(sample["name"], *t)
        elif parameter == "pj":
            print(sample["name"], sample["primeP"])
        elif parameter == "t":
            print(sample["name"], sample["T"])


def main():
    parser = argparse.ArgumentParser(description="Print selected parameters "
                                                 "from an Agico ASC file")
    parser.add_argument("ascfiles", metavar="asc-file",
                        type=str, nargs="+",
                        help="an ASC file to read")
    parser.add_argument('--param', "-p", metavar="parameter-name",
                        type=str, default="magsus",
                        choices=["magsus", "incdec", "tensor", "pj", "t"],
                        help="Parameter to extract"
                             "(magsus, incdec, pj, t, or tensor)")
    parser.add_argument('--system', "-s", metavar="coordinate-system",
                        type=str, default="specimen",
                        choices=["specimen", "geograph"],
                        help="Co-ordinate system (specimen or geograph)")
    args = parser.parse_args()
    for filename in args.ascfiles:
        samples = read_asc(filename)
        print_data(samples, args.param, args.system)


if __name__ == "__main__":
    main()
