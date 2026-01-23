import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.parsers.fountain_parser import FountainParser, Scene, ElementType
from app.services.emotion_detector import EmotionDetector
from app.services.visual_mapper import VisualMapper

from app.schemas.sis_schema import (
    SceneIntentSchema, 
    ScriptMetadata, 
    Beat, 
    EmotionType,
    VisualSignals,
    PowerDynamics,
    PacingMetadata,
    EmotionalArc,
    EmotionDetection
)

logger = logging.getLogger(__name__)

class AnalysisService:
    """
    Orchestrator service that combines parsing, emotion detection, 
    and visual mapping into a complete analysis pipeline.
    """

    def __init__(self):
        self.parser = FountainParser()
        self.emotion_detector = EmotionDetector()
        self.visual_mapper = VisualMapper()

    def analyze_script(self, text: str, job_id: str) -> List[SceneIntentSchema]:
        """
        Full pipeline: Parse -> Detect Emotion -> Map Visuals -> Construct Schema
        """
        logger.info(f"Starting analysis for job {job_id}")
        
        # 1. Parse Script
        scenes = self.parser.parse_string(text)
        logger.info(f"Parsed {len(scenes)} scenes")
        
        results = []
        
        for scene in scenes:
            scene_analysis = self._analyze_single_scene(scene, job_id)
            if scene_analysis:
                results.append(scene_analysis)
                
        return results

    def _analyze_single_scene(self, scene: Scene, job_id: str) -> Optional[SceneIntentSchema]:
        """Analyze a single parsed scene"""
        beats: List[Beat] = []
        scene_emotions: List[EmotionDetection] = []
        
        current_character = None
        global_time_cursor = 0.0
        
        # Filter elements to only analyze narrative content
        processable_types = {ElementType.ACTION, ElementType.DIALOGUE, ElementType.CHARACTER}
        
        # We need to look ahead/behind sometimes, but linear pass is easier
        # Grouping logic: Character -> Parenthetical -> Dialogue
        
        buffer_elements = []
        
        for idx, element in enumerate(scene.elements):
            
            if element.element_type == ElementType.CHARACTER:
                current_character = element.content
                continue
                
            if element.element_type not in [ElementType.ACTION, ElementType.DIALOGUE]:
                continue
                
            # Content Processing
            content_text = element.content
            
            # 1. Estimate Timing
            # Rule of thumb: speaking rate ~150 wpm (2.5 words/sec), action reading rate similar
            word_count = len(content_text.split())
            duration = max(1.0, word_count / 2.5) 
            start_time = global_time_cursor
            end_time = global_time_cursor + duration
            global_time_cursor = end_time
            
            # 2. Emotion Detection
            # We use scene number and element index as IDs
            beat_uid = f"{scene.scene_number}-{idx}"
            
            try:
                arc = self.emotion_detector.analyze_text(content_text)
                scene_emotions.append(arc.primary_emotion)
            except Exception as e:
                logger.error(f"Emotion detection failed for beat {beat_uid}: {e}")
                # Fallback to neutral
                # (Ideally we'd construct a NEUTRAL arc here, skipping for brevity)
                continue

            # 3. Pacing (Heuristic)
            pacing = self._calculate_pacing(content_text, duration)
            
            # 4. Power Dynamics (Placeholder / Simple Heuristic)
            power = self._estimate_power(current_character, arc.primary_emotion)
            
            # 5. Visual Mapping
            visuals = self.visual_mapper.map_to_visuals(
                emotional_arc=arc, 
                power_dynamics=power,
                pacing=pacing
            )
            
            # 6. Construct Beat
            beat = Beat(
                beat_id=f"{job_id}-{beat_uid}",
                beat_number=len(beats) + 1,
                timestamp_start=round(start_time, 2),
                timestamp_end=round(end_time, 2),
                dialogue=[content_text] if element.element_type == ElementType.DIALOGUE else [],
                action=[content_text] if element.element_type == ElementType.ACTION else [],
                characters=[current_character] if (current_character and element.element_type == ElementType.DIALOGUE) else [],
                emotional_arc=arc,
                power_dynamics=power,
                pacing=pacing,
                visual_signals=visuals
            )
            beats.append(beat)
            
            # Reset character if action
            if element.element_type == ElementType.ACTION:
                current_character = None

        if not beats:
            return None

        # Scene Aggregation
        dominant_emotion = self._get_dominant_emotion(scene_emotions)
        dominant_emotion_type = dominant_emotion.emotion if dominant_emotion else EmotionType.SERENITY
        
        avg_intensity = int(sum(e.intensity for e in scene_emotions) / len(scene_emotions)) if scene_emotions else 0
        
        # Calculate Range
        unique_emotions = list(set([e.emotion for e in scene_emotions]))
        
        # Calculate Visual Summary (based on dominant emotion)
        summary_arc = EmotionalArc(
            scene_id=str(scene.scene_number),
            segment_id="summary",
            primary_emotion=EmotionDetection(
                emotion=dominant_emotion_type,
                category=dominant_emotion.category if dominant_emotion else EmotionCategory.PRIMARY,
                intensity=avg_intensity,
                confidence=dominant_emotion.confidence if dominant_emotion else 0.0
            ),
            secondary_emotions=[],
            overall_intensity=avg_intensity
        )
        visual_summary = self.visual_mapper.map_to_visuals(summary_arc)

        return SceneIntentSchema(
            analysis_id=job_id,
            script_metadata=ScriptMetadata(
                scene_number=str(scene.scene_number) if scene.scene_number else "0",
                location=scene.location,
                time_of_day=scene.time_of_day,
                characters_present=list(set([c for b in beats for c in b.characters]))
            ),
            beats=beats,
            scene_dominant_emotion=dominant_emotion_type,
            scene_emotional_range=unique_emotions,
            scene_intensity_average=avg_intensity,
            scene_visual_summary=visual_summary
        )

    def _calculate_pacing(self, text: str, duration: float) -> PacingMetadata:
        """Estimate pacing metrics from text"""
        words = text.split()
        word_count = len(words)
        
        bpm = 120 # Standard
        rhythm = "medium"
        
        # Very rough heuristic
        if duration > 0:
            words_per_sec = word_count / duration
            if words_per_sec > 3.0:
                bpm = 140
                rhythm = "fast"
            elif words_per_sec < 1.5:
                bpm = 60
                rhythm = "slow"
                
        # Verb density (simplified: words ending in 'ing', 'ed', 's' - inaccurate but placeholder)
        verbs = [w for w in words if w.endswith('ing') or w.endswith('ed')]
        verb_density = len(verbs) / word_count if word_count > 0 else 0.0
        
        avg_len = sum(len(w) for w in words) / word_count if word_count > 0 else 0
        
        return PacingMetadata(
            bpm=bpm,
            rhythm=rhythm,
            sentence_avg_length=round(avg_len, 1),
            verb_density=round(verb_density, 2)
        )

    def _estimate_power(self, current_char: Optional[str], emotion: EmotionDetection) -> Optional[PowerDynamics]:
        """Estimate power dynamics based on emotion"""
        if not current_char:
            return None
            
        # Basic heuristic: Anger/Triumph = Dominant, Fear/Sadness = Submissive
        balance = "equal"
        score = 50
        
        if emotion.emotion in [EmotionType.ANGER, EmotionType.TRIUMPH, EmotionType.DISGUST]:
            balance = "dominant"
            score = 80
        elif emotion.emotion in [EmotionType.FEAR, EmotionType.SADNESS, EmotionType.ANXIETY]:
            balance = "submissive"
            score = 30
            
        return PowerDynamics(
            dominant_character=current_char if balance == "dominant" else None,
            power_balance=balance,
            power_score=score
        )

    def _get_dominant_emotion(self, emotions: List[EmotionDetection]) -> Optional[EmotionDetection]:
        """Find the most frequent or intense emotion in the scene"""
        if not emotions:
            return None
            
        # Simple Logic: Highest average intensity? Or frequency?
        # Let's go with highest intensity for now
        return max(emotions, key=lambda x: x.intensity)
