#!/usr/bin/python3

"""Convert AMS data from Agico ASC format to CSV format.

A simple command-line tool to extract a hard-coded selection of data from an
Agico AMS (anisotropy of magnetic susceptibility) file and output them as a
CSV file.
"""


import argparse

from anisoms import read_asc, corrected_anisotropy_factor


def main():
    parser = argparse.ArgumentParser(
        description="Convert anisotropy data from ASC format to CSV format")
    parser.add_argument("input", metavar="input_file", type=str,
                        help="input filename (Agico ASC format)")
    parser.add_argument("output", metavar="output_file", type=str,
                        help="output filename (comma separated value format)")
    parser.add_argument("-f", "--ftest", action="store_true",
                        help="only output samples which pass the F test")
    args = parser.parse_args()

    f_test_limit = 3.9715
    data = read_asc(args.input)
    total, valid = 0, 0
    with open(args.output, "w") as fh:
        fh.write(r"name,magsus,Ftest,F12,F23,PS1,PS2,PS3,"
                 "Lin,Fol,P,P',T,U,Q,E,P'a\n")
        for value in data.values():
            caf = corrected_anisotropy_factor(
                *[float(ps) for ps in value["principal_suscs"]])
            princ_suscs = value["principal_suscs"]
            f_test = float(value["Ftest"])
            total += 1
            if (not args.ftest) or (f_test > f_test_limit):
                valid += 1
                fh.write("{name},{mean_susceptibility},"
                         "{Ftest},{F12test},{F23test},{PS1},{PS2},{PS3},"
                         "{L},{F},{P},{primeP},{T},{U},{Q},{E},{CAF:.8f}"
                         "\n".format(PS1=princ_suscs[0], PS2=princ_suscs[1],
                                     PS3=princ_suscs[2], CAF=caf, **value))

    print("{} records read, {} records written".format(total, valid))


if __name__ == "__main__":
    main()
