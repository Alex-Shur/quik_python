"""
Miscellaneous classes and enums for QuikPython
"""

from enum import Enum
from typing import Any, Dict


class NotificationType(Enum):
    """
    Notification types for QUIK events
    """
    INFO = 1

    WARNING = 2

    ERROR = 3

    #DEBUG = 4


class Message:
    """
    Message class for inter-process communication
    """

    def __init__(self, data: Dict[str, Any] = None):
        self.data = data or {}

    def to_dict(self) -> Dict[str, Any]:
        return self.data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(data)
