"""
UMAJA WORLDTOUR - Worldtour Generator
City-specific comedy content generation system
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Literal, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorldtourGenerator:
    """
    City-specific comedy content generation.
    Manages a database of cities and generates themed content.
    """
    
    CONTENT_TYPES = ['city_review', 'cultural_debate', 'language_lesson', 'tourist_trap', 'food_review']
    PERSONALITIES = ['john_cleese', 'c3po', 'robin_williams']
    
    def __init__(self, cities_db_path: str = "data/worldtour_cities.json"):
        """
        Initialize the worldtour generator.
        
        Args:
            cities_db_path: Path to cities database JSON file
        """
        self.cities_db_path = Path(cities_db_path)
        self.cities_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize cities database
        self.cities = self._load_cities_db()
        
        # Content type templates
        self.content_templates = {
            'city_review': {
                'john_cleese': "Now, the curious thing about {city} is that it's rather like {comparison}...",
                'c3po': "Oh my! {city} presents precisely {number} possible interpretations...",
                'robin_williams': "So {city} walks into a bar... *laughs* Picture this!"
            },
            'cultural_debate': {
                'john_cleese': "The British approach to {topic} versus {city}'s method reveals fascinating absurdities...",
                'c3po': "By my calculations, {city}'s {topic} violates {number} known protocols!",
                'robin_williams': "Imagine if {topic} in {city} was a Broadway musical!"
            },
            'language_lesson': {
                'john_cleese': "Learning to say {phrase} in {language} is remarkably similar to gargling marbles...",
                'c3po': "The linguistic structure of {phrase} exhibits {number} phonetic variations...",
                'robin_williams': "*switches accent* So you want to say {phrase}? Let me show you..."
            },
            'tourist_trap': {
                'john_cleese': "The {attraction} in {city} attracts tourists like moths to a particularly overpriced flame...",
                'c3po': "Warning! {attraction} presents a {number}% probability of tourist confusion!",
                'robin_williams': "You haven't lived until you've seen {attraction}! *laughs* Or have you?"
            },
            'food_review': {
                'john_cleese': "Attempting to eat {food} in {city} requires the coordination of a trained acrobat...",
                'c3po': "Goodness! {food} contains exactly {number} ingredients, by my analysis...",
                'robin_williams': "So {food} and I are having a moment... *laughs* It's complicated!"
            }
        }
    
    def _load_cities_db(self) -> Dict:
        """Load cities database from JSON file."""
        if self.cities_db_path.exists():
            try:
                with open(self.cities_db_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load cities database: {e}")
        
        # Initialize with default cities
        return self._initialize_default_cities()
    
    def _initialize_default_cities(self) -> Dict:
        """Initialize database with 50+ cities and their comedy topics."""
        cities = {
            "new_york": {
                "name": "New York",
                "country": "USA",
                "topics": ["pizza", "subway", "Central Park", "Broadway", "hot dogs", "Times Square"],
                "stereotypes": ["Always rushing", "Coffee addicts", "Loud", "Never sleeps"],
                "fun_facts": ["8.3 million people", "800 languages spoken", "Central Park larger than Monaco"],
                "local_phrases": ["Forget about it!", "The City", "Bodega"],
                "language": "English (American)",
                "visited": False,
                "visit_date": None,
                "video_views": 0,
                "video_url": None
            },
            "london": {
                "name": "London",
                "country": "UK",
                "topics": ["tea", "tube", "Big Ben", "fish and chips", "queuing", "weather"],
                "stereotypes": ["Polite", "Tea obsessed", "Love queuing", "Talk about weather"],
                "fun_facts": ["2000 years old", "300 languages", "Invented the sandwich"],
                "local_phrases": ["Bloody hell!", "Cheers", "Mind the gap"],
                "language": "English (British)",
                "visited": False
            },
            "tokyo": {
                "name": "Tokyo",
                "country": "Japan",
                "topics": ["sushi", "trains", "technology", "anime", "vending machines", "karaoke"],
                "stereotypes": ["Ultra polite", "Tech-savvy", "Punctual", "Hardworking"],
                "fun_facts": ["37 million in metro area", "Most Michelin stars", "Busiest train station"],
                "local_phrases": ["Sumimasen", "Kawaii", "Oishii"],
                "language": "Japanese",
                "visited": False
            },
            "paris": {
                "name": "Paris",
                "country": "France",
                "topics": ["croissants", "Eiffel Tower", "fashion", "wine", "art", "baguettes"],
                "stereotypes": ["Romantic", "Fashion-forward", "Artistic", "Love strikes"],
                "fun_facts": ["City of Light", "20 million visitors/year", "300 bakeries"],
                "local_phrases": ["Bonjour", "C'est la vie", "Voilà"],
                "language": "French",
                "visited": False
            },
            "berlin": {
                "name": "Berlin",
                "country": "Germany",
                "topics": ["currywurst", "techno", "history", "beer gardens", "graffiti"],
                "stereotypes": ["Efficient", "Direct", "Party culture", "History-conscious"],
                "fun_facts": ["More bridges than Venice", "1500 museums", "Döner kebab capital"],
                "local_phrases": ["Alles klar", "Schnell", "Prost"],
                "language": "German",
                "visited": False
            },
            "rome": {
                "name": "Rome",
                "country": "Italy",
                "topics": ["pasta", "Colosseum", "gelato", "espresso", "scooters", "ruins"],
                "stereotypes": ["Passionate", "Loud", "Gesticulate", "Late dinners"],
                "fun_facts": ["2800 years old", "280 fountains", "Cat sanctuary"],
                "local_phrases": ["Ciao", "Basta", "Mamma mia"],
                "language": "Italian",
                "visited": False
            },
            "barcelona": {
                "name": "Barcelona",
                "country": "Spain",
                "topics": ["tapas", "Gaudí", "beaches", "sangria", "siesta", "football"],
                "stereotypes": ["Late nights", "Siesta lovers", "Passionate", "Football crazy"],
                "fun_facts": ["Unfinished cathedral 140+ years", "Unique architecture", "Las Ramblas"],
                "local_phrases": ["Hola", "Bon dia", "Tapas"],
                "language": "Spanish/Catalan",
                "visited": False
            },
            "amsterdam": {
                "name": "Amsterdam",
                "country": "Netherlands",
                "topics": ["bikes", "canals", "tulips", "cheese", "windmills", "coffee shops"],
                "stereotypes": ["Tall", "Bike everywhere", "Direct", "Liberal"],
                "fun_facts": ["More bikes than people", "165 canals", "Built on poles"],
                "local_phrases": ["Hallo", "Gezellig", "Lekker"],
                "language": "Dutch",
                "visited": False
            },
            "sydney": {
                "name": "Sydney",
                "country": "Australia",
                "topics": ["beaches", "Opera House", "barbecue", "surfing", "wildlife"],
                "stereotypes": ["Laid back", "Beach lovers", "Friendly", "Outdoorsy"],
                "fun_facts": ["Harbor Bridge climb", "300 days sunshine", "70+ beaches"],
                "local_phrases": ["G'day", "No worries", "Arvo"],
                "language": "English (Australian)",
                "visited": False
            },
            "dubai": {
                "name": "Dubai",
                "country": "UAE",
                "topics": ["skyscrapers", "malls", "desert", "luxury", "Burj Khalifa"],
                "stereotypes": ["Wealthy", "Modern", "Shopping", "Ambitious"],
                "fun_facts": ["Tallest building", "Gold ATMs", "Indoor skiing"],
                "local_phrases": ["Marhaba", "Shukran", "Yalla"],
                "language": "Arabic/English",
                "visited": False
            }
        }
        
        # Add more cities (abbreviated for space)
        more_cities = ["mumbai", "singapore", "bangkok", "istanbul", "moscow", "mexico_city",
                      "rio_de_janeiro", "buenos_aires", "toronto", "vancouver", "chicago",
                      "los_angeles", "san_francisco", "miami", "seattle", "boston",
                      "madrid", "lisbon", "vienna", "prague", "budapest", "athens",
                      "cairo", "cape_town", "nairobi", "lagos", "shanghai", "beijing",
                      "seoul", "hong_kong", "delhi", "jakarta", "manila", "hanoi",
                      "kuala_lumpur", "karachi", "tehran", "baghdad", "tel_aviv",
                      "stockholm", "copenhagen", "oslo", "helsinki", "dublin",
                      "edinburgh", "brussels", "zurich", "munich", "hamburg"]
        
        for city_id in more_cities:
            cities[city_id] = {
                "name": city_id.replace('_', ' ').title(),
                "country": "Various",
                "topics": ["local food", "culture", "landmarks", "people"],
                "stereotypes": ["Unique culture"],
                "fun_facts": ["Rich history"],
                "local_phrases": ["Hello"],
                "language": "Local",
                "visited": False
            }
        
        # Save to file
        self._save_cities_db(cities)
        
        return cities
    
    def _save_cities_db(self, cities: Dict = None):
        """Save cities database to JSON file."""
        if cities is None:
            cities = self.cities
        
        try:
            with open(self.cities_db_path, 'w') as f:
                json.dump(cities, f, indent=2)
            logger.info(f"Saved cities database to {self.cities_db_path}")
        except Exception as e:
            logger.error(f"Could not save cities database: {e}")
    
    def get_city(self, city_id: str) -> Optional[Dict]:
        """Get city information by ID."""
        return self.cities.get(city_id)
    
    def list_cities(self, visited_only: bool = False) -> List[Dict]:
        """
        List all cities in the database.
        
        Args:
            visited_only: If True, only return visited cities
            
        Returns:
            List of city dictionaries
        """
        cities_list = []
        for city_id, city_data in self.cities.items():
            if visited_only and not city_data.get('visited', False):
                continue
            
            cities_list.append({
                'id': city_id,
                **city_data
            })
        
        return cities_list
    
    def generate_city_content(self,
                            city_id: str,
                            personality: Literal['john_cleese', 'c3po', 'robin_williams'],
                            content_type: Literal['city_review', 'cultural_debate', 
                                                'language_lesson', 'tourist_trap', 'food_review']) -> Dict:
        """
        Generate city-specific comedy content.
        
        Args:
            city_id: City identifier
            personality: Comedian personality
            content_type: Type of content to generate
            
        Returns:
            Dictionary with content information
        """
        if city_id not in self.cities:
            raise ValueError(f"Unknown city: {city_id}")
        
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        if content_type not in self.CONTENT_TYPES:
            raise ValueError(f"Unknown content type: {content_type}")
        
        city = self.cities[city_id]
        template = self.content_templates[content_type][personality]
        
        # Generate content based on type
        if content_type == 'city_review':
            comparison = random.choice([
                "a confused tourist with a map",
                "organized chaos",
                "a beautiful disaster",
                "an elaborate stage production"
            ])
            # Handle templates that need 'number' parameter (like c3po)
            if '{number}' in template:
                topic = template.format(city=city['name'], number=random.randint(100, 9999))
            else:
                topic = template.format(city=city['name'], comparison=comparison)
            
        elif content_type == 'cultural_debate':
            topic_item = random.choice(city['topics'])
            topic = template.format(
                city=city['name'],
                topic=topic_item,
                number=random.randint(100, 9999)
            )
            
        elif content_type == 'language_lesson':
            phrase = random.choice(city.get('local_phrases', ['Hello']))
            topic = template.format(
                phrase=phrase,
                city=city['name'],
                language=city['language'],
                number=random.randint(2, 20)
            )
            
        elif content_type == 'tourist_trap':
            attraction = random.choice(city['topics'])
            topic = template.format(
                attraction=attraction,
                city=city['name'],
                number=random.randint(60, 99)
            )
            
        else:  # food_review
            food = random.choice([t for t in city['topics'] if any(f in t.lower() 
                                for f in ['food', 'pizza', 'sushi', 'tea', 'pasta'])] 
                               or city['topics'])
            topic = template.format(
                food=food,
                city=city['name'],
                number=random.randint(3, 50)
            )
        
        return {
            'city_id': city_id,
            'city_name': city['name'],
            'country': city['country'],
            'personality': personality,
            'content_type': content_type,
            'topic': topic,
            'topics': city['topics'],
            'stereotypes': city['stereotypes'],
            'fun_facts': city['fun_facts'],
            'language': city['language']
        }
    
    def mark_city_visited(self, city_id: str, video_url: Optional[str] = None, 
                         views: int = 0):
        """
        Mark a city as visited and update stats.
        
        Args:
            city_id: City identifier
            video_url: URL of the video
            views: Number of views
        """
        if city_id in self.cities:
            self.cities[city_id]['visited'] = True
            self.cities[city_id]['visit_date'] = datetime.now().isoformat()
            if video_url:
                self.cities[city_id]['video_url'] = video_url
            self.cities[city_id]['video_views'] = views
            
            self._save_cities_db()
            logger.info(f"Marked {city_id} as visited")
    
    def get_next_city(self) -> Optional[Dict]:
        """Get the next unvisited city."""
        unvisited = [city for city_id, city in self.cities.items() 
                    if not city.get('visited', False)]
        
        if unvisited:
            # Randomly select from unvisited cities
            city_id = random.choice([k for k, v in self.cities.items() 
                                   if not v.get('visited', False)])
            return {
                'id': city_id,
                **self.cities[city_id]
            }
        
        return None
    
    def create_content_queue(self, days: int = 7) -> List[Dict]:
        """
        Create a queue of upcoming content for the next N days.
        
        Args:
            days: Number of days to plan
            
        Returns:
            List of scheduled content items
        """
        queue = []
        start_date = datetime.now()
        
        for i in range(days):
            # Get next unvisited city
            next_city = self.get_next_city()
            if not next_city:
                break
            
            # Rotate through personalities
            personality = self.PERSONALITIES[i % len(self.PERSONALITIES)]
            
            # Rotate through content types
            content_type = self.CONTENT_TYPES[i % len(self.CONTENT_TYPES)]
            
            # Schedule date
            schedule_date = start_date + timedelta(days=i)
            
            queue.append({
                'date': schedule_date.isoformat(),
                'city_id': next_city['id'],
                'city_name': next_city['name'],
                'personality': personality,
                'content_type': content_type,
                'status': 'scheduled'
            })
        
        return queue
    
    def get_stats(self) -> Dict:
        """Get worldtour statistics."""
        total_cities = len(self.cities)
        visited = sum(1 for c in self.cities.values() if c.get('visited', False))
        total_views = sum(c.get('video_views', 0) for c in self.cities.values())
        
        return {
            'total_cities': total_cities,
            'visited_cities': visited,
            'remaining_cities': total_cities - visited,
            'total_views': total_views,
            'completion_percentage': round((visited / total_cities) * 100, 1)
        }


# Example usage and testing
if __name__ == "__main__":
    generator = WorldtourGenerator()
    
    print("Worldtour Generator Test")
    print("=" * 60)
    
    # Get stats
    stats = generator.get_stats()
    print(f"\nWorldtour Stats:")
    print(f"  Total cities: {stats['total_cities']}")
    print(f"  Visited: {stats['visited_cities']}")
    print(f"  Remaining: {stats['remaining_cities']}")
    
    # Generate content for a city
    print(f"\nGenerating content for New York...")
    content = generator.generate_city_content('new_york', 'john_cleese', 'city_review')
    print(f"  Topic: {content['topic']}")
    print(f"  Fun facts: {content['fun_facts']}")
    
    # Create weekly queue
    print(f"\nCreating 7-day content queue...")
    queue = generator.create_content_queue(7)
    for item in queue[:3]:
        print(f"  {item['date'][:10]}: {item['city_name']} - {item['personality']} - {item['content_type']}")
