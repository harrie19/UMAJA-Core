"""
Tests for World Tour API endpoints
"""
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Add api and src to path
sys.path.insert(0, str(PROJECT_ROOT / "api"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pytest
from api.simple_server import app, get_worldtour_generator


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def worldtour_generator():
    """Get worldtour generator instance"""
    return get_worldtour_generator()


def test_worldtour_status(client):
    """Test GET /worldtour/status"""
    response = client.get('/worldtour/status')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'active'
    assert 'stats' in data
    assert 'next_city' in data
    assert 'mission' in data


def test_worldtour_cities(client):
    """Test GET /worldtour/cities"""
    response = client.get('/worldtour/cities')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'cities' in data
    assert 'count' in data
    assert data['count'] > 0
    assert len(data['cities']) > 0
    
    # Check city structure
    city = data['cities'][0]
    assert 'id' in city
    assert 'name' in city
    assert 'country' in city
    assert 'visited' in city


def test_worldtour_cities_with_limit(client):
    """Test GET /worldtour/cities with limit parameter"""
    response = client.get('/worldtour/cities?limit=5')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['cities']) <= 5


def test_worldtour_start(client):
    """Test POST /worldtour/start"""
    response = client.post('/worldtour/start')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'next_city' in data or 'message' in data
    assert 'stats' in data
    assert 'mission' in data


def test_worldtour_content_get_city_info(client):
    """Test GET /worldtour/content/{city_id} - getting city info"""
    response = client.get('/worldtour/content/new_york')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'city' in data
    assert data['city']['id'] == 'new_york'
    assert data['city']['name'] == 'New York'
    assert 'available_personalities' in data
    assert 'available_content_types' in data


def test_worldtour_content_generate(client):
    """Test GET /worldtour/content/{city_id}?generate=true"""
    response = client.get('/worldtour/content/new_york?generate=true&personality=john_cleese&content_type=city_review')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['generated'] is True
    assert 'content' in data
    assert data['content']['personality'] == 'john_cleese'
    assert data['content']['content_type'] == 'city_review'
    assert data['content']['city_id'] == 'new_york'


def test_worldtour_content_invalid_city(client):
    """Test GET /worldtour/content/{city_id} with invalid city"""
    response = client.get('/worldtour/content/nonexistent_city')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_worldtour_visit_city(client):
    """Test POST /worldtour/visit/{city_id}"""
    response = client.post(
        '/worldtour/visit/paris',
        data=json.dumps({'personality': 'c3po', 'content_type': 'food_review'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'city' in data
    assert data['city']['id'] == 'paris'
    assert data['city']['visited'] is True
    assert 'content' in data
    assert data['content']['personality'] == 'c3po'
    assert data['content']['content_type'] == 'food_review'


def test_worldtour_visit_city_default_params(client, worldtour_generator):
    """Test POST /worldtour/visit/{city_id} with default parameters"""
    response = client.post(
        '/worldtour/visit/tokyo',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'content' in data
    # Personality and content_type should be randomly selected from available options
    assert data['content']['personality'] in worldtour_generator.PERSONALITIES
    assert data['content']['content_type'] in worldtour_generator.CONTENT_TYPES


def test_worldtour_visit_invalid_city(client):
    """Test POST /worldtour/visit/{city_id} with invalid city"""
    response = client.post('/worldtour/visit/nonexistent_city')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_worldtour_visit_invalid_personality(client):
    """Test POST /worldtour/visit/{city_id} with invalid personality"""
    response = client.post(
        '/worldtour/visit/berlin',
        data=json.dumps({'personality': 'invalid_person'}),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data
    assert 'available_personalities' in data


def test_worldtour_generator_initialization():
    """Test that worldtour generator initializes correctly"""
    generator = get_worldtour_generator()
    assert generator is not None
    assert len(generator.cities) > 0
    assert len(generator.PERSONALITIES) == 3
    assert len(generator.CONTENT_TYPES) == 5


def test_worldtour_generator_get_stats(worldtour_generator):
    """Test worldtour generator get_stats method"""
    stats = worldtour_generator.get_stats()
    assert 'total_cities' in stats
    assert 'visited_cities' in stats
    assert 'remaining_cities' in stats
    assert 'total_views' in stats
    assert 'completion_percentage' in stats
    assert stats['total_cities'] > 0


def test_worldtour_generator_get_city(worldtour_generator):
    """Test worldtour generator get_city method"""
    city = worldtour_generator.get_city('new_york')
    assert city is not None
    assert city['name'] == 'New York'
    assert city['country'] == 'USA'
    assert 'topics' in city
    assert 'stereotypes' in city


def test_worldtour_generator_list_cities(worldtour_generator):
    """Test worldtour generator list_cities method"""
    cities = worldtour_generator.list_cities()
    assert len(cities) > 0
    
    city = cities[0]
    assert 'id' in city
    assert 'name' in city
    assert 'country' in city


def test_worldtour_generator_generate_content(worldtour_generator):
    """Test worldtour generator generate_city_content method"""
    content = worldtour_generator.generate_city_content(
        'london',
        'john_cleese',
        'city_review'
    )
    assert content is not None
    assert content['city_id'] == 'london'
    assert content['city_name'] == 'London'
    assert content['personality'] == 'john_cleese'
    assert content['content_type'] == 'city_review'
    assert 'topic' in content
    assert len(content['topic']) > 0


def test_root_endpoint_includes_worldtour(client):
    """Test that root endpoint includes worldtour information"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'worldtour' in data
    assert 'endpoints' in data
    assert 'worldtour_start' in data['endpoints']
    assert 'worldtour_visit' in data['endpoints']
    assert 'worldtour_status' in data['endpoints']
    assert 'worldtour_cities' in data['endpoints']
    assert 'worldtour_content' in data['endpoints']
