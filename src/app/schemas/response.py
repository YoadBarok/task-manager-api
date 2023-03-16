from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')


class Response(GenericModel, Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T]