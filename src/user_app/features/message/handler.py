import platform
import subprocess

from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.message.response import MessageResponse


@FeatureRegistry.register(command_key="message", response_model=MessageResponse)
class MessageHandler(ResponseHandler):
    async def handle(self, command: MessageResponse):
        if platform.system().lower() == "linux":
            subprocess.run(["notify-send", command.title, command.text])
