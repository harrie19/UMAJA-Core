"""
UMAJA World Tour Automation - Master Orchestrator
One-command world tour content generation for global launch
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorldTourAutomation:
    """
    One-command world tour content generation.
    Orchestrates batch generation, scheduling, and monitoring for global launches.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize automation system.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.output_dir = Path(self.config.get('output_dir', 'output/world_tour'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Lazy-load dependencies to avoid circular imports
        self._batch_generator = None
        self._scheduler = None
        self._qa_system = None
        self._monitor = None
    
    @property
    def batch_generator(self):
        """Lazy-load batch content generator"""
        if self._batch_generator is None:
            from batch_content_generator import BatchContentGenerator
            self._batch_generator = BatchContentGenerator()
        return self._batch_generator
    
    @property
    def scheduler(self):
        """Lazy-load smart scheduler"""
        if self._scheduler is None:
            from smart_scheduler import SmartScheduler
            self._scheduler = SmartScheduler()
        return self._scheduler
    
    @property
    def qa_system(self):
        """Lazy-load quality assurance system"""
        if self._qa_system is None:
            from quality_assurance import QualityAssurance
            self._qa_system = QualityAssurance()
        return self._qa_system
    
    @property
    def monitor(self):
        """Lazy-load launch day monitor"""
        if self._monitor is None:
            from launch_day_monitor import LaunchDayMonitor
            self._monitor = LaunchDayMonitor()
        return self._monitor
    
    def generate_global_launch(self, launch_date: datetime, 
                               cities: List[str] = None,
                               languages: List[str] = None,
                               platforms: List[str] = None) -> Dict:
        """
        Generate ALL content for world tour launch.
        
        Args:
            launch_date: Date for the global launch
            cities: List of city IDs (default: all 50 cities)
            languages: List of language codes (default: 8 languages)
            platforms: List of platforms (default: tiktok, instagram, youtube)
            
        Returns:
            {
                'total_posts': 1200,
                'cities': 50,
                'languages': 8,
                'platforms': 3,
                'estimated_reach': '10M+ people',
                'content_ready': True,
                'schedule_created': True,
                'content_batch': {...}
            }
        """
        logger.info("🚀 Starting global launch content generation...")
        
        # Default values
        if cities is None:
            from worldtour_generator import WorldtourGenerator
            wt_gen = WorldtourGenerator()
            cities = list(wt_gen.cities.keys())[:50]  # Get first 50 cities
        
        if languages is None:
            languages = ['en', 'es', 'fr', 'de', 'ja', 'zh', 'ar', 'pt']  # 8 languages
        
        if platforms is None:
            platforms = ['tiktok', 'instagram', 'youtube']  # 3 platforms
        
        # Calculate totals
        total_posts = len(cities) * len(languages) * len(platforms)
        
        logger.info(f"📊 Generating content for:")
        logger.info(f"   - {len(cities)} cities")
        logger.info(f"   - {len(languages)} languages")
        logger.info(f"   - {len(platforms)} platforms")
        logger.info(f"   = {total_posts} total posts")
        
        # Step 1: Generate content batch
        logger.info("📝 Step 1/4: Generating content batch...")
        content_batch = self.batch_generator.generate_city_batch(
            cities=cities,
            languages=languages,
            platforms=platforms,
            parallel=True
        )
        
        # Step 2: Quality assurance
        logger.info("✅ Step 2/4: Running quality assurance...")
        qa_results = self.qa_system.validate_content_batch(content_batch)
        
        if not qa_results['safe_to_launch']:
            logger.warning("⚠️  Quality assurance found issues. Auto-fixing...")
            content_batch = self.qa_system.auto_fix_issues(
                content_batch, 
                qa_results['issues']
            )
            # Re-validate
            qa_results = self.qa_system.validate_content_batch(content_batch)
        
        # Step 3: Create schedule
        logger.info("📅 Step 3/4: Creating optimal schedule...")
        schedule = self.scheduler.create_global_schedule(
            content_batch=content_batch,
            launch_date=launch_date
        )
        
        # Step 4: Save everything
        logger.info("💾 Step 4/4: Saving content and schedule...")
        output_file = self.output_dir / f"global_launch_{launch_date.strftime('%Y%m%d')}.json"
        
        launch_data = {
            'launch_date': launch_date.isoformat(),
            'total_posts': total_posts,
            'cities': len(cities),
            'languages': len(languages),
            'platforms': len(platforms),
            'estimated_reach': self._calculate_reach(total_posts),
            'content_ready': True,
            'schedule_created': True,
            'qa_passed': qa_results['safe_to_launch'],
            'qa_summary': {
                'passed': qa_results['passed'],
                'failed': qa_results['failed'],
                'warnings': qa_results['warnings']
            },
            'content_batch': content_batch,
            'schedule': schedule
        }
        
        with open(output_file, 'w') as f:
            json.dump(launch_data, f, indent=2)
        
        logger.info(f"✨ Global launch content ready!")
        logger.info(f"📁 Saved to: {output_file}")
        
        return launch_data
    
    def schedule_optimal_posts(self, content_batch: Dict, launch_date: datetime) -> Dict:
        """
        Auto-schedule posts for optimal timezone-specific times.
        
        Features:
        - Calculates best posting time per city
        - Respects platform algorithms (TikTok peak times, etc.)
        - Staggers posts to avoid spam detection
        - Creates backup schedule if primary fails
        
        Args:
            content_batch: Generated content batch
            launch_date: Launch date for scheduling
            
        Returns:
            Schedule dictionary with optimal posting times
        """
        logger.info("📅 Creating optimal posting schedule...")
        
        schedule = self.scheduler.create_global_schedule(
            content_batch=content_batch,
            launch_date=launch_date
        )
        
        # Add backup times
        schedule['backup_times'] = self.scheduler.calculate_backup_schedule(schedule)
        
        return schedule
    
    def monitor_launch_day(self, launch_data: Dict) -> Dict:
        """
        Real-time monitoring during Global Smile Day.
        
        Tracks:
        - Posts going live (success/failure)
        - Engagement metrics per city/language
        - Trending status
        - Comment sentiment
        - Viral coefficient
        
        Args:
            launch_data: Launch data dictionary
            
        Returns:
            Monitoring dashboard data
        """
        logger.info("📊 Starting launch day monitoring...")
        
        # Create real-time dashboard
        dashboard_url = self.monitor.create_realtime_dashboard(launch_data)
        
        # Start tracking metrics
        metrics = self.monitor.track_metrics(launch_data)
        
        return {
            'dashboard_url': dashboard_url,
            'metrics': metrics,
            'monitoring_active': True
        }
    
    def _calculate_reach(self, total_posts: int) -> str:
        """
        Estimate potential reach based on number of posts.
        
        Args:
            total_posts: Total number of posts
            
        Returns:
            Estimated reach string (e.g., "10M+ people")
        """
        # Rough estimate: 10k avg views per post
        avg_views_per_post = 10000
        total_views = total_posts * avg_views_per_post
        
        if total_views >= 10_000_000:
            return f"{total_views // 1_000_000}M+ people"
        elif total_views >= 1_000_000:
            return f"{total_views // 1_000_000}M+ people"
        else:
            return f"{total_views // 1000}K+ people"
    
    def get_launch_status(self, launch_date: datetime) -> Dict:
        """
        Get status of a launch.
        
        Args:
            launch_date: Launch date
            
        Returns:
            Status dictionary
        """
        output_file = self.output_dir / f"global_launch_{launch_date.strftime('%Y%m%d')}.json"
        
        if output_file.exists():
            with open(output_file, 'r') as f:
                return json.load(f)
        
        return {'status': 'not_found'}


# Example usage
if __name__ == "__main__":
    automation = WorldTourAutomation()
    
    # Test launch generation
    launch_date = datetime(2026, 1, 1)
    
    print("🌍 UMAJA World Tour Automation Test")
    print("=" * 60)
    
    # Generate small test batch (5 cities, 2 languages, 2 platforms)
    result = automation.generate_global_launch(
        launch_date=launch_date,
        cities=['new_york', 'london', 'tokyo', 'paris', 'berlin'],
        languages=['en', 'es'],
        platforms=['tiktok', 'instagram']
    )
    
    print(f"\n✨ Launch Generation Complete!")
    print(f"   Total Posts: {result['total_posts']}")
    print(f"   Cities: {result['cities']}")
    print(f"   Languages: {result['languages']}")
    print(f"   Platforms: {result['platforms']}")
    print(f"   Estimated Reach: {result['estimated_reach']}")
    print(f"   Content Ready: {result['content_ready']}")
    print(f"   QA Passed: {result['qa_passed']}")
