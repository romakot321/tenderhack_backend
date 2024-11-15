from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)
from contextlib import asynccontextmanager
import asyncio
import uuid
import uvicorn
import os

from app.services.llm import LLMService
from app.repositories.qs import QSRepository


def register_exception(application):
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        print(await request.body(), exc_str)
        content = {'status_code': 422, 'message': exc_str, 'data': None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


@asynccontextmanager
async def application_lifespan(app: FastAPI):
    if os.getenv("LLM_ENABLE", False):
        llm_service = LLMService(QSRepository())
        asyncio.create_task(llm_service.connect())
    yield


def init_web_application():
    application = FastAPI(
        openapi_url="/api/openapi.json",
        docs_url=None,
        redoc_url=None,
        lifespan=application_lifespan
    )

    register_exception(application)

    from app.routes.auction import router as auction_router

    application.include_router(auction_router)

    @application.get("/api/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@latest/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@latest/swagger-ui.css",
        )

    return application


def run() -> FastAPI:
    application = init_web_application()
    return application


fastapi_app = run()

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
