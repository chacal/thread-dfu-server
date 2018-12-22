import argparse
import sys
import io
import zipfile
import json


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--dfu_pkg", help="DFU package (read from stdin, if omitted)", nargs="?",
                        type=argparse.FileType("rb"), default=sys.stdin.buffer)
    parser.add_argument("target_addr", help="IPv6 address for the DFU target")
    args = parser.parse_args()
    dfu_pkg = args.dfu_pkg.read()
    return dfu_pkg, args.target_addr


def extract_zip(zip_bytes, target_dir):
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_ref:
        zip_ref.extractall(target_dir)


def read_manifest(manifest_path):
    with open(manifest_path, 'r') as manifest:
        return json.load(manifest)


def read_file(path):
    f = open(path, "rb")
    content = f.read()
    f.close()
    return content
