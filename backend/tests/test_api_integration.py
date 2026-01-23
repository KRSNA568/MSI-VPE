import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.analysis_service import AnalysisService
from app.schemas.sis_schema import (
    SceneIntentSchema, ScriptMetadata, EmotionType, VisualSignals, 
    EmotionDetection, EmotionCategory, LightingParameters, CameraParameters,
    ColorPalette, CameraAngleHorizontal, CameraAngleVertical, CameraMovement,
    ShotSize, LightingDirection, LightingTechnique, Beat, EmotionalArc,
    PacingMetadata, PowerDynamics
)

from app.models.job import JobStatus, AnalysisJob

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        # Mock Service
        self.mock_service = MagicMock(spec=AnalysisService)
        self.client = TestClient(app)
        
        # Mock DB Session
        self.mock_db = MagicMock()
        
        # Override dependency
        from app.api.endpoints.analysis import get_analysis_service
        from app.core.database import get_db
        
        app.dependency_overrides[get_analysis_service] = lambda: self.mock_service
        app.dependency_overrides[get_db] = lambda: self.mock_db

    def test_analyze_endpoint_success(self):
        # Setup Mock Return with VALID data
        arc = EmotionalArc(
            scene_id="1",
            segment_id="1-1",
            primary_emotion=EmotionDetection(
                emotion=EmotionType.JOY,
                category=EmotionCategory.PRIMARY,
                intensity=80,
                confidence=0.9
            ),
            secondary_emotions=[],
            overall_intensity=80
        )
        
        mock_result = SceneIntentSchema(
            analysis_id="test_job",
            script_metadata=ScriptMetadata(
                scene_number="1",
                location="CAFE",
                time_of_day="DAY"
            ),
            beats=[
                Beat(
                    beat_id="1-1",
                    beat_number=1,
                    timestamp_start=0,
                    timestamp_end=1,
                    dialogue=["Hello"],
                    emotional_arc=arc,
                    pacing=PacingMetadata(
                        bpm=100, 
                        rhythm="medium",
                        sentence_avg_length=5,
                        verb_density=0.1
                    ),
                    visual_signals=VisualSignals(
                         lighting=LightingParameters(
                            quality=80,
                            temperature_kelvin=3200,
                            direction=LightingDirection.SIDE,
                            intensity="high",
                            contrast_ratio="2:1",
                            shadow_type="diffused",
                            technique=LightingTechnique.HIGH_KEY
                        ),
                        camera=CameraParameters(
                            vertical_angle=CameraAngleVertical.EYE_LEVEL,
                            horizontal_angle=CameraAngleHorizontal.FRONTAL,
                            movement=CameraMovement.STATIC,
                            shot_size=ShotSize.MS,
                            focal_length_mm=50,
                            depth_of_field="medium"
                        ),
                        colors=ColorPalette(
                            primary_colors=["#FFD700"],
                            secondary_colors=["#FFA500"],
                            accent_colors=["#FFFFFF"],
                            saturation=80,
                            brightness=80,
                            harmony_type="analogous"
                        ),
                        confidence_score=0.9,
                        reasoning="Test"
                    )
                )
            ],
            scene_dominant_emotion=EmotionType.JOY,
            scene_emotional_range=[EmotionType.JOY],
            scene_intensity_average=80,
            scene_visual_summary=VisualSignals(
                lighting=LightingParameters(
                    quality=80,
                    temperature_kelvin=3200,
                    direction=LightingDirection.SIDE,
                    intensity="high",
                    contrast_ratio="2:1",
                    shadow_type="diffused",
                    technique=LightingTechnique.HIGH_KEY
                ),
                camera=CameraParameters(
                    vertical_angle=CameraAngleVertical.EYE_LEVEL,
                    horizontal_angle=CameraAngleHorizontal.FRONTAL,
                    movement=CameraMovement.STATIC,
                    shot_size=ShotSize.MS,
                    focal_length_mm=50,
                    depth_of_field="medium"
                ),
                colors=ColorPalette(
                    primary_colors=["#FFD700"],
                    secondary_colors=["#FFA500"],
                    accent_colors=["#FFFFFF"],
                    saturation=80,
                    brightness=80,
                    harmony_type="analogous"
                ),
                confidence_score=0.9,
                reasoning="Test reasoning"
            )
        )
        self.mock_service.analyze_script.return_value = [mock_result]
        
        payload = {
            "script_text": "INT. CAFE - DAY\n\nJOHN\nHello world.",
            "analyze_full_script": False
        }
        
        response = self.client.post("/api/v1/analyze", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "completed")
        self.assertEqual(data["result"]["script_metadata"]["location"], "CAFE")

    def test_analyze_endpoint_failure(self):
        self.mock_service.analyze_script.side_effect = Exception("Parsing error")
        
        payload = {
            "script_text": "INVALID SCRIPT TEXT LONG ENOUGH"
        }
        
        response = self.client.post("/api/v1/analyze", json=payload)
        self.assertEqual(response.status_code, 200) # Returns 200 but context status failed
        data = response.json()
        self.assertEqual(data["status"], "failed")
        self.assertIn("Parsing error", data["error"])


    def test_get_job_status(self):
        """Test retrieving a job from DB"""
        # Mock DB Query
        mock_job = AnalysisJob(
            id="job_123",
            status=JobStatus.PROCESSING,
            error_message=None
        )
        # SQLAlchemy mocking is verbose, usually better to mock the query chain: db.query().filter().first()
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_job
        
        response = self.client.get("/api/v1/jobs/job_123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "processing")

if __name__ == "__main__":
    unittest.main()
