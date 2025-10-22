"""
Base class for all function modules
"""

from typing import Any, Optional
from ..quik_service import QuikService

class BaseFunctions:
    """
    Base class for all QUIK function modules
    """
    def __init__(self, port: int, host: str = "127.0.0.1"):
        self.service = QuikService.create(port, host)


    async def call_function(self, function_name: str, *args, trans_id:int=0, timeout: Optional[float] = None) -> Any:
        return await self.service.call_function(function_name, *args, trans_id=trans_id, timeout=timeout)
