import unittest
from unittest.mock import MagicMock, patch
from app.services.analysis_service import AnalysisService
from app.schemas.sis_schema import (
    EmotionDetection, EmotionType, EmotionCategory, EmotionalArc,
    SceneIntentSchema
)

class TestAnalysisService(unittest.TestCase):
    def setUp(self):
        # Patch the EmotionDetector inside AnalysisService to avoid loading ML model
        self.mock_emotion_patcher = patch('app.services.analysis_service.EmotionDetector')
        self.MockEmotionDetector = self.mock_emotion_patcher.start()
        
        # Setup the service with mocked detector
        self.service = AnalysisService()
        self.service.emotion_detector = MagicMock()
        
        # Mock Response - using analyze_text method (called by analysis_service)
        self.mock_arc = EmotionalArc(
            scene_id="1",
            segment_id="1-0",
            primary_emotion=EmotionDetection(
                emotion=EmotionType.JOY,
                category=EmotionCategory.PRIMARY,
                intensity=80,
                confidence=0.9
            ),
            secondary_emotions=[],
            overall_intensity=80
        )
        self.service.emotion_detector.analyze_text.return_value = self.mock_arc

    def tearDown(self):
        self.mock_emotion_patcher.stop()

    def test_analyze_simple_scene(self):
        script_text = """
INT. CAFE - DAY

JOHN
Hello world.
"""
        results = self.service.analyze_script(script_text, "job_123")
        
        self.assertEqual(len(results), 1)
        sis = results[0]
        self.assertIsInstance(sis, SceneIntentSchema)
        # Check metadata
        self.assertEqual(sis.script_metadata.location, "CAFE")
        # FountainParser often extracts INT./EXT. and Time separately or as parts
        # "INT. CAFE - DAY" -> Location: CAFE, Time: DAY?
        # Let's check what the mock parser produces essentially.
        # Actually FountainParser logic:
        # Regex: (INT|EXT...) (.+?) (- (.+))?
        # Heading: INT. CAFE - DAY
        # Location: CAFE
        # Time: DAY (if parser is robust)
        # We'll assert location contains CAFE
        self.assertIn("CAFE", sis.script_metadata.location)
        
        # Check Beats
        # Beat 1: Dialogue (Action implicit?)
        # Parser logic: 
        # Line 1: INT. CAFE -> Heading
        # Line 3: JOHN -> Character
        # Line 4: Hello world -> Dialogue
        
        # AnalysisService ignores Character element, processes Dialogue element.
        # So we expect 1 beat (Dialogue).
        self.assertEqual(len(sis.beats), 1)
        self.assertEqual(sis.beats[0].dialogue[0], "Hello world.")
        self.assertEqual(sis.beats[0].characters[0], "JOHN")
        
        # Check Visuals (Mapped from Joy)
        # VisualMapper logic: Joy -> High Key, Warm
        self.assertEqual(sis.beats[0].visual_signals.lighting.technique, "high_key")

    def test_pacing_calculation(self):
        text = "This is a sentence. And another one. Running fast."
        pacing = self.service._calculate_pacing(text, duration=2.0)
        self.assertGreater(pacing.bpm, 60)
        self.assertIsNotNone(pacing.rhythm)

if __name__ == "__main__":
    unittest.main()
