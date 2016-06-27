#!/usr/bin/python

import argparse
import re

def process_lines(lines):
    for line in lines:
    
        parts = line.split()
        if len(parts)>1 and parts[1] == 'ANISOTROPY':
            name = parts[0]
        if (len(parts)>2 and
            re.match("^F[123]$", parts[1]) and
            parts[2] != "L1"):
            print name, parts[2] # mag. sus.
    
def main():
    parser = argparse.ArgumentParser(description =
        "Extract parameters from an Agico ASC file")
    parser.add_argument("ascfiles", metavar = "asc-file",
                        type = str, nargs = "+",
                        help = "an ASC file to read")
    args = parser.parse_args()
    for filename in args.ascfiles:
        with open(filename) as fh:
            lines = fh.readlines()
            process_lines(lines)
    # TODO if no files use stdin

if __name__=="__main__":
    main()
