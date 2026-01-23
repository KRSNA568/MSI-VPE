"""
Visual Mapping Engine
---------------------
Translates emotional intent into concrete cinematic parameters (camera, lighting, color).
Uses knowledge base JSONs and heuristic rules.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from app.core.config import settings
from app.schemas.sis_schema import (
    EmotionType, EmotionCategory, EmotionalArc, PowerDynamics, PacingMetadata,
    VisualSignals, ColorPalette, LightingParameters, CameraParameters,
    LightingDirection, LightingTechnique, CameraAngleVertical, CameraAngleHorizontal,
    CameraMovement, ShotSize, EmotionDetection
)

logger = logging.getLogger(__name__)

class VisualMapper:
    """
    Expert system for mapping emotional data to visual cinematography parameters.
    """

    def __init__(self):
        self.color_map: Dict[str, Any] = {}
        self.lighting_db: Dict[str, Any] = {}
        self.camera_rules: Dict[str, Any] = {}
        
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load JSON knowledge base files"""
        try:
            # Load Color Map
            with open(settings.EMOTION_COLOR_MAP_PATH, 'r') as f:
                data = json.load(f)
                # create lookup dict
                self.color_map = {e['emotion'].lower(): e for e in data['emotions']}

            # Load specialized DBs if needed (ignoring for now, using heuristics for some)
            # But we should load them if we want to return references/metadata
            
        except FileNotFoundError as e:
            logger.error(f"Knowledge base file not found: {e}")
            # Ensure basic fallback maps exist or raise critical error
            pass
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing knowledge base: {e}")

    def map_to_visuals(
        self, 
        emotional_arc: EmotionalArc, 
        power_dynamics: Optional[PowerDynamics] = None,
        pacing: Optional[PacingMetadata] = None
    ) -> VisualSignals:
        """
        Main entry point: Convert emotional data into visual recommendations.
        """
        primary_emotion = emotional_arc.primary_emotion.emotion
        intensity = emotional_arc.primary_emotion.intensity

        # 1. Generate Colors
        colors = self._get_color_palette(primary_emotion, intensity)

        # 2. Generate Lighting
        lighting = self._get_lighting(primary_emotion, intensity)

        # 3. Generate Camera
        camera = self._get_camera(emotional_arc, power_dynamics, pacing)

        # 4. Construct Reasoning
        reasoning = self._generate_reasoning(emotional_arc, colors, lighting, camera)

        return VisualSignals(
            colors=colors,
            lighting=lighting,
            camera=camera,
            reasoning=reasoning,
            confidence_score=emotional_arc.primary_emotion.confidence, # simplified
            film_references=[], # Could populate from DB
            alternative_options=None
        )

    def _get_color_palette(self, emotion: EmotionType, intensity: int) -> ColorPalette:
        """Get color palette for emotion"""
        emotion_str = emotion.value.lower()
        
        # Default fallback
        default_palette = {
            "primary": ["#808080"], "secondary": ["#A9A9A9"], "accent": ["#D3D3D3"]
        }
        
        # Lookup in knowledge base
        kb_data = self.color_map.get(emotion_str, {})
        
        # Handle flat list or dict structure from knowledge base
        raw_palette = kb_data.get("palette", [])
        if raw_palette and isinstance(raw_palette, list):
             # Distribute flat list if available
             c_prim = [raw_palette[0]] if len(raw_palette) > 0 else ["#808080"]
             c_sec = [raw_palette[1]] if len(raw_palette) > 1 else ["#A9A9A9"]
             c_acc = raw_palette[2:] if len(raw_palette) > 2 else ["#D3D3D3"]
             
             palette = {"primary": c_prim, "secondary": c_sec, "accent": c_acc}
        else:
             palette = kb_data.get("color_palette", default_palette)
        
        # Determine saturation/brightness based on intensity
        # High intensity = higher saturation usually (except sadness)
        saturation = intensity
        brightness = intensity
        
        if emotion in [EmotionType.SADNESS, EmotionType.DESPAIR]:
             # Invert for sad emotions (high intensity sadness = low brightness/sat)
             saturation = max(10, 100 - intensity)
             brightness = max(10, 100 - intensity)

        return ColorPalette(
            primary_colors=palette["primary"],
            secondary_colors=palette["secondary"],
            accent_colors=palette["accent"],
            saturation=saturation,
            brightness=brightness,
            harmony_type="analogous" # Simplified default
        )

    def _get_lighting(self, emotion: EmotionType, intensity: int) -> LightingParameters:
        """Derive lighting parameters from emotion"""
        
        # Heuristic Rule Engine
        # Default: Neutral
        params = {
            "quality": 50, # medium
            "temperature_kelvin": 5600, # Daylight
            "direction": LightingDirection.SIDE,
            "intensity": "medium",
            "contrast_ratio": "4:1",
            "shadow_type": "defined",
            "technique": LightingTechnique.LOOP
        }

        e = emotion
        
        # 1. Light Quality (Hard vs Soft)
        if e in [EmotionType.ANGER, EmotionType.FEAR, EmotionType.TENSION, EmotionType.DREAD]:
            params["quality"] = min(intensity + 30, 100) # Hard
            params["shadow_type"] = "harsh"
        elif e in [EmotionType.JOY, EmotionType.PASSION, EmotionType.EUPHORIA]:
            params["quality"] = max(100 - intensity, 0) # Soft
            params["shadow_type"] = "diffused"

        # 2. Temperature
        if e in [EmotionType.SADNESS, EmotionType.LONELINESS, EmotionType.DESPAIR, EmotionType.FEAR]:
            params["temperature_kelvin"] = 6500 + (intensity * 20) # Cool
        elif e in [EmotionType.JOY, EmotionType.NOSTALGIA, EmotionType.PASSION, EmotionType.HOPE]:
            # Removed LOVE
            params["temperature_kelvin"] = 3200 - (intensity * 10) # Warm
            
        # 3. Technique & Contrast
        if e in [EmotionType.FEAR, EmotionType.DREAD, EmotionType.BETRAYAL]:
            params["technique"] = LightingTechnique.CHIAROSCURO
            params["contrast_ratio"] = "16:1"
            params["intensity"] = "low"
        elif e in [EmotionType.ANGER, EmotionType.TENSION]:
            params["technique"] = LightingTechnique.SPLIT
            params["contrast_ratio"] = "8:1"
        elif e in [EmotionType.JOY, EmotionType.HOPE]:
            params["technique"] = LightingTechnique.HIGH_KEY
            params["contrast_ratio"] = "2:1"
            params["intensity"] = "high"
        elif e == EmotionType.SADNESS:
            params["technique"] = LightingTechnique.LOW_KEY
            params["contrast_ratio"] = "8:1"
            params["intensity"] = "low"

        return LightingParameters(**params)

    def _get_camera(
        self, 
        arc: EmotionalArc, 
        power: Optional[PowerDynamics], 
        pacing: Optional[PacingMetadata]
    ) -> CameraParameters:
        """Derive camera parameters"""
        e = arc.primary_emotion.emotion
        intensity = arc.primary_emotion.intensity
        
        params = {
            "vertical_angle": CameraAngleVertical.EYE_LEVEL,
            "horizontal_angle": CameraAngleHorizontal.THREE_QUARTER,
            "movement": CameraMovement.STATIC,
            "shot_size": ShotSize.MS, # Using enum from Schema
            "focal_length_mm": 50,
            "depth_of_field": "medium"
        }

        # 1. Vertical Angle
        # Default based on emotion
        if e == EmotionType.FEAR:
            params["vertical_angle"] = CameraAngleVertical.HIGH # Vulnerability
        elif e == EmotionType.ANGER or e == EmotionType.TRIUMPH:
            params["vertical_angle"] = CameraAngleVertical.LOW # Dominance
            
        # Power Dynamics (Override)
        if power:
            if power.power_balance == "dominant":
                params["vertical_angle"] = CameraAngleVertical.LOW
            elif power.power_balance == "submissive":
                params["vertical_angle"] = CameraAngleVertical.HIGH

        # 2. Movement (Pacing)
        if pacing:
            if pacing.rhythm in ["fast", "very_fast"]:
                params["movement"] = CameraMovement.HANDHELD
                params["movement_speed"] = "fast"
            elif pacing.rhythm in ["slow", "very_slow"]:
                params["movement"] = CameraMovement.DOLLY_IN
                params["movement_speed"] = "slow"
        
        # 3. Focal Length & DOF
        if e in [EmotionType.LONELINESS, EmotionType.DESPAIR]:
            params["shot_size"] = ShotSize.LS
            params["focal_length_mm"] = 35
            params["depth_of_field"] = "deep"
        elif e in [EmotionType.PASSION, EmotionType.EUPHORIA]:
            params["shot_size"] = ShotSize.CU
            params["focal_length_mm"] = 85
            params["depth_of_field"] = "shallow"
        elif e in [EmotionType.ANXIETY, EmotionType.CONFUSION]:
            params["movement"] = CameraMovement.HANDHELD
            params["focal_length_mm"] = 100 # Compression/Claustrophobia

        return CameraParameters(**params)

    def _generate_reasoning(self, arc, colors, lighting, camera):
        """Generate text explanation for choices"""
        e_name = arc.primary_emotion.emotion.value
        return (
            f"Based on the primary emotion of {e_name} (intensity: {arc.primary_emotion.intensity}%), "
            f"we recommend a {lighting.technique.value} lighting setup to enhance the mood. "
            f"The color palette uses {colors.primary_colors[0]} to evoke the psychological state. "
            f"Camera is positioned {camera.vertical_angle.value} to reflect character power dynamics."
        )
