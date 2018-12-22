#!/usr/bin/env python3
import tempfile
import asyncio

from helpers import *
from dfu_server import start_dfu_server
from dfu_trigger import trigger_dfu


def main():
    dfu_pkg, target_addr = parse_arguments()
    log("Updating %d bytes to %s.." % (len(dfu_pkg), target_addr))

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_zip(dfu_pkg, tmpdir)
        bin_file, dat_file = start_dfu_server(tmpdir)
        trigger_dfu(target_addr, bin_file, dat_file)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
