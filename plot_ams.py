#!/usr/bin/python

from pyx import canvas, path
from ams_lib import PrincipalDirs, Direction
import argparse

def read_asc_dec_inc_data(filename, system_header, verbose):
    dirss = []
    got_one = False
    with open(filename, "r") as fh:
        for line in fh.readlines():
        
            parts = line.split()
            if (got_one):
                got_one = False
                i1 = float(parts[2])
                i2 = float(parts[3])
                i3 = float(parts[4])
                if verbose:
                    print(d1, i1)
                dirs = PrincipalDirs(
                    Direction.from_polar_degrees(d1, i1),
                    Direction.from_polar_degrees(d2, i2),
                    Direction.from_polar_degrees(d3, i3))
                dirss.append(dirs)
            if (len(parts) > 0 and parts[0] == system_header):
                got_one = True
                d1 = float(parts[2])
                d2 = float(parts[3])
                d3 = float(parts[4])

    return dirss

def make_dirs_plot(filename, dirss):
    mycanvas = canvas.canvas()
    mycanvas.stroke(path.circle(0, 0, 10))
    for dirs in dirss:
        dirs.plot(mycanvas)
    mycanvas.writePDFfile(filename)
    
def main():
    parser = argparse.ArgumentParser(description="Plot AMS directions from an ASC file.")

    parser.add_argument("input", type=str, nargs=1,
                        help="ASC file containing data to plot")
    parser.add_argument("output", type=str, nargs=1,
                        help="filename for PDF output")
    parser.add_argument("-c", "--coordinates",
                        type=str,
                        choices=["s", "g", "p1", "t1", "p2", "t2"],
                        default="g", 
                        help="co-ordinate system ([s]pecimen, "
                        "[g]eographic, [p]aleo, or [t]ectonic)")
    parser.add_argument("-v", "--verbose",
                        action="store_true")
    args = parser.parse_args()

    # See MFK-1 (Ver. 4.0 Mar-2009) manual for example of these section
    # headers in use.
    system_header = {"s"  : "Specimen",
                      "g"  : "Geograph",
                      "p1" : "Paleo 1",
                      "t1" : "Tecto 1",
                      "p2" : "Paleo 2",
                      "t2" : "Tecto 2"}[args.coordinates]

    dirss = read_asc_dec_inc_data(args.input[0], system_header, args.verbose)
    make_dirs_plot(args.output[0], dirss)

if __name__ == "__main__":
    main()
