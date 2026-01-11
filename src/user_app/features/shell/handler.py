import asyncio

from core.dispatcher import RequestDispatcher
from core.responses.base import ResponseHandler
from features.shell.request import ShellRequest
from features.shell.responses import ShellCommand


class ShellHandler(ResponseHandler[ShellCommand]):
    def __init__(self, dispatcher: RequestDispatcher):
        self.dispatcher = dispatcher

    async def handle(self, command: ShellCommand):

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
            event_id=command.event_id,
            type="shell_result",
            stdout=result_text,
            stderr=error,
            exit_code=process.returncode or 0,
        )

        await self.dispatcher.send(response)
