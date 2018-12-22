#!/usr/bin/env python3

from file_resource import FileResource
from helpers import *
import tempfile


def create_file_resources(dfu_pkg_dir):
    manifest = read_manifest(dfu_pkg_dir + "/manifest.json")
    bin_file = read_file(dfu_pkg_dir + "/" + manifest["manifest"]["application"]["bin_file"])
    dat_file = read_file(dfu_pkg_dir + "/" + manifest["manifest"]["application"]["dat_file"])
    return FileResource(bin_file), FileResource(dat_file)


def main():
    dfu_pkg, target_addr = parse_arguments()
    print("Updating %d bytes to %s.." % (len(dfu_pkg), target_addr))

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_zip(dfu_pkg, tmpdir)
        bin_resource, dat_resource = create_file_resources(tmpdir)


if __name__ == "__main__":
    main()
