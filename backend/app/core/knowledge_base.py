"""
Knowledge base validation utilities.
Ensures required JSON files exist and are well-formed at startup.
"""
import json
from pathlib import Path
import logging
from typing import Dict

from app.core.config import settings

logger = logging.getLogger(__name__)

REQUIRED_FILES: Dict[str, str] = {
    "emotion_color_map": settings.EMOTION_COLOR_MAP_PATH,
    "cinematography_rules": settings.CINEMATOGRAPHY_RULES_PATH,
    "lighting_techniques": settings.LIGHTING_TECHNIQUES_PATH,
    "camera_angle_psychology": settings.CAMERA_ANGLE_PSYCHOLOGY_PATH,
}


def validate_knowledge_base() -> None:
    """Validate that knowledge base files exist and contain valid JSON."""
    missing = []
    for name, path_str in REQUIRED_FILES.items():
        path = Path(path_str)
        if not path.exists():
            missing.append((name, path))
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                json.load(f)
        except Exception as exc:
            logger.warning(f"Knowledge base file '{name}' at {path} failed to load: {exc}")
    if missing:
        missing_list = ", ".join(f"{n} ({p})" for n, p in missing)
        logger.warning(f"Missing knowledge base files: {missing_list}")
    else:
        logger.info(f"Knowledge base validated ({len(REQUIRED_FILES)} files)")
