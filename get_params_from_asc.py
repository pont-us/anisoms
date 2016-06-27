#!/usr/bin/python

from __future__ import print_function
import argparse
import re

class SampleData(object):
    pass

def process_lines(lines):
    
    specimen_line_found = False
    current_sample = None
    samples = []

    for line in lines:
    
        parts = line.split()

        if len(parts)>1 and parts[1] == 'ANISOTROPY':
            current_sample = SampleData()
            samples.append(current_sample)
            current_sample.name = parts[0]

        if (len(parts)>2 and
            re.match("^F[123]$", parts[1]) and
            parts[2] != "L1"):
            current_sample.mag_sus = parts[2]

        if (specimen_line_found):
            specimen_line_found = False
            current_sample.i1 = parts[2]
            current_sample.i2 = parts[3]
            current_sample.i3 = parts[4]

        if (len(parts) > 0 and parts[0] == "Specimen"):
            specimen_line_found = True
            current_sample.d1 = parts[2]
            current_sample.d2 = parts[3]
            current_sample.d3 = parts[4]

    return samples

def print_data(samples, parameter):
    for sample in samples:
        if parameter == "magsus":
            print(sample.name, sample.mag_sus)
        elif parameter == "incdec":
            print(sample.name,
                  sample.i1, sample.d1, sample.i2,
                  sample.d2, sample.i3, sample.d3)

def main():
    parser = argparse.ArgumentParser(description =
        "Extract parameters from an Agico ASC file")
    parser.add_argument("ascfiles", metavar = "asc-file",
                        type = str, nargs = "+",
                        help = "an ASC file to read")
    parser.add_argument('--param', "-p", metavar = "parameter-name",
                        type = str, default="magsus",
                        help = "Parameter to extract (magsus or incdec)")
    args = parser.parse_args()
    for filename in args.ascfiles:
        with open(filename) as fh:
            lines = fh.readlines()
            samples = process_lines(lines)
            print_data(samples, args.param)
    # TODO if no files use stdin

if __name__=="__main__":
    main()
