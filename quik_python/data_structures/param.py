"""
Param class - параметры инструмента
"""

from dataclasses import dataclass
from typing import Optional
import json
from .base import BaseDataStructure


@dataclass
class Param(BaseDataStructure):
    """
    Параметры инструмента - код бумаги и код класса
    
    Простой класс для передачи основных идентификаторов финансового инструмента.
    Используется в различных запросах к QUIK API.
    """
    
    # Код бумаги
    sec_code: Optional[str] = None
    
    # Код класса
    class_code: Optional[str] = None
