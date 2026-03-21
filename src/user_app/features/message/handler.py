import platform
import subprocess

from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.message.response import MessageResponse


@FeatureRegistry.register(command_key="message", response_model=MessageResponse)
class MessageHandler(ResponseHandler):
    async def handle(self, command: MessageResponse):
        system = platform.system().lower()
        if system == "linux":
            try:
                subprocess.run(["notify-send", command.title, command.text], check=False)
            except Exception:
                pass
        elif system == "windows":
            try:
                cmd = f'msg * "{command.title}: {command.text}"'
                subprocess.run(cmd, shell=True, check=False)
            except Exception:
                pass
