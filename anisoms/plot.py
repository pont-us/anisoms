#!/usr/bin/python3

"""Plot AMS directions from ASC and RAN files.

This script produces equal-area PDF plots of AMS data from files in Agico ASC
and/or RAN format.
"""

import argparse

from pyx import canvas, path

from anisoms import directions_from_asc_directions
from anisoms import directions_from_asc_tensors, directions_from_ran


def main():
    parser = argparse.ArgumentParser(
        description="Plot AMS directions from ASC and RAN files.")

    parser.add_argument("-a", "--ascfile", type=str, action=OrderedArgsAction,
                        help="ASC file containing data to plot")
    parser.add_argument("-r", "--ranfile", type=str, action=OrderedArgsAction,
                        help="RAN file containing data to plot")
    parser.add_argument("output", type=str,
                        help="filename for PDF output")
    parser.add_argument("-c", "--coordinates",
                        type=str, action="append",
                        choices=["s", "g", "p1", "t1", "p2", "t2"],
                        default=[],
                        help="co-ordinate system for ASC file ([s]pecimen, "
                        "[g]eographic, [p]aleo, or [t]ectonic)")
    parser.add_argument("-d", "--directions",
                        type=str, action="append",
                        choices=["p", "t"],
                        default=[],
                        help="source for directions in ASC file ([p]rincipal"
                             "directions or [t]ensors)")
    parser.add_argument("-v", "--verbose",
                        action="store_true")
    args = parser.parse_args()

    if "ordered_args" not in args:
        print("Use --ascfile and/or --ranfile "
              "to specify one or two input files.")
        exit(1)

    if len(args.ordered_args) > 2:
        print("A maximum of two input files may be specified.")
        exit(1)

    # Add default settings in case not enough arguments were given for the
    # supplied ASC files.
    coords_types = args.coordinates + ["g", "g"]
    direction_types = args.directions + ["p", "p"]

    direction_sets = []
    for filetype, filename in args.ordered_args:
        direction_sets.append(read_data(filetype,
                              filename,
                              coords_types,
                              direction_types))

    if len(direction_sets) == 1:
        make_dirs_plot(args.output, direction_sets[0])
    else:
        make_dirs_plot(args.output, direction_sets[0], other=direction_sets[1])


class OrderedArgsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if "ordered_args" not in namespace:
            setattr(namespace, "ordered_args", [])
        previous = namespace.ordered_args
        previous.append((self.dest, values))
        setattr(namespace, "ordered_args", previous)


def read_data(filetype, filename, coords_types, direction_types):
    # See MFK-1 (Ver. 4.0 Mar-2009) manual for an example of these section
    # headers in use.
    header_codes = {"s": "Specimen",
                    "g": "Geograph",
                    "p1": "Paleo 1",
                    "t1": "Tecto 1",
                    "p2": "Paleo 2",
                    "t2": "Tecto 2"}
    if filetype == "ascfile":
        coords_type = coords_types.pop(0)
        direction_type = direction_types.pop(0)
        header = header_codes[coords_type]
        if direction_type == "t":  # tensor
            return directions_from_asc_tensors(filename, header)
        else:  # principal directions
            return directions_from_asc_directions(filename, header)
    else:  # RAN file
        return directions_from_ran(filename)


def make_dirs_plot(filename, dirs_dict, other=None):
    plot_canvas = canvas.canvas()
    plot_canvas.stroke(path.circle(0, 0, 10))
    for sample_name in dirs_dict.keys():
        if other is None:
            dirs_dict[sample_name].plot(plot_canvas)
        else:
            dirs_dict[sample_name].plot(plot_canvas, other=other[sample_name])
    plot_canvas.writePDFfile(filename)


if __name__ == "__main__":
    main()
