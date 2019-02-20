#!/usr/bin/python3

from anisoms.anisoms import read_asc, corrected_anisotropy_factor
import sys

F_LIMIT = 3.9715


def main():
    data = read_asc(sys.argv[1])
    total, valid = 0, 0
    with open(sys.argv[2], "w") as fh:
        fh.write(r"name,magsus,Ftest,F12,F23,PS1,PS2,PS3,"
                 "Lin,Fol,P,P',T,U,Q,E,P'a\n")
        for s in data.values():
            caf = corrected_anisotropy_factor(*[float(p)
                                                for p in s["principal_suscs"]])
            ps = s["principal_suscs"]
            f_test = float(s["Ftest"])
            total += 1
            if f_test > F_LIMIT:
                valid += 1
                fh.write("{name},{mean_susceptibility},"
                         "{Ftest},{F12test},{F23test},{PS1},{PS2},{PS3},"
                         "{L},{F},{P},{primeP},{T},{U},{Q},{E},{CAF:.8f}"
                         "\n".format(PS1=ps[0], PS2=ps[1], PS3=ps[2],
                                     CAF=caf, **s))

    print(total, valid)


if __name__ == "__main__":
    main()
