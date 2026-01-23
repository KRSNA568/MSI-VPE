"""
Test Fountain Parser
"""

import pytest
from pathlib import Path
from app.parsers.fountain_parser import FountainParser, ElementType


@pytest.fixture
def parser():
    """Create parser instance"""
    return FountainParser()


@pytest.fixture
def sample_fountain():
    """Sample Fountain content"""
    return """Title: Test Scene
Author: Test Author

INT. COFFEE SHOP - DAY

A cozy cafe. SARAH sits alone, nervous.

MARCUS enters.

MARCUS
Sarah. It's been a long time.

SARAH
(quietly)
Three years.

An uncomfortable silence.

MARCUS
I had to see you.

SARAH
(angry)
You left me!

She stands and exits.

FADE OUT.
"""


def test_parse_title_page(parser, sample_fountain):
    """Test title page parsing"""
    scenes = parser.parse_string(sample_fountain)
    
    assert "title" in parser.title_page
    assert parser.title_page["title"] == "Test Scene"
    assert parser.title_page["author"] == "Test Author"


def test_parse_scene_heading(parser, sample_fountain):
    """Test scene heading detection"""
    scenes = parser.parse_string(sample_fountain)
    
    assert len(scenes) == 1
    assert scenes[0].interior_exterior == "INT"
    assert "COFFEE SHOP" in scenes[0].location
    assert scenes[0].time_of_day == "DAY"


def test_parse_dialogue(parser, sample_fountain):
    """Test dialogue extraction"""
    scenes = parser.parse_string(sample_fountain)
    dialogue = scenes[0].get_dialogue()
    
    assert len(dialogue) >= 2
    # Extract character names and normalize for comparison
    characters = [d["character"].upper() if isinstance(d["character"], str) else d["character"] for d in dialogue]
    assert any("MARCUS" in str(c) for c in characters)
    assert any("SARAH" in str(c) for c in characters)


def test_parse_action(parser, sample_fountain):
    """Test action line detection"""
    scenes = parser.parse_string(sample_fountain)
    actions = scenes[0].get_action_lines()
    
    assert len(actions) > 0
    assert any("cafe" in action.lower() for action in actions)


def test_parse_parenthetical(parser):
    """Test parenthetical detection"""
    content = """
INT. ROOM - DAY

CHARACTER
(whispering)
Secret message.
"""
    scenes = parser.parse_string(content)
    elements = scenes[0].elements
    
    parentheticals = [e for e in elements if e.element_type == ElementType.PARENTHETICAL]
    assert len(parentheticals) > 0


def test_multiple_scenes(parser):
    """Test parsing multiple scenes"""
    content = """
INT. ROOM ONE - DAY

Action in room one.

EXT. STREET - NIGHT

Action on street.
"""
    scenes = parser.parse_string(content)
    
    assert len(scenes) == 2
    assert scenes[0].interior_exterior == "INT"
    assert scenes[1].interior_exterior == "EXT"


def test_get_all_dialogue_text(parser, sample_fountain):
    """Test extracting all dialogue as text"""
    parser.parse_string(sample_fountain)
    all_dialogue = parser.get_all_dialogue_text()
    
    assert len(all_dialogue) > 0
    assert "long time" in all_dialogue.lower()


def test_get_all_action_text(parser, sample_fountain):
    """Test extracting all action as text"""
    parser.parse_string(sample_fountain)
    all_action = parser.get_all_action_text()
    
    assert len(all_action) > 0
    assert "cafe" in all_action.lower() or "coffee shop" in all_action.lower()
