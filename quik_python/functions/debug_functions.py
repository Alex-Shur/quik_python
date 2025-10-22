"""
Debug functions for QUIK interaction
"""

from typing import Any
from .base_functions import BaseFunctions


class DebugFunctions(BaseFunctions):
    """
    Debug functions for QUIK interaction
    """

    async def ping(self) -> str:
        """
        Ping QUIK to test connection

        Returns:
            Response from QUIK
        """
        result = await self.call_function("ping", "Ping");
        return str(result['data'])


    async def echo(self, message: Any) -> Any:
        """
        Echo message back from QUIK

        Args:
            message: Message to echo

        Returns:
            The same message from QUIK
        """
        return await self.call_function("echo", message)


    async def log_message(self, message: str, level: str = "INFO") -> None:
        """
        Log message in QUIK

        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        await self.call_function("logMessage", message, level)


    async def divide_string_by_zero(self) -> str:
        """
        This method returns LuaException and demonstrates how Lua errors are caught
        """
        result = await self.call_function("divide_string_by_zero")
        return result['data'] if result else ''


    async def is_quik(self) -> bool:
        """
        Check if running inside Quik
        """
        result = await self.call_function("is_quik")
        return bool(result['data']) if result else False


    async def get_version(self) -> str:
        """
        Get QUIK version

        Returns:
            QUIK version string
        """
        result = await self.call_function("getVersion")
        return result['data'] if result else ''
