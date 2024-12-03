from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

from app.models import OpeningHours
from app.service import convert_to_text_output

app = FastAPI(
    title="Opening Hours",
    description="The service renders JSON opening hours input into a human readable text format",
    version="0.0.1",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/", response_class=PlainTextResponse)
async def welcome() -> str:
    """
    Welcome to Opening Hours Service
    """
    return (
        "🗺️ Welcome to Opening Hours Service!\n📝 For more info please check /docs endpoint"
    )


@app.post("/v1/ConvertOpeningHours/", response_class=PlainTextResponse)
async def convert_opening_hours(opening_hours: OpeningHours) -> str:
    """
    Convert Opening Hours into human readable textual format
    """
    return convert_to_text_output(opening_hours)
