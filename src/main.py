#!/usr/bin/env python3
import tempfile
import asyncio
import aiocoap
import aiocoap.resource as resource

from helpers import *
from dfu_server import start_dfu_server
from dfu_trigger import trigger_dfu


def create_aiocoap_ctx():
    return aiocoap.Context.create_server_context(resource.Site())


async def main():
    dfu_pkg, target_addr = parse_arguments()
    log("Updating %d bytes to %s.." % (len(dfu_pkg), target_addr))

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_zip(dfu_pkg, tmpdir)

        ctx = await create_aiocoap_ctx()
        bin_file, dat_file = start_dfu_server(ctx, tmpdir)
        trigger_dfu(ctx, target_addr, bin_file, dat_file)


if __name__ == "__main__":
    asyncio.Task(main())
    asyncio.get_event_loop().run_forever()
