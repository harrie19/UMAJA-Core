"""
Test Energy Monitor
Tests for energy tracking, new methods, and energy constants
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from energy_monitor import EnergyMonitor


def test_energy_monitor_initialization():
    """Test that energy monitor initializes correctly"""
    monitor = EnergyMonitor()
    
    # Check constants
    assert monitor.VECTOR_OPERATION_WH == 0.0000003
    assert monitor.VECTOR_SIMILARITY_WH == 0.0000003
    assert monitor.SLM_ENCODE_WH == 0.00001
    assert monitor.CACHE_HIT_WH == 0.0000001
    assert monitor.LLM_CALL_WH == 0.056
    
    # Check initial metrics
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 0
    assert metrics['total_wh_today'] == 0.0


def test_log_vector_similarity_single_operation():
    """Test logging a single vector similarity operation"""
    monitor = EnergyMonitor()
    
    # Log 1 operation
    monitor.log_vector_similarity(count=1)
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 1
    
    # Expected energy: 1 * 0.0000003 Wh
    expected_wh = 0.0000003
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-10


def test_log_vector_similarity_multiple_operations():
    """Test logging multiple vector similarity operations"""
    monitor = EnergyMonitor()
    
    # Log 5 operations
    monitor.log_vector_similarity(count=5)
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 1  # 1 log entry
    
    # Expected energy: 5 * 0.0000003 Wh = 0.0000015 Wh
    expected_wh = 5 * 0.0000003
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-10


def test_log_vector_similarity_with_details():
    """Test logging vector similarity with custom details"""
    monitor = EnergyMonitor()
    
    details = {'model': 'all-MiniLM-L6-v2', 'batch_size': 10}
    monitor.log_vector_similarity(count=10, details=details)
    
    # Check that details are stored
    assert len(monitor.operation_log) == 1
    log_entry = monitor.operation_log[0]
    assert log_entry['operation_type'] == 'vector_similarity'
    assert log_entry['details']['count'] == 10
    assert log_entry['details']['model'] == 'all-MiniLM-L6-v2'
    assert log_entry['details']['batch_size'] == 10


def test_log_slm_encode_short_text():
    """Test logging SLM encode for short text (< 100 chars)"""
    monitor = EnergyMonitor()
    
    # Log encoding of 50 characters (should be 1 encoding)
    monitor.log_slm_encode(text_length=50)
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 1
    
    # Expected energy: 1 * 0.00001 Wh
    expected_wh = 0.00001
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-10


def test_log_slm_encode_medium_text():
    """Test logging SLM encode for medium text"""
    monitor = EnergyMonitor()
    
    # Log encoding of 250 characters (should be 2 encodings)
    monitor.log_slm_encode(text_length=250)
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 1  # 1 log entry
    
    # Expected energy: 2 * 0.00001 Wh = 0.00002 Wh
    expected_wh = 2 * 0.00001
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-10


def test_log_slm_encode_long_text():
    """Test logging SLM encode for long text"""
    monitor = EnergyMonitor()
    
    # Log encoding of 1000 characters (should be 10 encodings)
    monitor.log_slm_encode(text_length=1000)
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 1
    
    # Expected energy: 10 * 0.00001 Wh = 0.0001 Wh
    expected_wh = 10 * 0.00001
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-10


def test_log_slm_encode_with_details():
    """Test logging SLM encode with custom details"""
    monitor = EnergyMonitor()
    
    details = {'text': 'sample text', 'language': 'en'}
    monitor.log_slm_encode(text_length=150, details=details)
    
    # Check that details are stored
    assert len(monitor.operation_log) == 1
    log_entry = monitor.operation_log[0]
    assert log_entry['operation_type'] == 'slm_encode'
    assert log_entry['details']['text_length'] == 150
    assert log_entry['details']['encoding_count'] == 1
    assert log_entry['details']['text'] == 'sample text'
    assert log_entry['details']['language'] == 'en'


def test_combined_energy_tracking():
    """Test tracking multiple types of operations"""
    monitor = EnergyMonitor()
    
    # Log various operations
    monitor.log_vector_similarity(count=3)  # 3 * 0.0000003 = 0.0000009 Wh
    monitor.log_slm_encode(text_length=500)  # 5 * 0.00001 = 0.00005 Wh
    monitor.log_vector_similarity(count=2)  # 2 * 0.0000003 = 0.0000006 Wh
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 3
    
    # Expected total energy
    expected_wh = (3 * 0.0000003) + (5 * 0.00001) + (2 * 0.0000003)
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-10


def test_energy_calculations_precision():
    """Test that energy calculations maintain precision"""
    monitor = EnergyMonitor()
    
    # Log 100 small operations
    for _ in range(100):
        monitor.log_vector_similarity(count=1)
    
    metrics = monitor.get_metrics()
    assert metrics['operations_count'] == 100
    
    # Expected energy: 100 * 0.0000003 Wh = 0.00003 Wh
    expected_wh = 100 * 0.0000003
    assert abs(metrics['total_wh_today'] - expected_wh) < 1e-9


def test_operation_log_entries():
    """Test that operations are properly logged"""
    monitor = EnergyMonitor()
    
    monitor.log_vector_similarity(count=5)
    monitor.log_slm_encode(text_length=200)
    
    # Check operation log
    assert len(monitor.operation_log) == 2
    
    # First entry
    entry1 = monitor.operation_log[0]
    assert entry1['operation_type'] == 'vector_similarity'
    assert 'timestamp' in entry1
    assert 'duration_sec' in entry1
    assert 'watts' in entry1
    assert 'wh' in entry1
    assert 'cost_usd' in entry1
    assert 'co2_kg' in entry1
    
    # Second entry
    entry2 = monitor.operation_log[1]
    assert entry2['operation_type'] == 'slm_encode'
    assert 'timestamp' in entry2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
