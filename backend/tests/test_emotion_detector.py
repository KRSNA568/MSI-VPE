"""
Tests for Emotion Detection Service
"""

import pytest
from unittest.mock import MagicMock, patch
from app.services.emotion_detector import EmotionDetector
from app.schemas.sis_schema import EmotionType, EmotionCategory

@pytest.fixture
def mock_pipeline():
    with patch("app.services.emotion_detector.pipeline") as mock:
        yield mock

@pytest.fixture
def detector(mock_pipeline):
    # Determine settings within the test context if needed
    return EmotionDetector()

def test_initialization(mock_pipeline):
    """Test service initialization loads pipeline"""
    detector = EmotionDetector()
    mock_pipeline.assert_called_once()
    assert detector.pipeline is not None

def test_category_classification(detector):
    """Test emotion categorization taxonomy"""
    assert detector.get_emotion_category(EmotionType.JOY) == EmotionCategory.PRIMARY
    assert detector.get_emotion_category(EmotionType.ANXIETY) == EmotionCategory.SECONDARY
    assert detector.get_emotion_category(EmotionType.TRIUMPH) == EmotionCategory.TERTIARY

def test_analyze_text_joy(detector):
    """Test analyzing text with clear joy emotion"""
    # Mock pipeline output for "I am so happy!"
    # GoEmotions output format: list of dicts [{'label': 'joy', 'score': 0.95}, ...]
    mock_output = [[
        {'label': 'joy', 'score': 0.9},
        {'label': 'excitement', 'score': 0.8},
        {'label': 'neutral', 'score': 0.1}
    ]]
    detector.pipeline.return_value = mock_output
    
    arc = detector.analyze_text("I am so happy!")
    
    assert arc.primary_emotion.emotion == EmotionType.JOY # excitement maps to EUPHORIA, joy to JOY. 0.9 > 0.8
    assert arc.primary_emotion.category == EmotionCategory.PRIMARY
    assert arc.overall_intensity > 0
    assert len(arc.secondary_emotions) > 0
    assert arc.secondary_emotions[0].emotion == EmotionType.EUPHORIA # excitement -> euphoria

def test_analyze_text_mixed(detector):
    """Test analyzing text with mixed emotions"""
    # "I love it but it scares me" -> love + fear
    mock_output = [[
        {'label': 'love', 'score': 0.8},
        {'label': 'fear', 'score': 0.75}, 
        {'label': 'neutral', 'score': 0.05}
    ]]
    detector.pipeline.return_value = mock_output
    
    arc = detector.analyze_text("I love it but it scares me")
    
    # love -> PASSION, fear -> FEAR
    assert arc.mixed_emotions is True
    assert arc.primary_emotion.emotion == EmotionType.PASSION
    assert arc.secondary_emotions[0].emotion == EmotionType.FEAR

def test_empty_text(detector):
    """Test handling of empty text"""
    arc = detector.analyze_text("")
    assert arc.overall_intensity == 0
    assert arc.primary_emotion.emotion == EmotionType.SERENITY # Default neutral

def test_mapping_aggregation(detector):
    """Test aggregating scores for mapped emotions"""
    # annoyance (0.4) + anger (0.5) -> should sum to ANGER 0.9
    mock_output = [[
        {'label': 'annoyance', 'score': 0.4},
        {'label': 'anger', 'score': 0.5},
        {'label': 'neutral', 'score': 0.1}
    ]]
    detector.pipeline.return_value = mock_output
    
    arc = detector.analyze_text("It makes me mad and annoyed.")
    
    assert arc.primary_emotion.emotion == EmotionType.ANGER
    # Score should be sum of 0.4+0.5 = 0.9? Or logic might differ.
    # Current logic sums them.
    assert arc.primary_emotion.confidence >= 0.9
