"""
MSI-VPE FastAPI Application Entry Point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Deque
from collections import defaultdict, deque

from app.core.config import settings
from app.core.database import engine, Base
from app.core.knowledge_base import validate_knowledge_base
from app.services.analysis_service import AnalysisService
from app.models.job import AnalysisJob # Import models to register them

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Simple in-memory rate limiter (per-process, best-effort)
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_per_minute: int, burst: int):
        super().__init__(app)
        self.max_per_minute = max_per_minute
        self.burst = burst
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        # Skip for docs/health
        path = request.url.path
        if path.startswith("/docs") or path.startswith("/openapi") or path.startswith("/health"):
            return await call_next(request)

        now = time.time()
        window_start = now - 60
        client_ip = request.client.host if request.client else "anonymous"
        q = self.requests[client_ip]
        # drop old
        while q and q[0] < window_start:
            q.popleft()

        if len(q) >= max(self.max_per_minute, self.burst):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please retry later."}
            )

        q.append(now)
        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Knowledge base directory: {settings.KNOWLEDGE_BASE_DIR}")

    # Initialize Database
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized.")

    # Validate knowledge base files
    validate_knowledge_base()

    # Optional: warm AI models to avoid cold start
    if settings.WARM_MODELS_ON_STARTUP:
        try:
            service = AnalysisService()
            service.emotion_detector.analyze_text("Warm up")
            logger.info("AI models warmed up")
        except Exception as exc:
            logger.warning(f"AI warm-up failed: {exc}")

    yield

    logger.info(f"Shutting down {settings.APP_NAME}")
    logger.info("Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    RateLimitMiddleware,
    max_per_minute=settings.RATE_LIMIT_PER_MINUTE,
    burst=settings.RATE_LIMIT_BURST,
)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "status": "running",
        "docs": "/docs",
        "api": settings.API_V1_PREFIX,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
    }


# API v1 routes will be registered here
from app.api.endpoints import analysis
app.include_router(analysis.router, prefix=settings.API_V1_PREFIX, tags=["analysis"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
