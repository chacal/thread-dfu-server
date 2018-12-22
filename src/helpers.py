import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--dfu_pkg", help="DFU package (read from stdin, if omitted)", nargs="?",
                        type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("target_addr", help="IPv6 address for the DFU target")
    args = parser.parse_args()
    dfu_pkg = args.dfu_pkg.read()
    return dfu_pkg, args.target_addr
