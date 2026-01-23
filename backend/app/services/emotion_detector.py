"""
Emotion Detection Service
-------------------------
Uses Hugging Face Transformers to detect emotions in text and map them to the 
MSI-VPE Scene Intent Schema (SIS) taxonomy.
"""

from transformers import pipeline
from typing import List, Dict, Optional, Tuple
import logging
from app.core.config import settings
from app.schemas.sis_schema import (
    EmotionType, 
    EmotionCategory, 
    EmotionDetection, 
    EmotionalArc
)

logger = logging.getLogger(__name__)

class EmotionDetector:
    """
    Service for detecting emotions in text using ensemble models.
    """
    
    # Mapping from GoEmotions labels to SIS EmotionType
    # GoEmotions has 27 labels + neutral
    GOEMOTIONS_MAP = {
        "admiration": EmotionType.SERENITY,  # or TRIUMPH/HOPE depending on context
        "amusement": EmotionType.JOY,
        "anger": EmotionType.ANGER,
        "annoyance": EmotionType.ANGER,       # Lower intensity
        "approval": EmotionType.SERENITY,     # or TRUST (if available) -> Serenity/Hope
        "caring": EmotionType.SERENITY,       # Empathy/Love -> Serenity
        "confusion": EmotionType.CONFUSION,
        "curiosity": EmotionType.TENSION,     # Interest/unknown -> Tension
        "desire": EmotionType.PASSION,
        "disappointment": EmotionType.SADNESS,
        "disapproval": EmotionType.DISGUST,
        "disgust": EmotionType.DISGUST,
        "embarrassment": EmotionType.ANXIETY, # Social anxiety
        "excitement": EmotionType.EUPHORIA,
        "fear": EmotionType.FEAR,
        "gratitude": EmotionType.JOY,
        "grief": EmotionType.DESPAIR,
        "joy": EmotionType.JOY,
        "love": EmotionType.PASSION,
        "nervousness": EmotionType.ANXIETY,
        "optimism": EmotionType.HOPE,
        "pride": EmotionType.TRIUMPH,
        "realization": EmotionType.SURPRISE,
        "relief": EmotionType.SERENITY,
        "remorse": EmotionType.SADNESS,      # or MELANCHOLY
        "sadness": EmotionType.SADNESS,
        "surprise": EmotionType.SURPRISE,
        "neutral": None
    }

    # Taxonomy definitions for categorization
    PRIMARY_EMOTIONS = {
        EmotionType.JOY, EmotionType.SADNESS, EmotionType.ANGER, 
        EmotionType.FEAR, EmotionType.SURPRISE, EmotionType.DISGUST
    }
    
    SECONDARY_EMOTIONS = {
        EmotionType.TENSION, EmotionType.MELANCHOLY, EmotionType.EUPHORIA,
        EmotionType.ANXIETY, EmotionType.NOSTALGIA, EmotionType.LONELINESS
    }
    
    TERTIARY_EMOTIONS = {
        EmotionType.HOPE, EmotionType.DESPAIR, EmotionType.TRIUMPH,
        EmotionType.BETRAYAL, EmotionType.CONFUSION, EmotionType.SERENITY,
        EmotionType.DREAD, EmotionType.PASSION
    }

    def __init__(self):
        """Initialize the emotion detection pipeline"""
        self.pipeline = None
        self._load_model()
        
    def _load_model(self):
        """Load the primary emotion detection model"""
        try:
            logger.info(f"Loading emotion model: {settings.EMOTION_MODEL_PRIMARY}")
            # Use 'text-classification' pipeline with specific model
            # top_k=None ensures we get scores for all labels
            self.pipeline = pipeline(
                "text-classification",
                model=settings.EMOTION_MODEL_PRIMARY,
                top_k=None,
                truncation=True,
                max_length=settings.MAX_SEQUENCE_LENGTH
            )
            logger.info("Emotion model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load emotion model: {str(e)}")
            # In production, might want to raise error or fallback
            self.pipeline = None

    def get_emotion_category(self, emotion: EmotionType) -> EmotionCategory:
        """Determine hierarchy category for an emotion"""
        if emotion in self.PRIMARY_EMOTIONS:
            return EmotionCategory.PRIMARY
        elif emotion in self.SECONDARY_EMOTIONS:
            return EmotionCategory.SECONDARY
        else:
            return EmotionCategory.TERTIARY

    def analyze_text(self, text: str) -> EmotionalArc:
        """
        Analyze text and return a complete EmotionalArc.
        """
        if not self.pipeline or not text.strip():
            # Return neutral/empty result if model failed or text empty
            return self._create_empty_arc()

        try:
            # Run inference
            results = self.pipeline(text)
            # Results is list of lists (one per input text), take first
            model_outputs = results[0]
            
            # Map and aggregate scores
            emotion_scores = {}
            
            for output in model_outputs:
                label = output['label']
                score = output['score']
                
                mapped_emotion = self.GOEMOTIONS_MAP.get(label)
                if mapped_emotion:
                    # Sum scores if multiple labels map to same emotion
                    if mapped_emotion in emotion_scores:
                        emotion_scores[mapped_emotion] += score
                    else:
                        emotion_scores[mapped_emotion] = score

            # Normalize scores if they summed > 1 (simple clamping or softmax if needed)
            # For this purpose, just keeping them is fine as rough 'confidence'
            
            # Filter by threshold and create detections
            detections = []
            for emotion, score in emotion_scores.items():
                if score >= settings.CONFIDENCE_THRESHOLD:
                    # Calculate intensity (0-100) based on score
                    # Score 0.3 -> 30 intensity? Or maybe non-linear scaling?
                    # Let's simple linear: score * 100, clamped at 100
                    intensity = int(min(score * 100, 100))
                    
                    # Clamp confidence to valid range [0.0, 1.0]
                    clamped_confidence = min(score, 1.0)
                    
                    detections.append(EmotionDetection(
                        emotion=emotion,
                        category=self.get_emotion_category(emotion),
                        confidence=clamped_confidence,
                        intensity=intensity
                    ))
            
            # Sort by confidence
            detections.sort(key=lambda x: x.confidence, reverse=True)
            
            if not detections:
                # If nothing passed threshold, take top emotion anyway if it exists
                if emotion_scores:
                    top_emotion = max(emotion_scores.items(), key=lambda x: x[1])
                    if top_emotion[0]: # If not mapped to None
                        emotion, score = top_emotion
                        clamped_confidence = min(score, 1.0)
                        detections.append(EmotionDetection(
                            emotion=emotion,
                            category=self.get_emotion_category(emotion),
                            confidence=clamped_confidence,
                            intensity=int(min(score * 100, 100))
                        ))
            
            if not detections:
                 return self._create_empty_arc()

            # Construct EmotionalArc
            primary = detections[0]
            secondary = detections[1:]
            
            weighted_avg_intensity = sum(d.intensity * d.confidence for d in detections) / sum(d.confidence for d in detections)
            
            return EmotionalArc(
                primary_emotion=primary,
                secondary_emotions=secondary,
                mixed_emotions=len(secondary) > 0,
                emotional_shift=False, # Would need segment analysis to determine shift
                overall_intensity=int(weighted_avg_intensity)
            )

        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return self._create_empty_arc()

    def _create_empty_arc(self) -> EmotionalArc:
        """Create a default neutral/empty emotional arc"""
        # Default to Neutral -> Serenity or just lowest intensity Joy?
        # SIS doesn't have "Neutral". Let's use SERENITY with low intensity.
        default_emotion = EmotionType.SERENITY
        
        detection = EmotionDetection(
            emotion=default_emotion,
            category=EmotionCategory.TERTIARY,
            confidence=0.0,
            intensity=0
        )
        
        return EmotionalArc(
            primary_emotion=detection,
            secondary_emotions=[],
            mixed_emotions=False,
            emotional_shift=False,
            overall_intensity=0
        )
