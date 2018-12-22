#!/usr/bin/env python3
import tempfile
import aiocoap.resource as resource
import aiocoap
import asyncio
import threading

from file_resource import FileResource
from helpers import *


def create_file_resources(dfu_pkg_dir):
    manifest = read_manifest(dfu_pkg_dir + "/manifest.json")
    bin_file = read_file(dfu_pkg_dir + "/" + manifest["manifest"]["application"]["bin_file"])
    dat_file = read_file(dfu_pkg_dir + "/" + manifest["manifest"]["application"]["dat_file"])
    return FileResource(bin_file), FileResource(dat_file)


def create_dfu_server(bin_resource, dat_resource):
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('f',), bin_resource)
    root.add_resource(('i',), dat_resource)
    return aiocoap.Context.create_server_context(root)


def run_in_background(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_dfu_server(bin_resource, dat_resource):
    asyncio.Task(create_dfu_server(bin_resource, dat_resource))

    loop = asyncio.get_event_loop()
    t = threading.Thread(target=run_in_background, args=(loop,))
    t.start()


def main():
    dfu_pkg, target_addr = parse_arguments()
    print("Updating %d bytes to %s.." % (len(dfu_pkg), target_addr))

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_zip(dfu_pkg, tmpdir)
        bin_resource, dat_resource = create_file_resources(tmpdir)
        start_dfu_server(bin_resource, dat_resource)
        print("Started DFU server..")


if __name__ == "__main__":
    main()
