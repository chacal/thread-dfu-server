#!/usr/bin/env python3

import asyncio
import aiocoap.resource as resource
import aiocoap
from helpers import *
import tempfile
import os


class FileResource(resource.Resource):
    def __init__(self, file_content):
        super().__init__()
        self.content = file_content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)


def main():
    dfu_pkg, target_addr = parse_arguments()
    print("Updating %d bytes to %s.." % (len(dfu_pkg), target_addr))

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_zip(dfu_pkg, tmpdir)
        print(os.listdir(tmpdir))


if __name__ == "__main__":
    main()
