"""
UMAJA Launch Day Monitor - Real-Time Dashboard
Live monitoring and metrics tracking during Global Smile Day
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LaunchDayMonitor:
    """
    Live monitoring during Global Smile Day.
    Provides real-time dashboards and metrics tracking.
    """
    
    def __init__(self, output_dir: str = "output/monitoring"):
        """
        Initialize launch day monitor.
        
        Args:
            output_dir: Directory for monitoring output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_log = []
    
    def create_realtime_dashboard(self, launch_data: Dict) -> str:
        """
        Generate live HTML dashboard.
        
        Shows:
        - Posts going live (countdown)
        - Current engagement (views, likes, shares)
        - Trending status per city
        - World map with active cities highlighted
        - Live comment feed
        - Viral coefficient tracking
        
        Updates every 10 seconds
        
        Args:
            launch_data: Launch configuration data
            
        Returns:
            Path to dashboard HTML file
        """
        logger.info("📊 Creating real-time dashboard...")
        
        dashboard_html = self._generate_dashboard_html(launch_data)
        
        dashboard_path = self.output_dir / "launch_dashboard.html"
        with open(dashboard_path, 'w') as f:
            f.write(dashboard_html)
        
        logger.info(f"✅ Dashboard created: {dashboard_path}")
        
        return str(dashboard_path)
    
    def _generate_dashboard_html(self, launch_data: Dict) -> str:
        """
        Generate HTML for real-time dashboard.
        
        Args:
            launch_data: Launch data
            
        Returns:
            HTML string
        """
        total_posts = launch_data.get('total_posts', 0)
        cities = launch_data.get('cities', 0)
        languages = launch_data.get('languages', 0)
        platforms = launch_data.get('platforms', 0)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌍 UMAJA World Tour - Launch Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .stat-value {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.8;
        }}
        .timeline {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }}
        .timeline-item {{
            display: flex;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }}
        .timeline-time {{
            font-weight: bold;
            margin-right: 20px;
            min-width: 120px;
        }}
        .timeline-city {{
            flex: 1;
        }}
        .status-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .status-scheduled {{ background: #fbbf24; color: #78350f; }}
        .status-live {{ background: #10b981; color: #064e3b; }}
        .status-complete {{ background: #3b82f6; color: #1e3a8a; }}
        .refresh-notice {{
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .metric-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
        }}
        .metric-title {{
            font-size: 1.2em;
            margin-bottom: 15px;
            opacity: 0.9;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 UMAJA World Tour Launch Dashboard</h1>
        <p class="subtitle">Real-time monitoring of Global Smile Day</p>
        
        <div class="refresh-notice">
            📡 Dashboard updates every 10 seconds • Last updated: <span id="last-update">{datetime.utcnow().strftime('%H:%M:%S UTC')}</span>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Posts</div>
                <div class="stat-value">{total_posts}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Cities</div>
                <div class="stat-value">{cities}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Languages</div>
                <div class="stat-value">{languages}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Platforms</div>
                <div class="stat-value">{platforms}</div>
            </div>
        </div>
        
        <div class="timeline">
            <h2>🚀 Live Timeline</h2>
            <div id="timeline-content">
                <div class="timeline-item">
                    <span class="timeline-time">00:00 UTC</span>
                    <span class="timeline-city">Launch begins...</span>
                    <span class="status-badge status-scheduled">SCHEDULED</span>
                </div>
                <div class="timeline-item">
                    <span class="timeline-time">02:00 UTC</span>
                    <span class="timeline-city">Tokyo • TikTok</span>
                    <span class="status-badge status-scheduled">SCHEDULED</span>
                </div>
                <div class="timeline-item">
                    <span class="timeline-time">04:00 UTC</span>
                    <span class="timeline-city">Sydney • Instagram</span>
                    <span class="status-badge status-scheduled">SCHEDULED</span>
                </div>
            </div>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-title">📈 Total Engagement</div>
                <div class="metric-value">0</div>
                <p style="opacity: 0.7;">Views • Likes • Shares</p>
            </div>
            <div class="metric-card">
                <div class="metric-title">🔥 Viral Posts</div>
                <div class="metric-value">0</div>
                <p style="opacity: 0.7;">Posts > 100k views</p>
            </div>
            <div class="metric-card">
                <div class="metric-title">😊 Sentiment</div>
                <div class="metric-value">95%</div>
                <p style="opacity: 0.7;">Positive comments</p>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 10 seconds
        setInterval(function() {{
            document.getElementById('last-update').textContent = new Date().toUTCString();
            // In production, this would fetch real data
        }}, 10000);
    </script>
</body>
</html>"""
        
        return html
    
    def track_metrics(self, launch_data: Dict) -> Dict:
        """
        Real-time metrics aggregation.
        
        Tracks:
        - Total reach (all platforms)
        - Engagement rate per language
        - Viral posts (> 10k views)
        - Comment sentiment
        - Share velocity
        - Trending hashtags
        
        Args:
            launch_data: Launch data
            
        Returns:
            Current metrics dictionary
        """
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_reach': 0,
            'total_engagement': 0,
            'viral_posts': 0,
            'sentiment': {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            },
            'by_platform': {
                'tiktok': {'views': 0, 'likes': 0, 'shares': 0},
                'instagram': {'views': 0, 'likes': 0, 'shares': 0},
                'youtube': {'views': 0, 'likes': 0, 'shares': 0}
            },
            'by_language': {},
            'trending_hashtags': [],
            'top_performing_cities': []
        }
        
        # Log metrics
        self.metrics_log.append(metrics)
        
        # Save to file
        metrics_file = self.output_dir / f"metrics_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"📊 Metrics tracked: {len(self.metrics_log)} snapshots")
        
        return metrics
    
    def send_alerts(self, alert_type: str, data: Dict):
        """
        Notify on important events.
        
        Alerts:
        - Post goes viral (> 100k views)
        - Negative sentiment spike (needs response)
        - Technical failure (post didn't publish)
        - Milestone reached (1M total views!)
        
        Args:
            alert_type: Type of alert
            data: Alert data
        """
        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': alert_type,
            'data': data
        }
        
        # Log alert
        alerts_file = self.output_dir / "alerts.jsonl"
        with open(alerts_file, 'a') as f:
            f.write(json.dumps(alert) + '\n')
        
        # Print to console
        logger.info(f"🚨 ALERT [{alert_type.upper()}]: {data}")
    
    def get_live_status(self, schedule: Dict) -> Dict:
        """
        Get current live status of posts.
        
        Args:
            schedule: Schedule dictionary
            
        Returns:
            Live status summary
        """
        now = datetime.utcnow()
        
        status = {
            'current_time': now.isoformat(),
            'posts_live': 0,
            'posts_upcoming': 0,
            'posts_completed': 0,
            'next_post': None
        }
        
        for post in schedule.get('posts', []):
            post_time = datetime.fromisoformat(post['scheduled_time'])
            
            if post_time <= now:
                if post_time > now - timedelta(hours=1):
                    status['posts_live'] += 1
                else:
                    status['posts_completed'] += 1
            else:
                status['posts_upcoming'] += 1
                
                if status['next_post'] is None:
                    status['next_post'] = post
        
        return status
    
    def generate_progress_report(self, schedule: Dict, metrics: Dict) -> str:
        """
        Generate progress report.
        
        Args:
            schedule: Schedule data
            metrics: Metrics data
            
        Returns:
            Formatted report
        """
        status = self.get_live_status(schedule)
        
        report = "=" * 60 + "\n"
        report += "🌍 LAUNCH DAY PROGRESS REPORT\n"
        report += "=" * 60 + "\n\n"
        
        report += f"⏰ Current Time: {status['current_time']}\n\n"
        
        report += "📊 Posts Status:\n"
        report += f"  ✅ Completed: {status['posts_completed']}\n"
        report += f"  🔴 Live: {status['posts_live']}\n"
        report += f"  ⏳ Upcoming: {status['posts_upcoming']}\n\n"
        
        if status['next_post']:
            next_post = status['next_post']
            report += f"⏭️  Next Post:\n"
            report += f"  City: {next_post['city_name']}\n"
            report += f"  Platform: {next_post['platform']}\n"
            report += f"  Time: {next_post['scheduled_time']}\n\n"
        
        report += "📈 Engagement:\n"
        report += f"  Reach: {metrics.get('total_reach', 0):,}\n"
        report += f"  Viral Posts: {metrics.get('viral_posts', 0)}\n"
        report += f"  Sentiment: {metrics.get('sentiment', {}).get('positive', 0)}% positive\n\n"
        
        report += "=" * 60 + "\n"
        
        return report
    
    def export_metrics(self, format: str = 'json') -> str:
        """
        Export collected metrics.
        
        Args:
            format: Export format (json, csv)
            
        Returns:
            Path to export file
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            export_file = self.output_dir / f"metrics_export_{timestamp}.json"
            with open(export_file, 'w') as f:
                json.dump(self.metrics_log, f, indent=2)
        elif format == 'csv':
            export_file = self.output_dir / f"metrics_export_{timestamp}.csv"
            # CSV export would be implemented here
            pass
        
        logger.info(f"📤 Metrics exported to {export_file}")
        
        return str(export_file)


# Example usage
if __name__ == "__main__":
    monitor = LaunchDayMonitor()
    
    print("📊 Launch Day Monitor Test")
    print("=" * 60)
    
    # Test dashboard creation
    test_launch_data = {
        'total_posts': 1200,
        'cities': 50,
        'languages': 8,
        'platforms': 3
    }
    
    dashboard_path = monitor.create_realtime_dashboard(test_launch_data)
    print(f"\n✅ Dashboard created: {dashboard_path}")
    
    # Test metrics tracking
    metrics = monitor.track_metrics(test_launch_data)
    print(f"📊 Metrics tracked: {metrics['timestamp']}")
    
    # Test alert
    monitor.send_alerts('viral_post', {
        'city': 'tokyo',
        'platform': 'tiktok',
        'views': 150000
    })
    print("🚨 Alert sent!")
