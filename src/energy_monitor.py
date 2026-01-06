"""
Energy Monitor for UMAJA-Core
Tracks energy consumption and cost metrics as outlined in VECTOR_UNIVERSE_ENERGIE.md
"""

import os
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from dataclasses import dataclass, field, asdict
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnergyMetrics:
    """Energy consumption metrics"""
    cpu_watts: float = 0.0
    ram_watts: float = 0.0
    network_watts: float = 0.0
    total_wh_today: float = 0.0
    total_cost_today: float = 0.0
    co2_kg_today: float = 0.0
    operations_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # Average energy per operation type
    avg_vector_operation_wh: float = 0.0000003  # As per doc: 0.0000003 Wh
    avg_llm_call_wh: float = 0.056  # As per doc: 0.056 Wh
    avg_cdn_serve_wh: float = 0.00000005  # As per doc: 0.00000005 Wh


class EnergyMonitor:
    """
    Monitors energy consumption in real-time
    Implements energy tracking as described in VECTOR_UNIVERSE_ENERGIE.md
    """
    
    # Cost and CO2 constants (configurable via environment)
    COST_PER_KWH = float(os.environ.get('ENERGY_COST_PER_KWH', 0.12))  # $0.12/kWh default
    CO2_PER_KWH = float(os.environ.get('ENERGY_CO2_PER_KWH', 0.45))   # 0.45 kg CO2/kWh default
    
    # Energy constants for operations (as per spec)
    VECTOR_SIMILARITY_WH = 0.0000000003  # Vector similarity check (ultra-efficient)
    SLM_ENCODE_WH = 0.00001              # Small Language Model encode
    LLM_CALL_WH = 0.056                  # LLM API call  
    CACHE_HIT_WH = 0.0000001             # Cached response
    VECTOR_OPERATION_WH = 0.0000003      # Vector operation
    CDN_SERVE_WH = 0.00000005            # CDN file serve
    
    def __init__(self, data_dir: str = "data/monitoring"):
        """Initialize energy monitor
        
        Args:
            data_dir: Directory to store energy logs
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics = EnergyMetrics()
        self.operation_log = []
        
        # Alert thresholds
        self.thresholds = {
            'cpu_watts': 5.0,           # Alert if > 5W
            'daily_cost': 0.10,         # Alert if > $0.10/day
            'daily_wh': 50.0            # Alert if > 50 Wh/day
        }
        
        logger.info("Energy Monitor initialized")
    
    def log_operation(self, operation_type: str, duration_sec: float, 
                     watts: float, details: Optional[Dict[str, Any]] = None):
        """Log an energy-consuming operation
        
        Args:
            operation_type: Type of operation (vector_op, llm_call, cdn_serve, etc.)
            duration_sec: Duration in seconds
            watts: Power consumption in watts
            details: Additional operation details
        """
        # Calculate energy consumption
        wh = (watts * duration_sec) / 3600
        cost = wh * self.COST_PER_KWH / 1000  # Convert Wh to kWh
        co2_kg = wh * self.CO2_PER_KWH / 1000
        
        # Update metrics
        self.metrics.total_wh_today += wh
        self.metrics.total_cost_today += cost
        self.metrics.co2_kg_today += co2_kg
        self.metrics.operations_count += 1
        
        # Log the operation
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'operation_type': operation_type,
            'duration_sec': duration_sec,
            'watts': watts,
            'wh': wh,
            'cost_usd': cost,
            'co2_kg': co2_kg,
            'details': details or {}
        }
        self.operation_log.append(log_entry)
        
        logger.info(f"{operation_type}: {wh:.9f} Wh, ${cost:.9f}, {co2_kg:.9f} kg CO2")
        
        # Check thresholds
        self._check_alerts()
    
    def log_vector_operation(self, operation: str = "similarity_check", 
                            count: int = 1, details: Optional[Dict] = None):
        """Log vector-based operation (ultra-efficient)
        
        Args:
            operation: Type of vector operation
            count: Number of operations
            details: Additional details
        """
        self.log_operation(
            operation_type=f"vector_{operation}",
            duration_sec=0.001 * count,  # ~1ms per operation
            watts=0.0001 * count,
            details={'operation': operation, 'count': count, **(details or {})}
        )
    
    def log_llm_call(self, model: str = "gpt-3.5", tokens: int = 0, 
                    cached: bool = False, details: Optional[Dict] = None):
        """Log LLM API call (energy-intensive)
        
        Args:
            model: LLM model name
            tokens: Number of tokens processed
            cached: Whether result was cached
            details: Additional details
        """
        if cached:
            # Cached response uses much less energy
            self.log_operation(
                operation_type="llm_cached",
                duration_sec=0.01,  # 10ms for cache hit
                watts=0.01,
                details={'model': model, 'tokens': tokens, 'cached': True, **(details or {})}
            )
        else:
            # Full LLM call
            self.log_operation(
                operation_type="llm_call",
                duration_sec=2.0,  # ~2 seconds
                watts=100.0,  # 100W typical
                details={'model': model, 'tokens': tokens, 'cached': False, **(details or {})}
            )
    
    def log_cdn_serve(self, file_size_kb: float = 5.0, cached: bool = True,
                     details: Optional[Dict] = None):
        """Log CDN file serve (ultra-efficient when cached)
        
        Args:
            file_size_kb: Size of file in KB
            cached: Whether served from CDN cache
            details: Additional details
        """
        if cached:
            # CDN edge cache hit
            self.log_operation(
                operation_type="cdn_cached",
                duration_sec=0.005,  # 5ms
                watts=0.1,
                details={'file_size_kb': file_size_kb, 'cached': True, **(details or {})}
            )
        else:
            # Origin server fetch
            self.log_operation(
                operation_type="cdn_origin",
                duration_sec=0.05,  # 50ms
                watts=1.0,
                details={'file_size_kb': file_size_kb, 'cached': False, **(details or {})}
            )
    
    def log_slm_encode(self, text_length: int = 100, details: Optional[Dict] = None):
        """Log small language model encoding operation
        
        Args:
            text_length: Length of text encoded
            details: Additional details
        """
        self.log_operation(
            operation_type="slm_encode",
            duration_sec=0.01,  # 10ms typical
            watts=1.0,  # 1W typical
            details={'text_length': text_length, **(details or {})}
        )
    
    def log_vector_similarity(self, count: int = 1, details: Optional[Dict] = None):
        """Log vector similarity calculation (ultra-efficient)
        
        Args:
            count: Number of similarity calculations
            details: Additional details
        """
        self.log_operation(
            operation_type="vector_similarity",
            duration_sec=0.00001 * count,  # 10 microseconds per calculation
            watts=0.001 * count,
            details={'count': count, **(details or {})}
        )
    
    def _check_alerts(self):
        """Check if any thresholds are exceeded"""
        alerts = []
        
        if self.metrics.cpu_watts > self.thresholds['cpu_watts']:
            alerts.append(f"⚠️  CPU usage > {self.thresholds['cpu_watts']}W: Consider agent sleep")
        
        if self.metrics.total_cost_today > self.thresholds['daily_cost']:
            alerts.append(f"⚠️  Daily cost > ${self.thresholds['daily_cost']}: Check for inefficiencies")
        
        if self.metrics.total_wh_today > self.thresholds['daily_wh']:
            alerts.append(f"⚠️  Energy > {self.thresholds['daily_wh']} Wh: Optimize operations")
        
        for alert in alerts:
            logger.warning(alert)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current energy metrics"""
        return asdict(self.metrics)
    
    def get_efficiency_score(self) -> float:
        """Calculate efficiency score (0-1, higher is better)
        
        Based on ratio of vector operations to LLM calls
        Target: 95% vector operations, 5% LLM calls
        """
        if self.metrics.operations_count == 0:
            return 1.0
        
        # Count operation types
        vector_ops = sum(1 for log in self.operation_log 
                        if log['operation_type'].startswith('vector_'))
        llm_ops = sum(1 for log in self.operation_log 
                     if log['operation_type'].startswith('llm_'))
        
        total_ops = len(self.operation_log)
        vector_ratio = vector_ops / total_ops if total_ops > 0 else 0
        
        # Score based on how close we are to 95% vector operations
        target_ratio = 0.95
        score = 1.0 - abs(vector_ratio - target_ratio)
        
        return max(0.0, min(1.0, score))
    
    def get_report(self) -> Dict[str, Any]:
        """Generate comprehensive energy report"""
        efficiency_score = self.get_efficiency_score()
        
        # Calculate savings vs traditional approach
        traditional_energy = self.metrics.operations_count * self.LLM_CALL_WH
        actual_energy = self.metrics.total_wh_today
        savings_percent = ((traditional_energy - actual_energy) / traditional_energy * 100) if traditional_energy > 0 else 0
        
        return {
            'metrics': self.get_metrics(),
            'efficiency': {
                'score': efficiency_score,
                'rating': 'excellent' if efficiency_score > 0.9 else 'good' if efficiency_score > 0.7 else 'fair',
                'savings_vs_traditional_percent': savings_percent
            },
            'operations': {
                'total': self.metrics.operations_count,
                'vector_operations': sum(1 for log in self.operation_log if log['operation_type'].startswith('vector_')),
                'llm_calls': sum(1 for log in self.operation_log if log['operation_type'].startswith('llm_')),
                'cdn_serves': sum(1 for log in self.operation_log if log['operation_type'].startswith('cdn_'))
            },
            'recommendations': self._get_recommendations()
        }
    
    def _get_recommendations(self) -> list:
        """Get optimization recommendations"""
        recommendations = []
        
        efficiency = self.get_efficiency_score()
        if efficiency < 0.8:
            recommendations.append("Increase vector operations, reduce LLM calls")
        
        if self.metrics.total_cost_today > self.thresholds['daily_cost'] * 0.8:
            recommendations.append("Approaching cost threshold - consider caching")
        
        if self.metrics.cpu_watts > self.thresholds['cpu_watts'] * 0.8:
            recommendations.append("High CPU usage - enable agent sleep mode")
        
        if not recommendations:
            recommendations.append("✅ All systems running optimally!")
        
        return recommendations
    
    def save_daily_report(self):
        """Save daily report to file"""
        report = self.get_report()
        date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        report_path = self.data_dir / f"energy_report_{date_str}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Daily energy report saved to {report_path}")
        
        return report_path
    
    def reset_daily_metrics(self):
        """Reset daily metrics (call at midnight)"""
        # Save report before reset
        self.save_daily_report()
        
        # Reset metrics
        self.metrics = EnergyMetrics()
        self.operation_log = []
        
        logger.info("Daily metrics reset")


# Global instance for easy access
_energy_monitor = None

def get_energy_monitor() -> EnergyMonitor:
    """Get or create global energy monitor instance"""
    global _energy_monitor
    if _energy_monitor is None:
        _energy_monitor = EnergyMonitor()
    return _energy_monitor


# Example usage
if __name__ == "__main__":
    monitor = EnergyMonitor()
    
    print("=== Energy Monitor Test ===\n")
    
    # Simulate operations
    print("Simulating 95 vector operations...")
    for i in range(95):
        monitor.log_vector_operation("similarity_check")
    
    print("\nSimulating 5 LLM calls...")
    for i in range(5):
        monitor.log_llm_call("gpt-3.5", tokens=500)
    
    print("\nSimulating 100 CDN serves...")
    for i in range(100):
        monitor.log_cdn_serve(file_size_kb=5.0, cached=True)
    
    # Get report
    report = monitor.get_report()
    
    print("\n=== Energy Report ===")
    print(f"Total Operations: {report['operations']['total']}")
    print(f"Efficiency Score: {report['efficiency']['score']:.2%}")
    print(f"Savings vs Traditional: {report['efficiency']['savings_vs_traditional_percent']:.2f}%")
    print(f"Total Energy: {report['metrics']['total_wh_today']:.6f} Wh")
    print(f"Total Cost: ${report['metrics']['total_cost_today']:.9f}")
    print(f"CO2: {report['metrics']['co2_kg_today']:.9f} kg")
    print("\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  - {rec}")
