"""
Storage interfaces and implementations for persistent data
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import os


class IPersistentStorage(ABC):
    """
    Interface for persistent storage of transaction data
    """
    
    @abstractmethod
    def save(self, key: str, value: Any) -> None:
        """Save value by key"""
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        """Load value by key"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete value by key"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        pass


class InMemoryStorage(IPersistentStorage):
    """
    In-memory storage implementation
    """
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    def save(self, key: str, value: Any) -> None:
        """Save value by key"""
        self._data[key] = value
    
    def load(self, key: str) -> Optional[Any]:
        """Load value by key"""
        return self._data.get(key)
    
    def delete(self, key: str) -> None:
        """Delete value by key"""
        if key in self._data:
            del self._data[key]
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._data


class FileStorage(IPersistentStorage):
    """
    File-based storage implementation using JSON
    """
    
    def __init__(self, storage_dir: str = "quik_storage"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """Get file path for key"""
        safe_key = key.replace("/", "_").replace("\\", "_")
        return os.path.join(self.storage_dir, f"{safe_key}.json")
    
    def save(self, key: str, value: Any) -> None:
        """Save value by key"""
        file_path = self._get_file_path(key)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False, default=str)
    
    def load(self, key: str) -> Optional[Any]:
        """Load value by key"""
        file_path = self._get_file_path(key)
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def delete(self, key: str) -> None:
        """Delete value by key"""
        file_path = self._get_file_path(key)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        file_path = self._get_file_path(key)
        return os.path.exists(file_path)
