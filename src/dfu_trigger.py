import asyncio
from aiocoap import Context, Message, Code

from helpers import *


async def send_trigger_request(target_addr):
    protocol = await Context.create_client_context()
    request = Message(code=Code.GET, uri="coap://localhost/.well-known/core")

    try:
        response = await protocol.request(request).response
    except Exception as e:
        log("Failed to fetch resource:")
        log(e)
    else:
        log("Trigger result: %s\n%r" % (response.code, response.payload))


async def start_sending_trigger(target_addr):
    log("Sending trigger in 2 seconds..")
    await asyncio.sleep(2)
    log("Sending trigger to %s" % target_addr)
    await send_trigger_request(target_addr)


def trigger_dfu(target_addr):
    asyncio.Task(start_sending_trigger(target_addr))
