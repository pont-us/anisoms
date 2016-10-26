#!/usr/bin/python

from pyx import canvas, path
from ams_lib import PrincipalDirs, Direction
import argparse

def main():
    parser = argparse.ArgumentParser(description="Plot AMS directions from an ASC file.")

    parser.add_argument("input", type=str, nargs=1,
                        help="ASC file containing data to plot")
    parser.add_argument("output", type=str, nargs=1,
                        help="filename for PDF output")
    parser.add_argument("-c", "--coordinates",
                        type=str,
                        choices=["s", "g"], default="g", 
                        help="co-ordinate system")
    parser.add_argument("-v", "--verbose",
                        action="store_true")
    args = parser.parse_args()

    mycanvas = canvas.canvas()
    mycanvas.stroke(path.circle(0, 0, 10))
    
    section_header = {"s" : "Specimen",
                      "g" : "Geograph"}[args.coordinates]
    
    got_one = False
    with open(args.input[0], "r") as fh:
        for line in fh.readlines():
        
            parts = line.split()
            if (got_one):
                got_one = False
                i1 = float(parts[2])
                i2 = float(parts[3])
                i3 = float(parts[4])
                if args.verbose:
                    print(d1, i1)
                dirs = PrincipalDirs(
                    Direction.from_polar_degrees(d1, i1),
                    Direction.from_polar_degrees(d2, i2),
                    Direction.from_polar_degrees(d3, i3))
                dirs.plot(mycanvas)
            if (len(parts) > 0 and parts[0] == section_header):
                got_one = True
                d1 = float(parts[2])
                d2 = float(parts[3])
                d3 = float(parts[4])
        
    mycanvas.writePDFfile(args.output[0])

if __name__ == "__main__":
    main()
