#!/usr/bin/python3

import argparse
import re

class SampleData(object):
    pass

class Directions(object):
    pass

def process_lines(lines):
    
    current_sample = None
    current_dirs = None
    samples = []

    factors_line = -1
    linenum = 0
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

        if (current_dirs): # previous line was "Specimen"/"Geograph"
            current_dirs.i1 = parts[2]
            current_dirs.i2 = parts[3]
            current_dirs.i3 = parts[4]
            current_dirs.k12 = parts[5]
            current_dirs.k23 = parts[6]
            current_dirs.k13 = parts[7]
            current_dirs = None

        if (len(parts) > 0 and
            (parts[0] == "Specimen" or parts[0] == "Geograph")):
            current_dirs = Directions()
            if parts[0] == "Specimen":
                current_sample.dirs_specimen = current_dirs
            elif parts[0] == "Geograph":
                current_sample.dirs_geograph = current_dirs
            else:
                assert(False)
            specimen_line_found = True
            current_dirs.d1 = parts[2]
            current_dirs.d2 = parts[3]
            current_dirs.d3 = parts[4]
            current_dirs.k11 = parts[5]
            current_dirs.k22 = parts[6]
            current_dirs.k33 = parts[7]

        if "Anisotropy factors" in line:
            factors_line = linenum + 4

        if (linenum == factors_line):
            current_sample.Pj = parts[3]
            current_sample.T = parts[4]

        linenum += 1
        
    return samples

def print_data(samples, parameter, system):
    for sample in samples:
        if system == "specimen":
            dirs = sample.dirs_specimen
        elif system == "geograph":
            dirs = sample.dirs_geograph
        else:
            assert(False)
        if parameter == "magsus":
            print(sample.name, sample.mag_sus)
        elif parameter == "incdec":
            print(sample.name,
                  dirs.i1, dirs.d1, dirs.i2,
                  dirs.d2, dirs.i3, dirs.d3)
        elif parameter == "tensor":
            print(sample.name,
                  dirs.k11, dirs.k22, dirs.k33,
                  dirs.k12, dirs.k23, dirs.k13)
        elif parameter == "pj":
            print(sample.name, sample.Pj)
        elif parameter == "t":
            print(sample.name, sample.T)

def main():
    parser = argparse.ArgumentParser(description =
        "Extract parameters from an Agico ASC file")
    parser.add_argument("ascfiles", metavar = "asc-file",
                        type = str, nargs = "+",
                        help = "an ASC file to read")
    parser.add_argument('--param', "-p", metavar = "parameter-name",
                        type = str, default="magsus",
                        choices = ["magsus", "incdec", "tensor", "pj", "t"],
                        help = "Parameter to extract"
                        "(magsus, incdec, pj, t, or tensor)")
    parser.add_argument('--system', "-s", metavar = "coordinate-system",
                        type = str, default="specimen",
                        choices = ["specimen", "geograph"],
                        help = "Co-ordinate system (specimen or geograph)")
    args = parser.parse_args()
    for filename in args.ascfiles:
        with open(filename) as fh:
            lines = fh.readlines()
            samples = process_lines(lines)
            print_data(samples, args.param, args.system)
    # TODO if no files use stdin

if __name__=="__main__":
    main()
