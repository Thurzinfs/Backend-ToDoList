from http import HTTPStatus
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

async def Integrit_error_handler(
    request: Request,
    exc: IntegrityError
):
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"detail" : "Database integrit error"}
    )