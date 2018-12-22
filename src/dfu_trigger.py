import asyncio
from aiocoap import Context, Message, Code
import struct
import binascii

from helpers import *

TRIGGER_VERSION = 1
MULTICAST_MODE_BIT = 0x08
RESET_SUPPRESS_BIT = 0x04


def create_trigger(bin_file, dat_file):
    multicast_mode = False
    reset_suppress = False

    def crc(payload):
        return binascii.crc32(payload) & 0xffffffff

    # Structure format:
    # flags:      uint8_t
    #
    #    |V3|V2|V1|V0|M|R|R1|R0|
    #
    #    V3-V0: version
    #    M:     mcast mode
    #    R:     reset suppress
    #    R1-R0: reserved bits
    #
    # init size:  uint32_t
    # init crc:   uint32_t
    # image size: uint32_t
    # image crc:  uint32_t
    flags = (TRIGGER_VERSION << 4)
    if multicast_mode:
        flags |= MULTICAST_MODE_BIT
    if reset_suppress != 0:
        flags |= RESET_SUPPRESS_BIT

    return struct.pack(">BIIII",
                       flags,
                       len(dat_file),
                       crc(dat_file),
                       len(bin_file),
                       crc(bin_file))


async def send_trigger_request(target_addr, trigger):
    protocol = await Context.create_client_context()
    request = Message(code=Code.POST, uri="coap://[" + target_addr + "]/t", payload=trigger)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        log("Failed to fetch resource:")
        log(e)
    else:
        log("Trigger result: %s\n%r" % (response.code, response.payload))


async def start_sending_trigger(target_addr, trigger):
    log("Sending trigger in 2 seconds..")
    await asyncio.sleep(2)
    log("Sending trigger to %s" % target_addr)
    await send_trigger_request(target_addr, trigger)


def trigger_dfu(target_addr, bin_file, dat_file):
    trigger = create_trigger(bin_file, dat_file)
    asyncio.Task(start_sending_trigger(target_addr, trigger))
