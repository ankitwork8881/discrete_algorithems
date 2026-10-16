"""Command line interface.

    python -m discrete_algorithms permutations 4 [--method johnson_trotter]
    python -m discrete_algorithms partitions 4 [--method gray]
    python -m discrete_algorithms product 1,2 a,b,c
    python -m discrete_algorithms union 1,2,3 3,4
"""

import argparse

from . import partitions, permutations, sets


def _format_partition(blocks):
    return " | ".join(" ".join(map(str, block)) for block in blocks)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="discrete_algorithms")
    sub = parser.add_subparsers(dest="command", required=True)

    perm = sub.add_parser("permutations", help="list permutations of 1..n")
    perm.add_argument("n", type=int)
    perm.add_argument("--method", choices=permutations.GENERATORS, default="johnson_trotter")

    part = sub.add_parser("partitions", help="list set partitions of {1..n}")
    part.add_argument("n", type=int)
    part.add_argument("--method", choices=partitions.GENERATORS, default="gray")

    for name in ("union", "product"):
        op = sub.add_parser(name, help=f"{name} of comma-separated sets")
        op.add_argument("sets", nargs="+")

    args = parser.parse_args(argv)

    if args.command == "permutations":
        for p in permutations.GENERATORS[args.method](args.n):
            print(" ".join(map(str, p)))
    elif args.command == "partitions":
        for blocks in partitions.GENERATORS[args.method](args.n):
            print(_format_partition(blocks))
    else:
        parsed = [s.split(",") for s in args.sets]
        if args.command == "union":
            print(" ".join(sets.union(*parsed)))
        else:
            for t in sets.cartesian_product(*parsed):
                print("(" + ", ".join(t) + ")")


if __name__ == "__main__":
    main()
