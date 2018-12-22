import aiocoap.resource as resource

from file_resource import FileResource
from helpers import *


def create_file_resources(dfu_pkg_dir):
    manifest = read_manifest(dfu_pkg_dir + "/manifest.json")
    bin_file = read_file(dfu_pkg_dir + "/" + manifest["manifest"]["application"]["bin_file"])
    dat_file = read_file(dfu_pkg_dir + "/" + manifest["manifest"]["application"]["dat_file"])
    return FileResource(bin_file), FileResource(dat_file)


def mount_resources(ctx, bin_resource, dat_resource):
    root = ctx.serversite
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('f',), bin_resource)
    root.add_resource(('i',), dat_resource)


def start_dfu_server(ctx, dfu_pkg_dir):
    bin_resource, dat_resource = create_file_resources(dfu_pkg_dir)
    mount_resources(ctx, bin_resource, dat_resource)
    log("Started DFU server..")
    return bin_resource.content, dat_resource.content
