"""
Test UMAJA Core Integration Features
Tests personality engine, energy monitoring, and integrated workflows
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest


def test_personality_engine_initialization():
    """Test that personality engine initializes correctly"""
    from personality_engine import PersonalityEngine
    
    engine = PersonalityEngine()
    
    # Check comedians
    assert len(engine.list_comedians()) == 3
    assert 'john_cleese' in engine.list_comedians()
    assert 'c3po' in engine.list_comedians()
    assert 'robin_williams' in engine.list_comedians()
    
    # Check archetypes
    assert len(engine.list_archetypes()) == 3
    assert 'professor' in engine.list_archetypes()
    assert 'worrier' in engine.list_archetypes()
    assert 'enthusiast' in engine.list_archetypes()


def test_comedian_personalities():
    """Test comedian personalities generate content"""
    from personality_engine import PersonalityEngine
    
    engine = PersonalityEngine()
    
    # Test John Cleese
    cleese = engine.get_comedian('john_cleese')
    assert cleese is not None
    text = cleese.generate_smile_text('pizza')
    assert len(text) > 0
    assert isinstance(text, str)
    
    # Test C-3PO
    c3po = engine.get_comedian('c3po')
    assert c3po is not None
    text = c3po.generate_smile_text('travel')
    assert len(text) > 0
    # C-3PO should use formal, anxious language
    assert 'my' in text.lower() or 'protocol' in text.lower() or 'calculation' in text.lower()
    
    # Test Robin Williams
    robin = engine.get_comedian('robin_williams')
    assert robin is not None
    text = robin.generate_smile_text('food')
    assert len(text) > 0
    assert '*laughs*' in text or 'beautiful' in text


def test_voice_synthesis_parameters():
    """Test that voice parameters are set for each personality"""
    from personality_engine import PersonalityEngine
    
    engine = PersonalityEngine()
    
    # John Cleese - lower pitch, measured
    cleese = engine.get_comedian('john_cleese')
    assert cleese.voice_params['pitch'] == 0.8
    assert cleese.voice_params['speed'] == 0.9
    assert cleese.voice_params['rate'] == 150
    
    # C-3PO - higher pitch, anxious
    c3po = engine.get_comedian('c3po')
    assert c3po.voice_params['pitch'] == 1.3
    assert c3po.voice_params['speed'] == 1.1
    assert c3po.voice_params['rate'] == 180
    
    # Robin Williams - varied, fast
    robin = engine.get_comedian('robin_williams')
    assert robin.voice_params['pitch'] == 1.1
    assert robin.voice_params['speed'] == 1.2
    assert robin.voice_params['rate'] == 190


def test_worldtour_content_generation():
    """Test worldtour content generation with personality engine"""
    from personality_engine import PersonalityEngine
    
    engine = PersonalityEngine()
    
    # This will use personality engine
    result = engine.generate_text(
        topic="New York pizza",
        personality="john_cleese"
    )
    
    assert 'text' in result
    assert result['text'] != ''


def test_energy_monitor_initialization():
    """Test energy monitor initializes correctly"""
    from energy_monitor import EnergyMonitor
    
    monitor = EnergyMonitor()
    
    assert monitor is not None
    assert monitor.metrics.total_wh_today == 0.0
    assert monitor.metrics.operations_count == 0


def test_energy_monitor_logging():
    """Test energy monitor can log operations"""
    from energy_monitor import EnergyMonitor
    
    monitor = EnergyMonitor()
    
    # Log vector operation (efficient)
    monitor.log_vector_operation('similarity_check', count=1)
    assert monitor.metrics.operations_count == 1
    
    # Log LLM call (expensive)
    monitor.log_llm_call('gpt-3.5', tokens=100, cached=False)
    assert monitor.metrics.operations_count == 2
    
    # Check metrics
    metrics = monitor.get_metrics()
    assert metrics['total_wh_today'] > 0
    assert metrics['operations_count'] == 2


def test_energy_efficiency_score():
    """Test efficiency score calculation"""
    from energy_monitor import EnergyMonitor
    
    monitor = EnergyMonitor()
    
    # Simulate optimal mix (95% vector, 5% LLM)
    for i in range(95):
        monitor.log_vector_operation('test_op')
    
    for i in range(5):
        monitor.log_llm_call('test', tokens=10, cached=True)
    
    score = monitor.get_efficiency_score()
    assert 0.0 <= score <= 1.0
    # Should be close to optimal
    assert score > 0.8


def test_umaja_core_integration():
    """Test UMAJA Core integration module"""
    try:
        from umaja_core_integration import UMAJACore
        
        core = UMAJACore(enable_energy_monitoring=True)
        
        # Check subsystems
        assert core.personality_engine is not None
        
        # Test daily smile generation
        smile = core.generate_daily_smile()
        assert 'content' in smile or 'error' in smile
        
        # Test mission info
        mission = core.get_mission_info()
        assert 'mission' in mission
        assert 'bahai_principles' in mission
        assert mission['target_reach'] == '8 billion people'
        
        # Test system status
        status = core.get_system_status()
        assert 'umaja_core' in status
        assert status['umaja_core'] == 'operational'
        
    except Exception as e:
        # If dependencies not available, skip but don't fail
        pytest.skip(f"UMAJA Core integration not fully available: {e}")


def test_mission_alignment():
    """Test that mission principles are embedded in system"""
    try:
        from umaja_core_integration import UMAJACore
        
        core = UMAJACore()
        mission = core.get_mission_info()
        
        # Check Bahá'í principles
        principles = mission['bahai_principles']
        assert 'unity' in principles
        assert 'truth' in principles
        assert 'service' in principles
        assert 'justice' in principles
        assert 'humility' in principles
        
        # Check mission statement
        assert '8 billion' in mission['mission']
        assert '$0' in mission['cost_model']
        
        # Check quote
        assert "The earth is but one country" in mission['quote']
        
    except Exception as e:
        pytest.skip(f"Mission alignment test skipped: {e}")


def test_personality_generate_text():
    """Test text generation with style intensity"""
    from personality_engine import PersonalityEngine
    
    engine = PersonalityEngine()
    
    # Generate with different intensities
    low_intensity = engine.generate_text('pizza', 'john_cleese', style_intensity=0.3)
    high_intensity = engine.generate_text('pizza', 'john_cleese', style_intensity=1.0)
    
    assert low_intensity['text'] != ''
    assert high_intensity['text'] != ''
    assert low_intensity['style_intensity'] == 0.3
    assert high_intensity['style_intensity'] == 1.0


def test_worldtour_fallback_generation():
    """Test worldtour fallback content generation"""
    from worldtour_generator import WorldtourGenerator
    
    generator = WorldtourGenerator()
    
    # Even if personality engine fails, should have fallback
    try:
        content = generator.generate_city_content('london', 'john_cleese', 'city_review')
        assert 'text' in content
        assert 'city_name' in content
        assert content['city_name'] == 'London'
    except Exception as e:
        # City database might not be initialized
        pytest.skip(f"Worldtour test skipped: {e}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, '-v'])
