from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(default=200, description="响应状态码")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": {}
            }
        }


def success_response(data: Optional[T] = None, message: str = "success") -> ApiResponse[T]:
    return ApiResponse(code=200, message=message, data=data)


def error_response(code: int = 500, message: str = "error", data: Optional[T] = None) -> ApiResponse[T]:
    return ApiResponse(code=code, message=message, data=data)
