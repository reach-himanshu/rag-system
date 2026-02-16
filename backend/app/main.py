"""FastAPI application factory with lifespan management."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.config import settings
from app.core.exceptions import AuthenticationError, NotFoundError, RAGSystemError
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown."""
    # --- Startup ---
    setup_logging()
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)

    # Initialize Qdrant collection (lazy — services will call ensure_collection)
    logger.info("Qdrant configured at %s:%s", settings.qdrant_host, settings.qdrant_port)
    logger.info("PostgreSQL configured at %s:%s", settings.postgres_host, settings.postgres_port)

    yield

    # --- Shutdown ---
    logger.info("Shutting down %s", settings.app_name)
    from app.db.session import engine

    await engine.dispose()
    logger.info("Database connections closed")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="RAG System — Document Q&A and Text-to-SQL",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Exception Handlers ---
    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(RAGSystemError)
    async def rag_system_error_handler(request: Request, exc: RAGSystemError) -> JSONResponse:
        logger.error("Application error: %s — %s", exc.code, exc.message)
        return JSONResponse(
            status_code=500,
            content={"error": exc.code, "message": exc.message},
        )

    # --- Routes ---
    app.include_router(api_router)

    # --- Prometheus ---
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        excluded_handlers=["/health", "/metrics"],
    ).instrument(app).expose(app, endpoint="/metrics")

    return app


app = create_app()
