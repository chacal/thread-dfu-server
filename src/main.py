import asyncio
import aiocoap.resource as resource
import aiocoap


class TimeResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.content = ""
        self.set_content(b"This is the resource's default content. It is padded "
                         b"with numbers to be large enough to trigger blockwise "
                         b"transfer.\n")

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
                      resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('time',), TimeResource())
    # root.add_resource(('other', 'block'), BlockResource())
    # root.add_resource(('other', 'separate'), SeparateLargeResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
