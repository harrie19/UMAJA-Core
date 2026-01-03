#!/usr/bin/env python3
"""
📊 UMAJA Autonomous Mode Dashboard
Real-time monitoring and status display for autonomous agent system

This script:
- Displays real-time status of all agents
- Shows task queue length and completion rate
- Displays system metrics (uptime, tasks completed, failures)
- Shows current city in World Tour
- Displays content generation statistics
- Provides agent health status
- Shows recent errors and recovery actions
- Exports status as JSON for API consumption

Usage:
    python scripts/autonomous_dashboard.py [--json] [--watch]
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class AutonomousDashboard:
    """
    Dashboard for monitoring autonomous agent system
    """
    
    def __init__(self):
        """Initialize dashboard"""
        self.data_dir = Path("data/agents")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.data_dir / "orchestrator_state.json"
        self.log_file = self.data_dir / "autonomous_mode.log"
    
    def load_state(self) -> Dict:
        """Load current system state"""
        if not self.state_file.exists():
            return {
                "stats": {
                    "total_agents": 0,
                    "active_agents": 0,
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "failed_tasks": 0,
                    "started_at": None
                },
                "agents": {},
                "saved_at": None
            }
        
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading state: {e}")
            return {"stats": {}, "agents": {}, "saved_at": None}
    
    def get_worldtour_status(self) -> Dict:
        """Get World Tour status"""
        worldtour_file = Path("data/worldtour_cities.json")
        
        if not worldtour_file.exists():
            return {
                "current_city": "Unknown",
                "cities_visited": 0,
                "total_cities": 0,
                "completion_percentage": 0
            }
        
        try:
            with open(worldtour_file, 'r') as f:
                data = json.load(f)
                cities = data.get('cities', [])
                visited = [c for c in cities if c.get('visited', False)]
                
                current_city = "Not started"
                if visited:
                    current_city = visited[-1].get('name', 'Unknown')
                
                return {
                    "current_city": current_city,
                    "cities_visited": len(visited),
                    "total_cities": len(cities),
                    "completion_percentage": (len(visited) / len(cities) * 100) if cities else 0
                }
        except Exception as e:
            print(f"Error loading worldtour status: {e}")
            return {
                "current_city": "Error",
                "cities_visited": 0,
                "total_cities": 0,
                "completion_percentage": 0
            }
    
    def get_recent_errors(self, max_lines: int = 10) -> List[str]:
        """Get recent errors from log file"""
        if not self.log_file.exists():
            return []
        
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                error_lines = [line for line in lines if 'ERROR' in line]
                return error_lines[-max_lines:]
        except Exception as e:
            return [f"Error reading logs: {e}"]
    
    def calculate_uptime(self, started_at: str) -> str:
        """Calculate system uptime"""
        if not started_at:
            return "Not running"
        
        try:
            start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            uptime = datetime.utcnow() - start_time
            
            days = uptime.days
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        except:
            return "Unknown"
    
    def check_emergency_stop(self) -> Dict:
        """Check emergency stop status"""
        emergency_file = Path(".github/emergency_stop.json")
        
        if not emergency_file.exists():
            return {
                "enabled": True,
                "reason": None,
                "stopped_at": None
            }
        
        try:
            with open(emergency_file, 'r') as f:
                config = json.load(f)
                return {
                    "enabled": config.get('agent_enabled', True),
                    "reason": config.get('reason'),
                    "stopped_at": config.get('disabled_by')
                }
        except Exception as e:
            return {
                "enabled": True,
                "reason": f"Error reading config: {e}",
                "stopped_at": None
            }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all dashboard data"""
        state = self.load_state()
        stats = state.get('stats', {})
        agents = state.get('agents', {})
        
        # Calculate metrics
        completion_rate = (
            stats.get('completed_tasks', 0) / stats.get('total_tasks', 1) * 100
            if stats.get('total_tasks', 0) > 0 else 0
        )
        
        failure_rate = (
            stats.get('failed_tasks', 0) / stats.get('total_tasks', 1) * 100
            if stats.get('total_tasks', 0) > 0 else 0
        )
        
        # Agent health
        agent_health = {}
        for agent_id, agent_data in agents.items():
            status = agent_data.get('status', 'unknown')
            health = "healthy" if status in ["idle", "working"] else "unhealthy"
            agent_health[agent_id] = {
                "status": status,
                "health": health,
                "tasks_completed": agent_data.get('tasks_completed', 0),
                "tasks_failed": agent_data.get('tasks_failed', 0)
            }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system_status": {
                "uptime": self.calculate_uptime(stats.get('started_at')),
                "total_agents": stats.get('total_agents', 0),
                "active_agents": stats.get('active_agents', 0),
                "started_at": stats.get('started_at')
            },
            "task_metrics": {
                "total_tasks": stats.get('total_tasks', 0),
                "completed_tasks": stats.get('completed_tasks', 0),
                "failed_tasks": stats.get('failed_tasks', 0),
                "completion_rate": round(completion_rate, 2),
                "failure_rate": round(failure_rate, 2)
            },
            "agents": agent_health,
            "worldtour": self.get_worldtour_status(),
            "emergency_stop": self.check_emergency_stop(),
            "recent_errors": self.get_recent_errors(5),
            "last_state_save": state.get('saved_at')
        }
    
    def display_dashboard(self, data: Dict):
        """Display dashboard in terminal"""
        print("\033[2J\033[H")  # Clear screen
        print("=" * 80)
        print("🤖 UMAJA AUTONOMOUS MODE DASHBOARD")
        print("=" * 80)
        print()
        
        # System Status
        system = data['system_status']
        print("📊 SYSTEM STATUS")
        print("-" * 80)
        print(f"Uptime:        {system['uptime']}")
        print(f"Total Agents:  {system['total_agents']}")
        print(f"Active Agents: {system['active_agents']}")
        print(f"Started At:    {system['started_at'] or 'Not running'}")
        print()
        
        # Task Metrics
        metrics = data['task_metrics']
        print("📈 TASK METRICS")
        print("-" * 80)
        print(f"Total Tasks:      {metrics['total_tasks']}")
        print(f"Completed:        {metrics['completed_tasks']} ({metrics['completion_rate']:.1f}%)")
        print(f"Failed:           {metrics['failed_tasks']} ({metrics['failure_rate']:.1f}%)")
        print()
        
        # World Tour Status
        worldtour = data['worldtour']
        print("🌍 WORLD TOUR STATUS")
        print("-" * 80)
        print(f"Current City:     {worldtour['current_city']}")
        print(f"Cities Visited:   {worldtour['cities_visited']}/{worldtour['total_cities']}")
        print(f"Completion:       {worldtour['completion_percentage']:.1f}%")
        print()
        
        # Agent Health
        print("🏥 AGENT HEALTH")
        print("-" * 80)
        agents = data['agents']
        if agents:
            healthy_count = sum(1 for a in agents.values() if a['health'] == 'healthy')
            print(f"Healthy: {healthy_count}/{len(agents)}")
            print()
            
            # Show top 5 agents by tasks completed
            sorted_agents = sorted(
                agents.items(),
                key=lambda x: x[1]['tasks_completed'],
                reverse=True
            )[:5]
            
            for agent_id, agent_data in sorted_agents:
                health_icon = "✅" if agent_data['health'] == 'healthy' else "❌"
                print(f"{health_icon} {agent_id[:30]:<30} | "
                      f"Status: {agent_data['status']:<10} | "
                      f"Completed: {agent_data['tasks_completed']:>4} | "
                      f"Failed: {agent_data['tasks_failed']:>2}")
        else:
            print("No agents found")
        print()
        
        # Emergency Stop Status
        emergency = data['emergency_stop']
        print("🚨 EMERGENCY STOP")
        print("-" * 80)
        if emergency['enabled']:
            print("✅ System is ENABLED and running")
        else:
            print(f"❌ System is DISABLED")
            if emergency['reason']:
                print(f"Reason: {emergency['reason']}")
            if emergency['stopped_at']:
                print(f"Stopped by: {emergency['stopped_at']}")
        print()
        
        # Recent Errors
        errors = data['recent_errors']
        if errors:
            print("⚠️  RECENT ERRORS")
            print("-" * 80)
            for error in errors[-3:]:  # Show last 3 errors
                print(error.strip()[:80])
            print()
        
        # Footer
        print("=" * 80)
        print(f"Last Updated: {data['timestamp']}")
        print("Press Ctrl+C to exit")
        print("=" * 80)
    
    def export_json(self) -> str:
        """Export dashboard data as JSON"""
        data = self.get_dashboard_data()
        return json.dumps(data, indent=2)
    
    def watch_mode(self, refresh_interval: int = 5):
        """
        Watch mode - continuously refresh dashboard
        
        Args:
            refresh_interval: Seconds between refreshes
        """
        try:
            while True:
                data = self.get_dashboard_data()
                self.display_dashboard(data)
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print()
            print("Dashboard stopped")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="📊 UMAJA Autonomous Mode Dashboard"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON instead of dashboard view'
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Continuously refresh dashboard (default: single snapshot)'
    )
    parser.add_argument(
        '--refresh',
        type=int,
        default=5,
        help='Refresh interval in seconds for watch mode (default: 5)'
    )
    
    args = parser.parse_args()
    
    dashboard = AutonomousDashboard()
    
    if args.json:
        # JSON output mode
        print(dashboard.export_json())
    elif args.watch:
        # Watch mode
        dashboard.watch_mode(refresh_interval=args.refresh)
    else:
        # Single snapshot
        data = dashboard.get_dashboard_data()
        dashboard.display_dashboard(data)


if __name__ == "__main__":
    main()
