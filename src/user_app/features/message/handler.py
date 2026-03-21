import os
import platform
import subprocess

from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.message.response import MessageResponse


@FeatureRegistry.register(command_key="message", response_model=MessageResponse)
class MessageHandler(ResponseHandler):
    async def handle(self, command: MessageResponse):
        print(f"DEBUG: [MESSAGE] Showing: {command.title}")
        system = platform.system().lower()
        try:
            if system == "linux":
                subprocess.run(
                    ["notify-send", command.title, command.text], check=False
                )
            elif system == "windows":
                cmd = f'msg * "{command.title}: {command.text}"'
                subprocess.run(cmd, shell=True, check=False)
            print("DEBUG: [MESSAGE] Success")
        except Exception as e:
            print(f"DEBUG: [MESSAGE] Error: {e}")
