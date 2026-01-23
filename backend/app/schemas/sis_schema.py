"""
Scene Intent Schema (SIS) - Pydantic Models
Complete data validation and serialization for MSI-VPE system

Version: 1.0
Date: January 23, 2026
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from enum import Enum


class SISBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        protected_namespaces=()
    )


# ============================================================================
# ENUMS - Emotion and Visual Parameter Types
# ============================================================================

class EmotionCategory(str, Enum):
    """Emotion classification categories"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


class EmotionType(str, Enum):
    """Complete emotion taxonomy (20+ emotions)"""
    # Primary
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    
    # Secondary
    TENSION = "tension"
    MELANCHOLY = "melancholy"
    EUPHORIA = "euphoria"
    ANXIETY = "anxiety"
    NOSTALGIA = "nostalgia"
    LONELINESS = "loneliness"
    
    # Tertiary
    HOPE = "hope"
    DESPAIR = "despair"
    TRIUMPH = "triumph"
    BETRAYAL = "betrayal"
    CONFUSION = "confusion"
    SERENITY = "serenity"
    DREAD = "dread"
    PASSION = "passion"


class CameraAngleVertical(str, Enum):
    """Vertical camera angles"""
    EXTREME_LOW = "extreme_low"
    LOW = "low"
    EYE_LEVEL = "eye_level"
    HIGH = "high"
    EXTREME_HIGH = "extreme_high"
    OVERHEAD = "overhead"
    WORMS_EYE = "worms_eye"
    DUTCH = "dutch"


class CameraAngleHorizontal(str, Enum):
    """Horizontal camera angles"""
    FRONTAL = "frontal"
    THREE_QUARTER = "three_quarter"
    PROFILE = "profile"
    OVER_SHOULDER = "over_shoulder"
    POV = "pov"


class CameraMovement(str, Enum):
    """Camera movement types"""
    STATIC = "static"
    PAN = "pan"
    TILT = "tilt"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    TRACK = "track"
    HANDHELD = "handheld"
    STEADICAM = "steadicam"
    CRANE_UP = "crane_up"
    CRANE_DOWN = "crane_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    WHIP_PAN = "whip_pan"
    CIRCLE = "circle"


class ShotSize(str, Enum):
    """Shot composition sizes"""
    ECU = "extreme_closeup"
    CU = "closeup"
    MCU = "medium_closeup"
    MS = "medium_shot"
    MLS = "medium_long_shot"
    LS = "long_shot"
    ELS = "extreme_long_shot"
    TWO_SHOT = "two_shot"
    THREE_SHOT = "three_shot"
    OTS = "over_the_shoulder"


class LightingDirection(str, Enum):
    """Lighting direction options"""
    FRONT = "front"
    THREE_QUARTER = "three_quarter"
    SIDE = "side"
    RIM_BACK = "rim_back"
    UNDER = "under"
    OVERHEAD = "overhead"
    WINDOW = "window"
    MOTIVATED = "motivated"


class LightingTechnique(str, Enum):
    """Professional lighting techniques"""
    REMBRANDT = "rembrandt"
    BUTTERFLY = "butterfly"
    SPLIT = "split"
    LOOP = "loop"
    BROAD = "broad"
    SHORT = "short"
    CHIAROSCURO = "chiaroscuro"
    SILHOUETTE = "silhouette"
    HIGH_KEY = "high_key"
    LOW_KEY = "low_key"


# ============================================================================
# NESTED MODELS - Emotional Analysis
# ============================================================================

class EmotionDetection(SISBaseModel):
    """Individual emotion detection result"""
    emotion: EmotionType = Field(..., description="Detected emotion type")
    category: EmotionCategory = Field(..., description="Emotion category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    intensity: int = Field(..., ge=0, le=100, description="Emotional intensity (0-100)")
    
    @field_validator('confidence')
    @classmethod
    def round_confidence(cls, v: float) -> float:
        """Round confidence to 2 decimal places"""
        return round(v, 2)


class EmotionalArc(SISBaseModel):
    """Complete emotional profile for a beat/scene"""
    scene_id: Optional[str] = Field(None, description="Scene identifier")
    segment_id: Optional[str] = Field(None, description="Segment identifier")
    primary_emotion: EmotionDetection = Field(..., description="Dominant emotion")
    secondary_emotions: List[EmotionDetection] = Field(
        default_factory=list, 
        description="Additional detected emotions"
    )
    mixed_emotions: bool = Field(
        default=False, 
        description="Whether multiple emotions are present"
    )
    emotional_shift: Optional[bool] = Field(
        None, 
        description="Whether emotion changes within this beat"
    )
    overall_intensity: int = Field(..., ge=0, le=100, description="Overall emotional intensity")


class PowerDynamics(SISBaseModel):
    """Character power relationships"""
    dominant_character: Optional[str] = Field(None, description="Character with power in scene")
    power_balance: Literal["dominant", "submissive", "equal", "shifting"] = Field(
        ..., 
        description="Overall power balance"
    )
    power_score: int = Field(..., ge=0, le=100, description="Power intensity (0=weak, 100=strong)")


class PacingMetadata(SISBaseModel):
    """Scene pacing information"""
    bpm: int = Field(..., ge=20, le=180, description="Suggested editing BPM")
    rhythm: Literal["very_slow", "slow", "medium", "fast", "very_fast"] = Field(
        ..., 
        description="Overall pacing rhythm"
    )
    sentence_avg_length: float = Field(..., description="Average sentence length")
    verb_density: float = Field(..., ge=0.0, le=1.0, description="Ratio of action verbs")


# ============================================================================
# NESTED MODELS - Visual Recommendations
# ============================================================================

class ColorPalette(SISBaseModel):
    """Color scheme recommendations"""
    primary_colors: List[str] = Field(
        ..., 
        min_length=1, 
        max_length=5,
        description="Primary colors (hex codes)"
    )
    secondary_colors: List[str] = Field(
        default_factory=list,
        max_length=5,
        description="Secondary colors (hex codes)"
    )
    accent_colors: List[str] = Field(
        default_factory=list,
        max_length=3,
        description="Accent colors (hex codes)"
    )
    saturation: int = Field(..., ge=0, le=100, description="Saturation level")
    brightness: int = Field(..., ge=0, le=100, description="Brightness level")
    harmony_type: Optional[Literal["complementary", "analogous", "triadic", "monochromatic"]] = Field(
        None,
        description="Color harmony principle"
    )
    
    @field_validator('primary_colors', 'secondary_colors', 'accent_colors')
    @classmethod
    def validate_hex_colors(cls, v: List[str]) -> List[str]:
        """Validate hex color codes"""
        for color in v:
            if not color.startswith('#') or len(color) not in [4, 7]:
                raise ValueError(f"Invalid hex color: {color}")
        return v


class LightingParameters(SISBaseModel):
    """Comprehensive lighting setup"""
    quality: int = Field(..., ge=0, le=100, description="Hardness (0=soft, 100=hard)")
    temperature_kelvin: int = Field(
        ..., 
        ge=1800, 
        le=10000, 
        description="Color temperature in Kelvin"
    )
    direction: LightingDirection = Field(..., description="Primary light direction")
    intensity: Literal["very_low", "low", "medium", "high", "very_high"] = Field(
        ...,
        description="Light intensity level"
    )
    contrast_ratio: str = Field(..., description="Key to fill ratio (e.g., '8:1')")
    shadow_type: Literal["diffused", "defined", "harsh", "none"] = Field(
        ...,
        description="Shadow characteristics"
    )
    technique: Optional[LightingTechnique] = Field(
        None,
        description="Specific lighting technique"
    )
    motivated_source: Optional[str] = Field(
        None,
        description="Practical light source (window, lamp, fire, etc.)"
    )
    modifiers: List[str] = Field(
        default_factory=list,
        description="Equipment: softbox, umbrella, flags, gels, etc."
    )
    
    @field_validator('temperature_kelvin')
    @classmethod
    def round_temperature(cls, v: int) -> int:
        """Round temperature to nearest 100K"""
        return round(v, -2)


class CameraParameters(SISBaseModel):
    """Complete camera setup"""
    vertical_angle: CameraAngleVertical = Field(..., description="Vertical angle")
    horizontal_angle: CameraAngleHorizontal = Field(..., description="Horizontal angle")
    angle_degrees: Optional[int] = Field(
        None, 
        ge=-90, 
        le=90, 
        description="Angle in degrees from eye-level"
    )
    movement: CameraMovement = Field(..., description="Camera movement type")
    movement_speed: Optional[Literal["very_slow", "slow", "medium", "fast", "very_fast"]] = Field(
        None,
        description="Speed of movement"
    )
    shot_size: ShotSize = Field(..., description="Shot composition size")
    focal_length_mm: int = Field(
        ..., 
        ge=8, 
        le=800, 
        description="Lens focal length in mm"
    )
    aperture: Optional[str] = Field(
        None,
        description="Aperture f-stop (e.g., 'f/2.8')"
    )
    depth_of_field: Literal["shallow", "medium", "deep"] = Field(
        ...,
        description="Depth of field characteristics"
    )


class VisualSignals(SISBaseModel):
    """Complete visual recommendation package"""
    colors: ColorPalette = Field(..., description="Color palette")
    lighting: LightingParameters = Field(..., description="Lighting setup")
    camera: CameraParameters = Field(..., description="Camera configuration")
    reasoning: str = Field(..., description="Explanation of visual choices")
    confidence_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Overall confidence in recommendations"
    )
    film_references: List[str] = Field(
        default_factory=list,
        description="Famous film examples with similar visual approach"
    )
    alternative_options: Optional[Dict[str, Any]] = Field(
        None,
        description="Alternative visual approaches"
    )


# ============================================================================
# BEAT & SCENE MODELS
# ============================================================================

class Beat(SISBaseModel):
    """Individual beat within a scene (sub-scene unit)"""
    beat_id: str = Field(..., description="Unique beat identifier")
    beat_number: int = Field(..., ge=1, description="Sequential beat number in scene")
    timestamp_start: float = Field(..., ge=0.0, description="Start time in seconds")
    timestamp_end: float = Field(..., ge=0.0, description="End time in seconds")
    
    # Content
    dialogue: List[str] = Field(default_factory=list, description="Lines of dialogue")
    action: List[str] = Field(default_factory=list, description="Action descriptions")
    characters: List[str] = Field(default_factory=list, description="Characters present")
    
    # Analysis
    emotional_arc: EmotionalArc = Field(..., description="Emotional analysis")
    power_dynamics: Optional[PowerDynamics] = Field(None, description="Power relationships")
    pacing: PacingMetadata = Field(..., description="Pacing information")
    
    # Visual recommendations
    visual_signals: VisualSignals = Field(..., description="Visual recommendations")
    technical_tags: List[str] = Field(
        default_factory=list,
        description="Technical keywords for downstream tools"
    )
    
    @field_validator('timestamp_end')
    @classmethod
    def validate_timestamp_order(cls, v: float, info) -> float:
        """Ensure end timestamp is after start"""
        if 'timestamp_start' in info.data and v <= info.data['timestamp_start']:
            raise ValueError("timestamp_end must be greater than timestamp_start")
        return v


class ScriptMetadata(SISBaseModel):
    """Screenplay metadata"""
    title: Optional[str] = Field(None, description="Script title")
    scene_number: str = Field(..., description="Scene number/ID")
    location: str = Field(..., description="Scene location")
    time_of_day: str = Field(..., description="INT/EXT and time")
    characters_present: List[str] = Field(
        default_factory=list,
        description="All characters in scene"
    )
    page_number: Optional[int] = Field(None, description="Script page number")
    estimated_duration_seconds: Optional[float] = Field(
        None,
        description="Estimated scene duration"
    )


# ============================================================================
# TOP-LEVEL SCENE INTENT SCHEMA
# ============================================================================

class SceneIntentSchema(SISBaseModel):
    """
    Complete Scene Intent Schema (SIS) - Top-level output
    
    This is the primary data structure output by MSI-VPE system.
    Contains all emotional analysis and visual recommendations for a scene.
    """
    
    # Schema metadata
    schema_version: str = Field(default="1.0", description="SIS schema version")
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of analysis"
    )
    analysis_id: str = Field(..., description="Unique analysis identifier")
    
    # Script information
    script_metadata: ScriptMetadata = Field(..., description="Scene metadata")
    
    # Beats (sub-scene analysis)
    beats: List[Beat] = Field(
        ..., 
        min_length=1, 
        description="Scene broken into beats"
    )
    
    # Scene-level aggregates
    scene_dominant_emotion: EmotionType = Field(
        ...,
        description="Overall dominant emotion for entire scene"
    )
    scene_emotional_range: List[EmotionType] = Field(
        ...,
        description="All emotions present in scene"
    )
    scene_intensity_average: int = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Average emotional intensity"
    )
    
    # Scene-level visual recommendations
    scene_visual_summary: VisualSignals = Field(
        ...,
        description="Overall visual approach for scene"
    )
    
    # Analysis metadata
    processing_time_seconds: Optional[float] = Field(
        None,
        description="Time taken to analyze scene"
    )
    model_versions: Dict[str, str] = Field(
        default_factory=dict,
        description="AI model versions used"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="Analysis warnings or caveats"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "schema_version": "1.0",
                "analysis_id": "scene_001_20260123",
                "script_metadata": {
                    "scene_number": "12",
                    "location": "SARAH'S APARTMENT",
                    "time_of_day": "INT. NIGHT",
                    "characters_present": ["SARAH", "JOHN"]
                },
                "scene_dominant_emotion": "betrayal",
                "scene_intensity_average": 85,
                "beats": [
                    {
                        "beat_id": "beat_001",
                        "beat_number": 1,
                        "timestamp_start": 0.0,
                        "timestamp_end": 15.5,
                        "emotional_arc": {
                            "primary_emotion": {
                                "emotion": "betrayal",
                                "category": "tertiary",
                                "confidence": 0.89,
                                "intensity": 85
                            },
                            "overall_intensity": 85
                        },
                        "visual_signals": {
                            "colors": {
                                "primary_colors": ["#991B1B", "#6B21A8"],
                                "saturation": 75,
                                "brightness": 45
                            },
                            "lighting": {
                                "quality": 90,
                                "temperature_kelvin": 6500,
                                "direction": "side",
                                "intensity": "medium",
                                "contrast_ratio": "12:1",
                                "shadow_type": "harsh",
                                "technique": "split"
                            },
                            "camera": {
                                "vertical_angle": "high",
                                "horizontal_angle": "frontal",
                                "movement": "dolly_out",
                                "shot_size": "closeup",
                                "focal_length_mm": 85,
                                "depth_of_field": "shallow"
                            },
                            "reasoning": "Betrayal requires harsh split lighting...",
                            "confidence_score": 0.87
                        }
                    }
                ]
            }
        }
    )


# ============================================================================
# INPUT/OUTPUT MODELS
# ============================================================================

class ScriptInput(SISBaseModel):
    """Input model for script upload"""
    script_text: str = Field(..., min_length=10, description="Fountain format screenplay text")
    title: Optional[str] = Field(None, description="Script title")
    analyze_full_script: bool = Field(
        default=False,
        description="Analyze entire script or single scene"
    )
    style_profile: Optional[str] = Field(
        None,
        description="Visual style preset (e.g., 'noir', 'blockbuster')"
    )


class AnalysisRequest(SISBaseModel):
    """Request for scene analysis"""
    job_id: str = Field(..., description="Unique job identifier")
    script_text: str = Field(..., description="Scene text to analyze")
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Analysis options"
    )


class AnalysisResponse(SISBaseModel):
    """Response from analysis endpoint"""
    job_id: str = Field(..., description="Job identifier")
    status: Literal["pending", "processing", "completed", "failed"] = Field(
        ...,
        description="Analysis status"
    )
    result: Optional[SceneIntentSchema] = Field(None, description="Analysis result")
    error: Optional[str] = Field(None, description="Error message if failed")
    progress: Optional[int] = Field(None, ge=0, le=100, description="Progress percentage")


class HealthCheck(SISBaseModel):
    """API health check response"""
    status: Literal["healthy", "unhealthy"] = "healthy"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
    models_loaded: bool = False


# ============================================================================
# EXPORT MODELS
# ============================================================================

class ExportFormat(str, Enum):
    """Supported export formats"""
    JSON = "json"
    XML = "xml"
    PDF = "pdf"
    USD = "usd"  # Future: Universal Scene Description


class ExportRequest(SISBaseModel):
    """Request for exporting analysis"""
    job_id: str = Field(..., description="Job to export")
    format: ExportFormat = Field(default=ExportFormat.JSON, description="Export format")
    include_reasoning: bool = Field(default=True, description="Include explanations")
    include_alternatives: bool = Field(default=False, description="Include alternative options")
