"""
UMAJA Core Integration Module
Ties together all UMAJA capabilities for seamless operation
"""

import logging
from typing import Dict, Optional, Any, List
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UMAJACore:
    """
    Central integration point for all UMAJA capabilities
    
    Features:
    - Personality-driven content generation (3 comedians + 3 archetypes)
    - World Tour city content
    - Energy-efficient operations
    - Vector-based agent communication
    - Mission alignment (Bahá'í principles)
    """
    
    def __init__(self, enable_energy_monitoring: bool = True):
        """Initialize UMAJA Core with all subsystems
        
        Args:
            enable_energy_monitoring: Enable energy consumption tracking
        """
        self.enable_energy_monitoring = enable_energy_monitoring
        
        # Initialize subsystems
        self._init_personality_engine()
        self._init_worldtour_generator()
        self._init_vector_analyzer()
        self._init_energy_monitor()
        
        logger.info("UMAJA Core initialized successfully")
        logger.info("Mission: Bringing smiles to 8 billion people")
        logger.info("Principle: Truth, Unity, Service")
    
    def _init_personality_engine(self):
        """Initialize personality engine with all personalities"""
        try:
            from personality_engine import PersonalityEngine
            self.personality_engine = PersonalityEngine()
            logger.info(f"Personality Engine: {len(self.personality_engine.list_comedians())} comedians, "
                       f"{len(self.personality_engine.list_archetypes())} archetypes")
        except Exception as e:
            logger.error(f"Failed to initialize personality engine: {e}")
            self.personality_engine = None
    
    def _init_worldtour_generator(self):
        """Initialize World Tour generator"""
        try:
            from worldtour_generator import WorldtourGenerator
            self.worldtour = WorldtourGenerator()
            stats = self.worldtour.get_stats()
            logger.info(f"World Tour: {stats['total_cities']} cities, "
                       f"{stats['visited_cities']} visited ({stats['completion_percentage']}%)")
        except Exception as e:
            logger.error(f"Failed to initialize world tour: {e}")
            self.worldtour = None
    
    def _init_vector_analyzer(self):
        """Initialize vector analyzer for semantic analysis"""
        try:
            from vektor_analyzer import VektorAnalyzer
            self.vector_analyzer = VektorAnalyzer()
            logger.info(f"Vector Analyzer: {self.vector_analyzer.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize vector analyzer: {e}")
            self.vector_analyzer = None
    
    def _init_energy_monitor(self):
        """Initialize energy monitoring"""
        if self.enable_energy_monitoring:
            try:
                from energy_monitor import get_energy_monitor
                self.energy_monitor = get_energy_monitor()
                logger.info("Energy Monitor: Active (target: 95% vector ops, 5% LLM)")
            except Exception as e:
                logger.error(f"Failed to initialize energy monitor: {e}")
                self.energy_monitor = None
        else:
            self.energy_monitor = None
            logger.info("Energy Monitor: Disabled")
    
    # =========================================================================
    # PERSONALITY-DRIVEN CONTENT GENERATION
    # =========================================================================
    
    def generate_daily_smile(self, archetype: Optional[str] = None) -> Dict[str, Any]:
        """Generate a daily smile with friendly archetype
        
        Args:
            archetype: Specific archetype or random if None
            
        Returns:
            Dictionary with smile content
        """
        if not self.personality_engine:
            return {
                'error': 'Personality engine not available',
                'fallback': 'Have a wonderful day! 😊'
            }
        
        result = self.personality_engine.generate_daily_smile(archetype)
        
        # Add mission alignment
        result['mission'] = 'Bringing joy to 8 billion people'
        result['principle'] = 'Service, not profit'
        
        return result
    
    def generate_worldtour_content(self, city_id: str, 
                                   personality: Optional[str] = None,
                                   content_type: Optional[str] = None) -> Dict[str, Any]:
        """Generate World Tour content for a city
        
        Args:
            city_id: City identifier
            personality: Comedian personality (john_cleese, c3po, robin_williams)
            content_type: Type of content to generate
            
        Returns:
            Dictionary with generated content
        """
        if not self.worldtour:
            return {'error': 'World Tour not available'}
        
        import random
        personality = personality or random.choice(self.worldtour.PERSONALITIES)
        content_type = content_type or random.choice(self.worldtour.CONTENT_TYPES)
        
        content = self.worldtour.generate_city_content(
            city_id=city_id,
            personality=personality,
            content_type=content_type,
            track_energy=self.enable_energy_monitoring
        )
        
        # Add mission values
        content['mission'] = 'Bringing smiles to 8 billion people'
        content['bahai_principle'] = 'The earth is but one country, and mankind its citizens'
        
        return content
    
    def generate_comedian_content(self, topic: str, personality: Optional[str] = None,
                                  style_intensity: float = 0.7) -> Dict[str, Any]:
        """Generate content with comedian personality
        
        Args:
            topic: Topic to generate about
            personality: Comedian personality
            style_intensity: Style intensity (0.0-1.0)
            
        Returns:
            Generated content dictionary
        """
        if not self.personality_engine:
            return {'error': 'Personality engine not available'}
        
        content = self.personality_engine.generate_worldtour_content(
            topic=topic,
            personality=personality,
            style_intensity=style_intensity
        )
        
        # Track energy if enabled
        if self.energy_monitor:
            self.energy_monitor.log_vector_operation(
                operation='comedian_content_generation',
                count=1,
                details={'topic': topic, 'personality': personality or 'random'}
            )
        
        return content
    
    # =========================================================================
    # SEMANTIC ANALYSIS & QUALITY CHECKING
    # =========================================================================
    
    def analyze_content_coherence(self, text: str, theme: str) -> Dict[str, Any]:
        """Analyze semantic coherence of content
        
        Args:
            text: Text to analyze
            theme: Theme/topic to check against
            
        Returns:
            Coherence analysis results
        """
        if not self.vector_analyzer:
            return {'error': 'Vector analyzer not available'}
        
        analysis = self.vector_analyzer.analyze_coherence(text, theme)
        
        # Track energy
        if self.energy_monitor:
            self.energy_monitor.log_vector_operation(
                operation='coherence_analysis',
                count=1,
                details={'quality': analysis['quality']}
            )
        
        return analysis
    
    def compare_content_similarity(self, text1: str, text2: str) -> float:
        """Compare semantic similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0.0-1.0)
        """
        if not self.vector_analyzer:
            return 0.0
        
        similarity = self.vector_analyzer.compare_texts(text1, text2)
        
        # Track energy
        if self.energy_monitor:
            self.energy_monitor.log_vector_operation(
                operation='similarity_comparison',
                count=1
            )
        
        return similarity
    
    # =========================================================================
    # WORLD TOUR MANAGEMENT
    # =========================================================================
    
    def get_worldtour_status(self) -> Dict[str, Any]:
        """Get current World Tour status and statistics"""
        if not self.worldtour:
            return {'error': 'World Tour not available'}
        
        stats = self.worldtour.get_stats()
        next_city = self.worldtour.get_next_city()
        
        return {
            'status': 'active',
            'stats': stats,
            'next_city': next_city,
            'personalities': self.worldtour.PERSONALITIES,
            'content_types': self.worldtour.CONTENT_TYPES,
            'mission': 'Touring the world to bring smiles to 8 billion people'
        }
    
    def list_worldtour_cities(self, visited_only: bool = False, limit: Optional[int] = None) -> List[Dict]:
        """List all World Tour cities
        
        Args:
            visited_only: Only return visited cities
            limit: Limit number of results
            
        Returns:
            List of city dictionaries
        """
        if not self.worldtour:
            return []
        
        cities = self.worldtour.list_cities(visited_only=visited_only)
        
        if limit and limit > 0:
            cities = cities[:limit]
        
        return cities
    
    # =========================================================================
    # ENERGY MONITORING & OPTIMIZATION
    # =========================================================================
    
    def get_energy_metrics(self) -> Dict[str, Any]:
        """Get current energy consumption metrics"""
        if not self.energy_monitor:
            return {'error': 'Energy monitoring not enabled'}
        
        return self.energy_monitor.get_metrics()
    
    def get_energy_report(self) -> Dict[str, Any]:
        """Get comprehensive energy efficiency report"""
        if not self.energy_monitor:
            return {'error': 'Energy monitoring not enabled'}
        
        return self.energy_monitor.get_report()
    
    def get_efficiency_score(self) -> float:
        """Get system efficiency score (0-1)
        
        Returns:
            Efficiency score based on vector ops vs LLM calls
            Target: 0.95 (95% vector operations, 5% LLM)
        """
        if not self.energy_monitor:
            return 0.0
        
        return self.energy_monitor.get_efficiency_score()
    
    # =========================================================================
    # MISSION ALIGNMENT
    # =========================================================================
    
    def get_mission_info(self) -> Dict[str, Any]:
        """Get mission and principle information"""
        return {
            'mission': 'Bring personalized daily inspiration to 8 billion people at $0 cost',
            'bahai_principles': {
                'unity': 'Serves all 8 billion people equally, no discrimination',
                'truth': 'Transparent about capabilities and limitations',
                'service': 'Mission-focused, $0 cost, accessible to all',
                'justice': 'Equal access worldwide via CDN edge servers',
                'humility': 'Acknowledges limitations, asks for help when needed'
            },
            'quote': 'The earth is but one country, and mankind its citizens',
            'author': 'Bahá'u'lláh',
            'cost_model': '$0/month - Free for all humanity',
            'target_reach': '8 billion people',
            'current_languages': 8,
            'personality_types': 6  # 3 comedians + 3 archetypes
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        status = {
            'umaja_core': 'operational',
            'subsystems': {
                'personality_engine': 'operational' if self.personality_engine else 'unavailable',
                'worldtour': 'operational' if self.worldtour else 'unavailable',
                'vector_analyzer': 'operational' if self.vector_analyzer else 'unavailable',
                'energy_monitor': 'operational' if self.energy_monitor else 'disabled'
            },
            'mission': self.get_mission_info(),
            'worldtour': self.get_worldtour_status() if self.worldtour else None,
            'energy': self.get_energy_metrics() if self.energy_monitor else None
        }
        
        return status


# Global instance for easy access
_umaja_core = None

def get_umaja_core(enable_energy_monitoring: bool = True) -> UMAJACore:
    """Get or create global UMAJA Core instance"""
    global _umaja_core
    if _umaja_core is None:
        _umaja_core = UMAJACore(enable_energy_monitoring=enable_energy_monitoring)
    return _umaja_core


# Example usage
if __name__ == "__main__":
    print("=== UMAJA Core Integration Test ===\n")
    
    # Initialize
    core = UMAJACore(enable_energy_monitoring=True)
    
    # Get system status
    status = core.get_system_status()
    print("System Status:")
    print(f"  UMAJA Core: {status['umaja_core']}")
    print(f"  Personality Engine: {status['subsystems']['personality_engine']}")
    print(f"  World Tour: {status['subsystems']['worldtour']}")
    print(f"  Vector Analyzer: {status['subsystems']['vector_analyzer']}")
    print(f"  Energy Monitor: {status['subsystems']['energy_monitor']}")
    
    # Generate daily smile
    print("\n=== Daily Smile ===")
    smile = core.generate_daily_smile()
    print(f"Personality: {smile.get('personality')}")
    print(f"Content: {smile.get('content')[:100]}...")
    
    # Generate World Tour content
    print("\n=== World Tour Content ===")
    try:
        content = core.generate_worldtour_content('london', 'john_cleese', 'city_review')
        print(f"City: {content.get('city_name')}")
        print(f"Personality: {content.get('personality')}")
        print(f"Text: {content.get('text')[:100]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Get energy report
    print("\n=== Energy Report ===")
    report = core.get_energy_report()
    if 'error' not in report:
        print(f"Efficiency Score: {report['efficiency']['score']:.2%}")
        print(f"Total Operations: {report['operations']['total']}")
        print(f"Recommendations: {report['recommendations']}")
    
    print("\n✨ UMAJA Core - Service, not profit ✨")
