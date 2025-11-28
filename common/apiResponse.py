from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class CommonResponse(GenericModel, Generic[T]):
    errorCode : Optional[str] = None
    message : str
    result : Optional[T] = None
    
    @classmethod
    def success_response(cls, message:str, result : Optional[T] = None):
        return cls(errorCode=None, message=message, result = result)
    
    @classmethod
    def fail_response(cls, errorCode: str, message:str, result : Optional[T] = None):
        return cls(errorCode=errorCode, message=message, result = result)