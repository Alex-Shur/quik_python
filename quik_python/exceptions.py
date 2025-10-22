"""
Exception classes for QuikPython
"""


class LuaException(Exception):
    """
    Exception raised when Lua script returns an error
    """
    
    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code is not None:
            return f"LuaException (code {self.error_code}): {self.message}"
        return f"LuaException: {self.message}"


class QuikException(Exception):
    """
    Base exception for QuikPython related errors
    """
    pass


class ConnectionException(QuikException):
    """
    Exception raised when connection to QUIK fails
    """
    pass


class TimeoutException(QuikException):
    """
    Exception raised when operation times out
    """
    pass
