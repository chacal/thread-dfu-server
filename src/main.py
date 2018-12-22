#!/usr/bin/env python3
import tempfile

from helpers import *
from dfu_server import start_dfu_server


def main():
    dfu_pkg, target_addr = parse_arguments()
    print("Updating %d bytes to %s.." % (len(dfu_pkg), target_addr))

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_zip(dfu_pkg, tmpdir)
        start_dfu_server(tmpdir)
        print("Started DFU server..")


if __name__ == "__main__":
    main()
