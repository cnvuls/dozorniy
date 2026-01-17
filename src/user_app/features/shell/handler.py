import asyncio

from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler

from .request import ShellRequest
from .responses import ShellResponse


@FeatureRegistry.register(command_key="shell", response_model=ShellResponse)
class ShellHandler(ResponseHandler[ShellResponse]):
    async def handle(self, command: ShellResponse):

        process = await asyncio.create_subprocess_shell(
            command.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        output = stdout.decode(errors="replace").strip()
        error = stderr.decode(errors="replace").strip()
        result_text = output if output else error

        response = ShellRequest(
            event_id=command.event_id or "unknown",
            type="shell_result",
            stdout=result_text,
            stderr=error,
            exit_code=process.returncode or 0,
        )
        print(response)
        await self.bus.publish(response)
