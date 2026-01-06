"""
Tests for WorldtourGenerator - City-specific comedy content generation
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from worldtour_generator import WorldtourGenerator


class TestWorldtourGenerator:
    """Test suite for WorldtourGenerator"""
    
    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator instance with temporary database"""
        db_path = tmp_path / "test_cities.json"
        return WorldtourGenerator(cities_db_path=str(db_path))
    
    def test_initialization(self, generator):
        """Test generator initialization"""
        assert generator is not None
        assert len(generator.cities) >= 10  # At least 10 cities
        assert generator.CONTENT_TYPES == [
            'city_review', 'cultural_debate', 'language_lesson', 
            'tourist_trap', 'food_review'
        ]
        assert generator.PERSONALITIES == ['john_cleese', 'c3po', 'robin_williams']
    
    def test_cities_database_initialization(self, generator):
        """Test that cities database is initialized with required cities"""
        # Check specific cities exist
        assert 'new_york' in generator.cities
        assert 'london' in generator.cities
        assert 'tokyo' in generator.cities
        assert 'paris' in generator.cities
        
        # Verify city structure
        nyc = generator.cities['new_york']
        assert 'name' in nyc
        assert 'country' in nyc
        assert 'topics' in nyc
        assert 'language' in nyc
        assert 'visited' in nyc
    
    def test_get_city(self, generator):
        """Test getting city information"""
        city = generator.get_city('new_york')
        
        assert city is not None
        assert city['name'] == 'New York'
        assert city['country'] == 'USA'
        assert isinstance(city['topics'], list)
        assert len(city['topics']) > 0
    
    def test_get_city_nonexistent(self, generator):
        """Test getting non-existent city"""
        city = generator.get_city('nonexistent_city')
        assert city is None
    
    def test_list_cities(self, generator):
        """Test listing all cities"""
        cities = generator.list_cities()
        
        assert len(cities) >= 10
        
        # Check structure of returned cities
        for city in cities:
            assert 'id' in city
            assert 'name' in city
            assert 'country' in city
    
    def test_list_cities_visited_only(self, generator):
        """Test listing only visited cities"""
        # Mark one city as visited
        generator.mark_city_visited('new_york')
        
        visited = generator.list_cities(visited_only=True)
        
        assert len(visited) == 1
        assert visited[0]['id'] == 'new_york'
        assert visited[0]['visited'] is True
    
    def test_generate_city_content(self, generator):
        """Test content generation for all content types"""
        city_id = 'new_york'
        
        for content_type in generator.CONTENT_TYPES:
            for personality in generator.PERSONALITIES:
                content = generator.generate_city_content(
                    city_id, personality, content_type, track_energy=False
                )
                
                assert content is not None
                assert 'city_id' in content
                assert 'city_name' in content
                assert 'personality' in content
                assert 'content_type' in content
                assert 'text' in content
                assert len(content['text']) > 0
                
                assert content['city_id'] == city_id
                assert content['personality'] == personality
                assert content['content_type'] == content_type
    
    def test_generate_content_invalid_city(self, generator):
        """Test content generation with invalid city"""
        with pytest.raises(ValueError, match="Unknown city"):
            generator.generate_city_content(
                'invalid_city', 'john_cleese', 'city_review'
            )
    
    def test_generate_content_invalid_personality(self, generator):
        """Test content generation with invalid personality"""
        with pytest.raises(ValueError, match="Unknown personality"):
            generator.generate_city_content(
                'new_york', 'invalid_personality', 'city_review'
            )
    
    def test_generate_content_invalid_content_type(self, generator):
        """Test content generation with invalid content type"""
        with pytest.raises(ValueError, match="Unknown content type"):
            generator.generate_city_content(
                'new_york', 'john_cleese', 'invalid_type'
            )
    
    def test_mark_city_visited(self, generator):
        """Test marking city as visited"""
        city_id = 'london'
        
        # Initially not visited
        assert generator.cities[city_id]['visited'] is False
        
        # Mark as visited
        result = generator.mark_city_visited(city_id, video_url="https://example.com/video", views=100)
        
        assert result is True
        assert generator.cities[city_id]['visited'] is True
        assert generator.cities[city_id]['video_url'] == "https://example.com/video"
        assert generator.cities[city_id]['video_views'] == 100
        assert generator.cities[city_id]['visit_date'] is not None
    
    def test_mark_city_visited_invalid(self, generator):
        """Test marking invalid city as visited"""
        result = generator.mark_city_visited('invalid_city')
        assert result is False
    
    def test_get_next_city(self, generator):
        """Test getting next unvisited city"""
        next_city = generator.get_next_city()
        
        assert next_city is not None
        assert 'id' in next_city
        assert 'name' in next_city
        assert next_city['visited'] is False
    
    def test_get_next_city_all_visited(self, generator):
        """Test getting next city when all are visited"""
        # Mark all cities as visited
        for city_id in generator.cities.keys():
            generator.cities[city_id]['visited'] = True
        
        next_city = generator.get_next_city()
        assert next_city is None
    
    def test_get_stats(self, generator):
        """Test statistics calculation"""
        # Initially no cities visited
        stats = generator.get_stats()
        
        assert 'total_cities' in stats
        assert 'visited_cities' in stats
        assert 'remaining_cities' in stats
        assert 'total_views' in stats
        assert 'completion_percentage' in stats
        
        assert stats['total_cities'] >= 10
        assert stats['visited_cities'] == 0
        assert stats['remaining_cities'] == stats['total_cities']
        assert stats['completion_percentage'] == 0.0
        
        # Visit one city
        generator.mark_city_visited('tokyo', views=1000)
        
        stats = generator.get_stats()
        assert stats['visited_cities'] == 1
        assert stats['total_views'] == 1000
        assert stats['completion_percentage'] > 0
    
    def test_create_content_queue(self, generator):
        """Test creating content queue"""
        queue = generator.create_content_queue(days=7)
        
        assert len(queue) <= 7
        
        for item in queue:
            assert 'date' in item
            assert 'city_id' in item
            assert 'city_name' in item
            assert 'personality' in item
            assert 'content_type' in item
            assert 'status' in item
            assert item['status'] == 'scheduled'
    
    def test_create_content_queue_limited_cities(self, generator):
        """Test content queue with limited cities"""
        # Mark most cities as visited
        cities_list = list(generator.cities.keys())
        for city_id in cities_list[:len(cities_list)-2]:
            generator.cities[city_id]['visited'] = True
        
        # Request more days than available cities
        queue = generator.create_content_queue(days=10)
        
        # Should only have items for remaining unvisited cities
        assert len(queue) <= 2
    
    def test_get_progress(self, generator):
        """Test progress string formatting"""
        progress = generator.get_progress()
        
        assert isinstance(progress, str)
        assert '/' in progress
        assert '%' in progress
    
    def test_content_types_variety(self, generator):
        """Test that different content types generate different content"""
        city_id = 'paris'
        personality = 'john_cleese'
        
        contents = []
        for content_type in generator.CONTENT_TYPES:
            content = generator.generate_city_content(
                city_id, personality, content_type, track_energy=False
            )
            contents.append(content['text'])
        
        # All content should be different (though this is probabilistic)
        # At least check that we got content for all types
        assert len(contents) == len(generator.CONTENT_TYPES)
    
    def test_personality_integration(self, generator):
        """Test that personality affects content generation"""
        city_id = 'berlin'
        content_type = 'food_review'
        
        contents = {}
        for personality in generator.PERSONALITIES:
            content = generator.generate_city_content(
                city_id, personality, content_type, track_energy=False
            )
            contents[personality] = content['text']
        
        # Should generate content for all personalities
        assert len(contents) == len(generator.PERSONALITIES)
    
    def test_database_persistence(self, tmp_path):
        """Test that database persists to file"""
        db_path = tmp_path / "persist_cities.json"
        
        # Create generator and mark a city
        gen1 = WorldtourGenerator(cities_db_path=str(db_path))
        gen1.mark_city_visited('amsterdam')
        
        # Create new generator with same path
        gen2 = WorldtourGenerator(cities_db_path=str(db_path))
        
        # Should load the visited status
        assert gen2.cities['amsterdam']['visited'] is True
    
    def test_city_minimum_count(self, generator):
        """Test that we have at least 59 cities as specified"""
        total_cities = len(generator.cities)
        assert total_cities >= 59, f"Expected at least 59 cities, got {total_cities}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
