"""
Configuration settings for MSI-VPE Backend
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    # Application Info
    APP_NAME: str = "MSI-VPE Backend"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Multi-Modal Screenplay Intent to Visual Pre-Visualization Engine"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Database Settings (SQLite for capstone)
    DATABASE_URL: str = "sqlite:///./msi_vpe.db"
    DATABASE_ECHO: bool = False
    
    # AI Model Settings
    EMOTION_MODEL_PRIMARY: str = "SamLowe/roberta-base-go_emotions"
    EMOTION_MODEL_SECONDARY: str = "j-hartmann/emotion-english-distilroberta-base"
    EMOTION_MODEL_TERTIARY: str = "bhadresh-savani/distilbert-base-uncased-emotion"
    
    MODEL_CACHE_DIR: str = "./models_cache"
    
    # Inference Settings
    MAX_SEQUENCE_LENGTH: int = 512
    BATCH_SIZE: int = 8
    CONFIDENCE_THRESHOLD: float = 0.3
    
    # Knowledge Base Paths
    KNOWLEDGE_BASE_DIR: str = "./knowledge-base"
    EMOTION_COLOR_MAP_PATH: str = f"{KNOWLEDGE_BASE_DIR}/emotion_color_map.json"
    CINEMATOGRAPHY_RULES_PATH: str = f"{KNOWLEDGE_BASE_DIR}/cinematography_rules.json"
    LIGHTING_TECHNIQUES_PATH: str = f"{KNOWLEDGE_BASE_DIR}/lighting_techniques.json"
    CAMERA_ANGLE_PSYCHOLOGY_PATH: str = f"{KNOWLEDGE_BASE_DIR}/camera_angle_psychology.json"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: list = [".fountain", ".txt"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance
    ENABLE_CACHING: bool = True
    CACHE_TTL: int = 3600

    # Security / Auth
    API_KEY: Optional[str] = None
    RATE_LIMIT_PER_MINUTE: int = 120
    RATE_LIMIT_BURST: int = 60

    # Startup behavior
    WARM_MODELS_ON_STARTUP: bool = False

    # AI Text Generation tuning
    AI_TEXT_MAX_SUMMARY_LEN: int = 120
    AI_TEXT_MIN_SUMMARY_LEN: int = 40
    AI_TEXT_MAX_BULLET_LEN: int = 180
    
    # Feature Flags
    ENABLE_ENSEMBLE_MODELS: bool = True
    ENABLE_ADVANCED_VISUAL_MAPPING: bool = True
    ENABLE_SCENE_BEAT_DETECTION: bool = True
    
settings = Settings()
