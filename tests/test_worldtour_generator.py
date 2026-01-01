"""
Tests for WorldtourGenerator - City-specific content generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from worldtour_generator import WorldtourGenerator


def test_worldtour_generator_instantiation():
    """Test that WorldtourGenerator can be instantiated"""
    generator = WorldtourGenerator()
    assert generator is not None
    assert hasattr(generator, 'cities')


def test_get_next_city():
    """Test getting the next city to visit"""
    generator = WorldtourGenerator()
    next_city = generator.get_next_city()
    
    # Should return a city (unless all are visited)
    if next_city:
        assert 'id' in next_city
        assert 'name' in next_city
        assert 'country' in next_city
        assert 'topics' in next_city
        assert 'stereotypes' in next_city
        assert 'fun_facts' in next_city
        assert 'visited' in next_city
        assert next_city['visited'] is False


def test_generate_city_content():
    """Test generating content for a city"""
    generator = WorldtourGenerator()
    next_city = generator.get_next_city()
    
    if next_city:
        city_id = next_city['id']
        
        # Test with different personalities
        for personality in ['john_cleese', 'c3po', 'robin_williams']:
            content = generator.generate_city_content(
                city_id=city_id,
                personality=personality,
                content_type='city_review'
            )
            
            assert content is not None
            assert 'city_id' in content
            assert 'personality' in content
            assert 'content_type' in content


def test_content_types():
    """Test that all content types work"""
    generator = WorldtourGenerator()
    next_city = generator.get_next_city()
    
    if next_city:
        city_id = next_city['id']
        content_types = ['city_review', 'food_review', 'cultural_debate']
        
        for content_type in content_types:
            content = generator.generate_city_content(
                city_id=city_id,
                personality='john_cleese',
                content_type=content_type
            )
            assert content is not None
            assert content['content_type'] == content_type


def test_get_progress():
    """Test getting world tour progress"""
    generator = WorldtourGenerator()
    progress = generator.get_progress()
    
    assert 'total_cities' in progress
    assert 'visited' in progress
    assert 'remaining' in progress
    assert progress['total_cities'] >= 0
    assert progress['visited'] >= 0
    assert progress['remaining'] >= 0
    assert progress['total_cities'] == progress['visited'] + progress['remaining']
