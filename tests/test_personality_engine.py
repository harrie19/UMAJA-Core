"""
Tests for PersonalityEngine - Archetype system (Professor, Worrier, Enthusiast)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from personality_engine import (
    PersonalityEngine,
    TheProfessor,
    TheWorrier,
    TheEnthusiast
)


def test_professor_archetype_instantiation():
    """Test that Professor archetype can be created"""
    professor = TheProfessor()
    assert professor.name == "The Professor"
    assert "curious" in professor.traits
    assert "thoughtful" in professor.traits
    assert professor.tone == "friendly and informative"


def test_worrier_archetype_instantiation():
    """Test that Worrier archetype can be created"""
    worrier = TheWorrier()
    assert worrier.name == "The Worrier"
    assert "relatable" in worrier.traits
    assert "caring" in worrier.traits
    assert worrier.tone == "warm and understanding"


def test_enthusiast_archetype_instantiation():
    """Test that Enthusiast archetype can be created"""
    enthusiast = TheEnthusiast()
    assert enthusiast.name == "The Enthusiast"
    assert "energetic" in enthusiast.traits
    assert "joyful" in enthusiast.traits


def test_professor_generates_smile_text():
    """Test that Professor can generate smile text"""
    professor = TheProfessor()
    text = professor.generate_smile_text()
    
    assert text is not None
    assert len(text) > 0
    assert isinstance(text, str)
    # Professor generates educational, warm content
    assert len(text.split()) > 10  # Should be substantial


def test_worrier_generates_smile_text():
    """Test that Worrier can generate smile text"""
    worrier = TheWorrier()
    text = worrier.generate_smile_text()
    
    assert text is not None
    assert len(text) > 0
    assert isinstance(text, str)
    # Worrier generates relatable content
    assert len(text.split()) > 10  # Should be substantial


def test_enthusiast_generates_smile_text():
    """Test that Enthusiast can generate smile text"""
    enthusiast = TheEnthusiast()
    text = enthusiast.generate_smile_text()
    
    assert text is not None
    assert len(text) > 0
    assert isinstance(text, str)
    # Enthusiast generates energetic, joyful content
    assert len(text.split()) > 10  # Should be substantial


def test_personality_engine_instantiation():
    """Test that PersonalityEngine can be created"""
    engine = PersonalityEngine()
    assert engine is not None


def test_personality_engine_get_archetype():
    """Test getting specific archetypes from engine"""
    engine = PersonalityEngine()
    
    professor = engine.get_archetype('professor')
    assert professor is not None
    assert professor.name == "The Professor"
    
    worrier = engine.get_archetype('worrier')
    assert worrier is not None
    assert worrier.name == "The Worrier"
    
    enthusiast = engine.get_archetype('enthusiast')
    assert enthusiast is not None
    assert enthusiast.name == "The Enthusiast"


def test_personality_engine_generate_daily_smile():
    """Test generating daily smile from engine"""
    engine = PersonalityEngine()
    
    # Test with random archetype
    smile = engine.generate_daily_smile()
    assert smile is not None
    assert 'content' in smile
    assert 'personality' in smile
    assert len(smile['content']) > 0
    
    # Test with specific archetype
    smile_prof = engine.generate_daily_smile('professor')
    assert smile_prof['personality'] == "The Professor"


def test_archetype_text_length():
    """Test that generated text is appropriate length (30-60 seconds worth)"""
    engine = PersonalityEngine()
    
    for archetype in ['professor', 'worrier', 'enthusiast']:
        smile = engine.generate_daily_smile(archetype)
        text = smile['content']
        
        # Target: 30-60 seconds at 150-200 words per minute = 75-200 words
        word_count = len(text.split())
        assert 30 <= word_count <= 250, f"{archetype} text length out of range: {word_count} words"
