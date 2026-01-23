"""
LLM-powered text generation for MSI-VPE PDF reports.
Uses transformers (local) for summarization and generation to avoid API keys.
If models are unavailable, falls back to template-based text.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Any

from transformers import pipeline

from app.core.config import settings

logger = logging.getLogger(__name__)


class AITextService:
    def __init__(self):
        self._summarizer = None
        self._generator = None
        self._init_pipelines()

    def _init_pipelines(self):
        try:
            # Lightweight summarizer
            self._summarizer = pipeline(
                "summarization",
                model="t5-small",
                tokenizer="t5-small"
            )
            # Use the same model for light generation by framing prompts
            self._generator = self._summarizer
            logger.info("AITextService pipelines initialized (t5-small)")
        except Exception as e:
            logger.warning(f"AITextService pipeline init failed: {e}. Will use fallbacks.")
            self._summarizer = None
            self._generator = None

    def _safe_summarize(self, text: str, max_len: int | None = None, min_len: int | None = None) -> str:
        text = (text or "").strip()
        if not text:
            return ""
        max_len = max_len or settings.AI_TEXT_MAX_SUMMARY_LEN
        min_len = min_len or settings.AI_TEXT_MIN_SUMMARY_LEN
        # Cap lengths to avoid HF warnings for short inputs
        approx_tokens = max(8, len(text.split()) * 2)
        max_len = max(20, min(max_len, approx_tokens))
        min_len = max(5, min(min_len, max_len - 5))
        if not self._summarizer:
            return text if len(text) <= max_len else text[: max_len] + "…"
        try:
            # t5 expects prefixed task
            input_text = f"summarize: {text}"
            out = self._summarizer(
                input_text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )
            return (out[0]["summary_text"] or "").strip()
        except Exception as e:
            logger.warning(f"Summarization failed: {e}")
            return text if len(text) <= max_len else text[: max_len] + "…"

    def _safe_generate_bullets(self, prompt: str, count: int = 5) -> List[str]:
        prompt = (prompt or "").strip()
        if not prompt:
            return []
        if not self._generator:
            # Template fallback
            return [f"Shot suggestion {i+1}: {prompt[:48]}…" for i in range(count)]
        try:
            # For t5-small, reuse summarization with a directive and split sentences
            input_text = (
                "generate bullets: "
                + prompt
                + f"\nReturn {count} concise bullet points."
            )
            max_len = min(settings.AI_TEXT_MAX_BULLET_LEN, max(40, len(input_text.split()) * 2))
            min_len = max(15, min(30, max_len - 10))
            out = self._generator(input_text, max_length=max_len, min_length=min_len, do_sample=False)
            text = (out[0]["summary_text"] or "").strip()
            # Split heuristically into bullets
            bullets = [b.strip("- •\n ") for b in text.replace("\r", "").split("\n") if b.strip()]
            if len(bullets) < count:
                # Try periods as separators
                more = [s.strip() for s in text.split(".") if s.strip()]
                for s in more:
                    if s not in bullets:
                        bullets.append(s)
                    if len(bullets) >= count:
                        break
            return bullets[:count]
        except Exception as e:
            logger.warning(f"Bullet generation failed: {e}")
            return [f"Shot suggestion {i+1}: {prompt[:48]}…" for i in range(count)]

    def generate_executive_summary(self, analysis: Dict[str, Any], script_title: str) -> str:
        scenes = analysis.get("scenes") or []
        if not scenes and analysis:
            # single-scene shape
            scenes = [analysis]
        beats_count = sum(len(s.get("beats", [])) for s in scenes)
        emotions = []
        for s in scenes:
            for b in s.get("beats", []):
                arc = b.get("emotional_arc") or {}
                pe = arc.get("primary_emotion")
                if isinstance(pe, dict):
                    emotions.append(pe.get("emotion"))
                elif isinstance(pe, str):
                    emotions.append(pe)
        top_emotions = ", ".join(sorted({e for e in emotions if e})[:6])

        base = (
            f"Project '{script_title}' analyzed across {len(scenes)} scene(s) "
            f"and {beats_count} beat(s). Dominant emotions detected include: {top_emotions}. "
            "This report translates emotional arcs into actionable cinematography, lighting, and color guidance "
            "to support creative intent and on-set decision-making."
        )
        return self._safe_summarize(base, max_len=120, min_len=40)

    def generate_scene_overview(self, scene: Dict[str, Any], idx: int) -> str:
        loc = scene.get("scene_location") or "Unknown location"
        beats = scene.get("beats", [])
        emotions = []
        for b in beats:
            arc = b.get("emotional_arc") or {}
            pe = arc.get("primary_emotion")
            if isinstance(pe, dict):
                emotions.append(pe.get("emotion"))
            elif isinstance(pe, str):
                emotions.append(pe)
        emo_text = ", ".join(sorted({e for e in emotions if e})) or "mixed"
        raw = (
            f"Scene {idx} at {loc} comprises {len(beats)} beats with a tonal palette of {emo_text}. "
            "The pacing and emotional intensity evolve to guide coverage and lighting motifs."
        )
        return self._safe_summarize(raw, max_len=110, min_len=30)

    def generate_shot_list(self, scene: Dict[str, Any], count: int = 5) -> List[str]:
        # Build a compact prompt from beats' visual recommendations
        details = []
        for b in scene.get("beats", [])[:6]:  # cap context size
            arc = b.get("emotional_arc") or {}
            pe = arc.get("primary_emotion")
            pe_name = pe.get("emotion") if isinstance(pe, dict) else pe or "neutral"
            vr = b.get("visual_recommendations") or {}
            cam = vr.get("camera") or {}
            shots = ", ".join(cam.get("shot_types", [])[:3])
            moves = ", ".join(cam.get("movements", [])[:2])
            angs = ", ".join(cam.get("angles", [])[:2])
            details.append(
                f"{pe_name} — shots: {shots}; moves: {moves}; angles: {angs}"
            )
        prompt = (
            "Design a concise, practical shot list for a scene based on emotional beats and suggested coverage.\n"
            + "\n".join(details)
        )
        return self._safe_generate_bullets(prompt, count=count)


# Singleton access
_ai_text_service: AITextService | None = None


def get_ai_text_service() -> AITextService:
    global _ai_text_service
    if _ai_text_service is None:
        _ai_text_service = AITextService()
    return _ai_text_service
