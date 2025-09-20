from typing import Generic, TypeVar, Optional
from core.error_list import ErrorCode

T = TypeVar("T")

class Result(Generic[T]):
    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None, code: Optional[ErrorCode] = None):
        self.success = success
        self.data = data
        self.error = error
        self.code = code

    @classmethod
    def ok(cls, data: T):
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str, code: ErrorCode):
        return cls(success=False, error=error, code=code)
