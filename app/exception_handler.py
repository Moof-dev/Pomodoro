from fastapi import Request
from fastapi.responses import JSONResponse
from app.exception import BaseAppException

async def common_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail},
    )