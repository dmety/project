from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.response import error_response


class BusinessException(Exception):
    def __init__(self, code: int = 400, message: str = "业务错误"):
        self.code = code
        self.message = message


async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=200,
        content=error_response(code=exc.code, message=exc.message).model_dump()
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(code=exc.status_code, message=exc.detail).model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response(code=500, message="服务器内部错误").model_dump()
    )
