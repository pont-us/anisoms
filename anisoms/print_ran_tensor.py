#!/usr/bin/python3

"""Read Agico RAN files and print their AMS tensors.

The tensors are in the geographic co-ordinate system.
"""

import argparse

from anisoms import directions_from_ran


def main():
    parser = argparse.ArgumentParser(
        description="Read Agico RAN files and output their AMS tensors."
    )
    parser.add_argument("ranfile", nargs="+")
    args = parser.parse_args()
    for filename in args.ranfile:
        directions = directions_from_ran(filename)
        for name in directions:
            components = directions[name].tensor
            print(name, components[0], components[1], components[2],
                  components[3], components[4], components[5])


if __name__ == "__main__":
    main()
