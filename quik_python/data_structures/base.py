"""
Base classes for data structures
"""

from dataclasses import dataclass, fields
from typing import Dict, Any, Optional
import json


@dataclass
class BaseDataStructure:
    """
    Base class for all data structures
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {k: v for k, v in self.__dict__.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseDataStructure':
        """Create instance from dictionary"""
        # Filter only fields that exist in the dataclass
        if hasattr(cls, '__dataclass_fields__'):
            field_names = {field.name for field in fields(cls)}
            filtered_data = {k: v for k, v in data.items() if k in field_names}
        else:
            filtered_data = data
        return cls(**filtered_data)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)
