import unittest
from app.services.visual_mapper import VisualMapper
from app.schemas.sis_schema import (
    EmotionalArc, EmotionDetection, EmotionType, EmotionCategory,
    VisualSignals, LightingTechnique, CameraAngleVertical, 
    CameraMovement, ShotSize, PowerDynamics, PacingMetadata
)

class TestVisualMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = VisualMapper()

    def test_map_fear_visuals(self):
        """Test if FEAR validates to High Angle and Chiaroscuro"""
        # Create a synthetic Fear arc
        arc = EmotionalArc(
            scene_id="1",
            segment_id="1A",
            primary_emotion=EmotionDetection(
                emotion=EmotionType.FEAR,
                category=EmotionCategory.PRIMARY,
                intensity=90,
                confidence=0.95
            ),
            secondary_emotions=[],
            overall_intensity=90
        )
        
        signals = self.mapper.map_to_visuals(arc)
        
        # Check Camera
        self.assertEqual(signals.camera.vertical_angle, CameraAngleVertical.HIGH, "Fear should map to High Angle (Vulnerability)")
        
        # Check Lighting
        self.assertEqual(signals.lighting.technique, LightingTechnique.CHIAROSCURO, "Fear should map to Chiaroscuro")
        self.assertGreater(signals.lighting.temperature_kelvin, 5000, "Fear should be cool/blue")

    def test_map_joy_visuals(self):
        """Test if JOY maps to High Key and Warmth"""
        arc = EmotionalArc(
            scene_id="2",
            segment_id="2A",
            primary_emotion=EmotionDetection(
                emotion=EmotionType.JOY,
                category=EmotionCategory.PRIMARY,
                intensity=80,
                confidence=0.9
            ),
            secondary_emotions=[],
            overall_intensity=80
        )
        
        signals = self.mapper.map_to_visuals(arc)
        
        self.assertEqual(signals.lighting.technique, LightingTechnique.HIGH_KEY)
        self.assertLess(signals.lighting.temperature_kelvin, 4000, "Joy should be warm")

    def test_power_dynamics_override(self):
        """Test if Power Dynamics metadata overrides default emotion mapping"""
        # Anger usually means Low Angle, but here we force Submissive (High Angle)
        arc = EmotionalArc(
            scene_id="3",
            segment_id="3A",
            primary_emotion=EmotionDetection(
                emotion=EmotionType.ANGER,
                category=EmotionCategory.PRIMARY,
                intensity=80,
                confidence=0.9
            ),
            secondary_emotions=[],
            overall_intensity=80
        )
        
        power = PowerDynamics(
            dominant_character="Villain",
            power_balance="submissive", # The scene focus (Hero) is submissive
            power_score=80
        )
        
        signals = self.mapper.map_to_visuals(arc, power_dynamics=power)
        
        # Should be HIGH angle due to 'submissive' power dynamic, overriding Anger's default
        self.assertEqual(signals.camera.vertical_angle, CameraAngleVertical.HIGH)

    def test_pacing_influence(self):
        """Test if Fast Pacing forces Handheld"""
        arc = EmotionalArc(
            scene_id="4",
            segment_id="4A",
            primary_emotion=EmotionDetection(
                emotion=EmotionType.SERENITY,
                category=EmotionCategory.SECONDARY,
                intensity=50,
                confidence=0.9
            ),
            secondary_emotions=[],
            overall_intensity=50
        )
        
        pacing = PacingMetadata(
            bpm=120,
            rhythm="fast",
            sentence_avg_length=10.0,
            verb_density=0.8
        )
        
        signals = self.mapper.map_to_visuals(arc, pacing=pacing)
        
        self.assertEqual(signals.camera.movement, CameraMovement.HANDHELD)

if __name__ == "__main__":
    unittest.main()
