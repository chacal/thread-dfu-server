import aiocoap.resource as resource
import aiocoap


class FileResource(resource.Resource):
    def __init__(self, file_content):
        super().__init__()
        self.content = file_content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
