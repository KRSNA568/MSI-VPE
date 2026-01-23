"""Lightweight API key auth dependency."""
from typing import Optional
from fastapi import Header, HTTPException, status, Depends
from app.core.config import settings

async def require_api_key(x_api_key: Optional[str] = Header(default=None)):
    if not settings.API_KEY:
        return None  # auth disabled
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return x_api_key

def secure_dependency():
    return Depends(require_api_key)
