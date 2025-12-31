"""
UMAJA Automation Test Suite
Comprehensive tests for world tour automation components
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import datetime
import json


def test_world_tour_automation():
    """Test world tour automation orchestrator"""
    print("\n🧪 Testing World Tour Automation...")
    
    from world_tour_automation import WorldTourAutomation
    
    automation = WorldTourAutomation()
    
    # Test small batch generation
    result = automation.generate_global_launch(
        launch_date=datetime(2026, 1, 1),
        cities=['new_york', 'london'],
        languages=['en'],
        platforms=['tiktok']
    )
    
    assert result['total_posts'] == 2, "Should generate 2 posts (2 cities × 1 lang × 1 platform)"
    assert result['content_ready'] is True, "Content should be ready"
    assert result['schedule_created'] is True, "Schedule should be created"
    assert result['qa_passed'] is True, "QA should pass"
    
    print("✅ World Tour Automation test passed")
    return True


def test_batch_content_generator():
    """Test batch content generator"""
    print("\n🧪 Testing Batch Content Generator...")
    
    from batch_content_generator import BatchContentGenerator
    
    generator = BatchContentGenerator(max_workers=2)
    
    # Test batch generation
    batch = generator.generate_city_batch(
        cities=['new_york', 'london'],
        languages=['en'],
        platforms=['tiktok'],
        parallel=True
    )
    
    assert 'new_york' in batch, "Should have New York content"
    assert 'london' in batch, "Should have London content"
    assert batch['new_york']['quality_score'] > 0, "Should have quality score"
    
    # Test variations
    variations = generator.generate_with_variations('new_york', count=3)
    assert len(variations) == 3, "Should generate 3 variations"
    assert variations[0]['engagement_score'] >= variations[-1]['engagement_score'], \
        "Should be sorted by engagement score"
    
    print("✅ Batch Content Generator test passed")
    return True


def test_smart_scheduler():
    """Test smart scheduler"""
    print("\n🧪 Testing Smart Scheduler...")
    
    from smart_scheduler import SmartScheduler
    
    scheduler = SmartScheduler()
    
    # Test optimal time calculation
    optimal_time = scheduler.calculate_optimal_time('tokyo', 'tiktok')
    assert optimal_time is not None, "Should calculate optimal time"
    
    # Test schedule creation
    mock_batch = {
        'new_york': {
            'city_name': 'New York',
            'platforms': {'tiktok': {}, 'instagram': {}}
        }
    }
    
    schedule = scheduler.create_global_schedule(mock_batch)
    assert schedule['total_posts'] == 2, "Should schedule 2 posts"
    assert 'posts' in schedule, "Should have posts list"
    assert 'timeline' in schedule, "Should have timeline"
    
    # Test backup schedule
    backup = scheduler.calculate_backup_schedule(schedule)
    assert len(backup['posts']) == 2, "Should have backup for all posts"
    
    print("✅ Smart Scheduler test passed")
    return True


def test_quality_assurance():
    """Test quality assurance system"""
    print("\n🧪 Testing Quality Assurance...")
    
    from quality_assurance import QualityAssurance
    
    qa = QualityAssurance()
    
    # Test validation
    test_batch = {
        'new_york': {
            'platforms': {
                'tiktok': {
                    'content': 'Great content about New York!',
                    'hashtags': ['#NYC', '#Travel']
                }
            },
            'languages': {
                'en': 'English content'
            }
        }
    }
    
    results = qa.validate_content_batch(test_batch)
    assert results['passed'] > 0, "Should have passing content"
    assert results['safe_to_launch'] is True, "Should be safe to launch"
    
    # Test cultural safety
    safety = qa.cultural_safety_check('Hello world', 'en')
    assert safety['safe'] is True, "Should be culturally safe"
    
    # Test auto-fix
    bad_batch = {
        'test': {
            'platforms': {
                'tiktok': {
                    'content': 'A' * 200,  # Too long
                    'hashtags': []  # Missing
                }
            }
        }
    }
    
    bad_results = qa.validate_content_batch(bad_batch)
    fixed_batch = qa.auto_fix_issues(bad_batch, bad_results['issues'])
    assert fixed_batch is not None, "Should auto-fix issues"
    
    print("✅ Quality Assurance test passed")
    return True


def test_launch_day_monitor():
    """Test launch day monitor"""
    print("\n🧪 Testing Launch Day Monitor...")
    
    from launch_day_monitor import LaunchDayMonitor
    
    monitor = LaunchDayMonitor()
    
    # Test dashboard creation
    test_data = {
        'total_posts': 100,
        'cities': 10,
        'languages': 5,
        'platforms': 2
    }
    
    dashboard = monitor.create_realtime_dashboard(test_data)
    assert dashboard.endswith('.html'), "Should create HTML dashboard"
    assert Path(dashboard).exists(), "Dashboard file should exist"
    
    # Test metrics tracking
    metrics = monitor.track_metrics(test_data)
    assert 'timestamp' in metrics, "Should have timestamp"
    assert 'total_reach' in metrics, "Should track reach"
    
    # Test alerts
    monitor.send_alerts('test_alert', {'test': 'data'})
    alert_file = Path('output/monitoring/alerts.jsonl')
    assert alert_file.exists(), "Should create alert log"
    
    print("✅ Launch Day Monitor test passed")
    return True


def test_compilation_generator():
    """Test compilation generator"""
    print("\n🧪 Testing Compilation Generator...")
    
    from compilation_generator import CompilationGenerator
    
    generator = CompilationGenerator()
    
    # Test recap creation
    test_batch = {
        'new_york': {
            'city_name': 'New York',
            'quality_score': 0.95
        },
        'london': {
            'city_name': 'London',
            'quality_score': 0.92
        }
    }
    
    recap = generator.create_launch_day_recap('2026-01-01', test_batch)
    assert recap['cities_count'] == 2, "Should include both cities"
    assert recap['duration_seconds'] == 60, "Should be 60 seconds"
    
    # Test top moments
    top = generator.create_top_moments(7, test_batch)
    assert 'clips' in top, "Should have clips"
    
    print("✅ Compilation Generator test passed")
    return True


def test_performance_optimizer():
    """Test performance optimizer"""
    print("\n🧪 Testing Performance Optimizer...")
    
    from performance_optimizer import PerformanceOptimizer
    import time
    
    optimizer = PerformanceOptimizer()
    
    # Test caching
    optimizer.cache_everything('test_key', 'test_value')
    cached = optimizer.cache_everything('test_key')
    assert cached == 'test_value', "Should retrieve cached value"
    
    # Test parallel processing
    def mock_task(task):
        time.sleep(0.01)
        return {'result': task['id']}
    
    tasks = [{'id': i} for i in range(10)]
    results = optimizer.parallel_processing(tasks, mock_task, max_workers=3)
    assert len(results) == 10, "Should process all tasks"
    
    # Test cache stats
    stats = optimizer.get_cache_stats()
    assert stats['hits'] > 0, "Should have cache hits"
    
    print("✅ Performance Optimizer test passed")
    return True


def test_safety_system():
    """Test safety system"""
    print("\n🧪 Testing Safety System...")
    
    from safety_system import SafetySystem
    
    safety = SafetySystem()
    
    # Test dry run
    test_data = {
        'total_posts': 10,
        'cities': 2,
        'languages': 1,
        'platforms': 1
    }
    
    simulation = safety.dry_run_mode('test_action', test_data)
    assert simulation['mode'] == 'dry_run', "Should be dry run mode"
    assert 'would_affect' in simulation, "Should analyze impact"
    
    # Test safety validation
    launch_data = {
        'content_batch': {},
        'schedule': {}
    }
    
    checks = safety.validate_safety_checks(launch_data)
    assert 'content_validated' in checks, "Should validate content"
    assert 'emergency_stop_ready' in checks, "Should check emergency stop"
    
    # Test emergency stop
    stop = safety.emergency_stop('test_stop')
    assert stop['activated'] is True, "Should activate emergency stop"
    
    print("✅ Safety System test passed")
    return True


def run_all_tests():
    """Run all automation tests"""
    print("=" * 70)
    print("🧪 UMAJA AUTOMATION TEST SUITE")
    print("=" * 70)
    
    tests = [
        test_world_tour_automation,
        test_batch_content_generator,
        test_smart_scheduler,
        test_quality_assurance,
        test_launch_day_monitor,
        test_compilation_generator,
        test_performance_optimizer,
        test_safety_system
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n❌ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
