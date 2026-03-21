import asyncio
import os
import subprocess

from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler

from .request import ShellRequest
from .responses import ShellResponse


@FeatureRegistry.register(command_key="shell", response_model=ShellResponse)
class ShellHandler(ResponseHandler[ShellResponse]):
    async def handle(self, command: ShellResponse):
        print(f"DEBUG: [SHELL] Executing: {command.command}")

        env = os.environ.copy()

        try:
            process = await asyncio.create_subprocess_shell(
                command.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )

            stdout, stderr = await process.communicate()

            def decode_output(raw_bytes: bytes) -> str:
                for enc in ("utf-8", "cp866", "cp1251"):
                    try:
                        return raw_bytes.decode(enc)
                    except UnicodeDecodeError:
                        pass
                return raw_bytes.decode("utf-8", errors="replace")

            output = decode_output(stdout).strip()
            error = decode_output(stderr).strip()
            result_text = output if output else error

            print(f"DEBUG: [SHELL] Result: {result_text[:50]}...")

            response = ShellRequest(
                event_id=command.event_id,
                type="shell_result",
                stdout=result_text,
                stderr=error,
                exit_code=process.returncode or 0,
            )
            await self.bus.publish(response)
        except Exception as e:
            print(f"DEBUG: [SHELL] Critical Error: {e}")
