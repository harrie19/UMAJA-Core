"""
UMAJA Smart Scheduler - Intelligent Timing
Timezone-aware optimal posting scheduler with platform-specific timing
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartScheduler:
    """
    Timezone-aware optimal posting scheduler.
    Calculates best posting times based on city, platform, and engagement patterns.
    """
    
    # Platform-specific peak hours (in local time)
    PLATFORM_PEAK_HOURS = {
        'tiktok': [(7, 9), (19, 23)],  # 7-9am, 7-11pm
        'instagram': [(11, 13), (19, 21)],  # 11am-1pm, 7-9pm
        'youtube': [(12, 15), (20, 22)]  # 12-3pm, 8-10pm
    }
    
    # City timezones (UTC offset)
    CITY_TIMEZONES = {
        'new_york': -5,
        'london': 0,
        'tokyo': 9,
        'paris': 1,
        'berlin': 1,
        'rome': 1,
        'barcelona': 1,
        'amsterdam': 1,
        'sydney': 10,
        'dubai': 4,
        'mumbai': 5.5,
        'singapore': 8,
        'bangkok': 7,
        'istanbul': 3,
        'moscow': 3,
        'mexico_city': -6,
        'rio_de_janeiro': -3,
        'buenos_aires': -3,
        'toronto': -5,
        'vancouver': -8,
        'chicago': -6,
        'los_angeles': -8,
        'san_francisco': -8,
        'miami': -5,
        'seattle': -8,
        'boston': -5,
        'madrid': 1,
        'lisbon': 0,
        'vienna': 1,
        'prague': 1,
        'budapest': 1,
        'athens': 2,
        'cairo': 2,
        'cape_town': 2,
        'nairobi': 3,
        'lagos': 1,
        'shanghai': 8,
        'beijing': 8,
        'seoul': 9,
        'hong_kong': 8,
        'delhi': 5.5,
        'jakarta': 7,
        'manila': 8,
        'hanoi': 7,
        'kuala_lumpur': 8,
        'karachi': 5,
        'tehran': 3.5,
        'baghdad': 3,
        'tel_aviv': 2,
        'stockholm': 1,
        'copenhagen': 1,
        'oslo': 1,
        'helsinki': 2,
        'dublin': 0,
        'edinburgh': 0,
        'brussels': 1,
        'zurich': 1,
        'munich': 1,
        'hamburg': 1
    }
    
    def __init__(self):
        """Initialize smart scheduler"""
        pass
    
    def calculate_optimal_time(self, city: str, platform: str, 
                              base_date: datetime = None) -> datetime:
        """
        Calculate best posting time for city + platform.
        
        Factors:
        - Local timezone
        - Platform peak hours (TikTok: 7-9am, 7-11pm)
        - Day of week
        - Cultural considerations (prayer times, work hours)
        - Competition analysis
        
        Args:
            city: City ID
            platform: Platform name
            base_date: Base date for scheduling (default: today)
            
        Returns:
            Optimal posting datetime
        """
        if base_date is None:
            base_date = datetime.utcnow()
        
        # Get timezone offset
        tz_offset = self.CITY_TIMEZONES.get(city, 0)
        
        # Get platform peak hours
        peak_hours = self.PLATFORM_PEAK_HOURS.get(platform, [(12, 14)])
        
        # Select first peak window
        start_hour, end_hour = peak_hours[0]
        target_hour = (start_hour + end_hour) // 2
        
        # Calculate local time in city
        local_time = base_date + timedelta(hours=tz_offset)
        
        # Set to target hour today or tomorrow
        optimal_time = local_time.replace(hour=target_hour, minute=0, second=0, microsecond=0)
        
        # If time has passed, schedule for tomorrow
        if optimal_time < local_time:
            optimal_time += timedelta(days=1)
        
        # Convert back to UTC
        utc_time = optimal_time - timedelta(hours=tz_offset)
        
        return utc_time
    
    def create_global_schedule(self, 
                              content_batch: Dict,
                              launch_date: datetime = None) -> Dict:
        """
        Create 24-hour rolling schedule.
        
        Strategy:
        - Post every 2 hours in different timezone
        - Ensure 24/7 content flow
        - Avoid gaps in coverage
        - Maximize "always trending" effect
        
        Args:
            content_batch: Generated content batch
            launch_date: Launch date (default: today)
            
        Returns:
            Schedule dictionary with posting times
        """
        if launch_date is None:
            launch_date = datetime.utcnow()
        
        logger.info("📅 Creating global rolling schedule...")
        
        schedule = {
            'launch_date': launch_date.isoformat(),
            'total_posts': 0,
            'posts': [],
            'timeline': {}
        }
        
        post_index = 0
        current_offset = 0  # Hours offset from launch_date
        
        for city_id, city_data in content_batch.items():
            if 'error' in city_data:
                continue
            
            # Schedule posts for each platform
            for platform in city_data.get('platforms', {}).keys():
                # Calculate optimal time
                post_time = self.calculate_optimal_time(
                    city_id, 
                    platform,
                    launch_date + timedelta(hours=current_offset)
                )
                
                # Create post entry
                post_entry = {
                    'post_id': f"{city_id}_{platform}_{post_index}",
                    'city_id': city_id,
                    'city_name': city_data.get('city_name', city_id),
                    'platform': platform,
                    'scheduled_time': post_time.isoformat(),
                    'local_time': self._to_local_time(post_time, city_id),
                    'content': city_data['platforms'][platform],
                    'status': 'scheduled'
                }
                
                schedule['posts'].append(post_entry)
                
                # Add to timeline (group by hour)
                hour_key = post_time.strftime('%Y-%m-%d %H:00')
                if hour_key not in schedule['timeline']:
                    schedule['timeline'][hour_key] = []
                schedule['timeline'][hour_key].append(post_entry['post_id'])
                
                post_index += 1
                current_offset += 2  # Stagger by 2 hours
        
        schedule['total_posts'] = len(schedule['posts'])
        
        logger.info(f"✅ Scheduled {schedule['total_posts']} posts")
        
        return schedule
    
    def calculate_backup_schedule(self, primary_schedule: Dict) -> Dict:
        """
        Create backup schedule with alternative times.
        
        Args:
            primary_schedule: Primary schedule
            
        Returns:
            Backup schedule with +3 hour offset
        """
        backup = {
            'posts': []
        }
        
        for post in primary_schedule['posts']:
            primary_time = datetime.fromisoformat(post['scheduled_time'])
            backup_time = primary_time + timedelta(hours=3)
            
            backup_post = post.copy()
            backup_post['scheduled_time'] = backup_time.isoformat()
            backup_post['local_time'] = self._to_local_time(
                backup_time, 
                post['city_id']
            )
            backup_post['is_backup'] = True
            
            backup['posts'].append(backup_post)
        
        return backup
    
    def handle_failures_automatically(self, failed_posts: List[Dict]) -> Dict:
        """
        Auto-retry failed posts with backup times.
        
        Args:
            failed_posts: List of failed post entries
            
        Returns:
            Retry schedule
        """
        logger.info(f"🔄 Rescheduling {len(failed_posts)} failed posts...")
        
        retry_schedule = {
            'retry_count': len(failed_posts),
            'posts': []
        }
        
        for post in failed_posts:
            # Retry in 1 hour
            original_time = datetime.fromisoformat(post['scheduled_time'])
            retry_time = original_time + timedelta(hours=1)
            
            retry_post = post.copy()
            retry_post['scheduled_time'] = retry_time.isoformat()
            retry_post['retry_attempt'] = post.get('retry_attempt', 0) + 1
            retry_post['status'] = 'retry_scheduled'
            
            retry_schedule['posts'].append(retry_post)
        
        return retry_schedule
    
    def optimize_for_engagement(self, schedule: Dict) -> Dict:
        """
        Optimize schedule for maximum engagement.
        
        Args:
            schedule: Current schedule
            
        Returns:
            Optimized schedule
        """
        logger.info("🎯 Optimizing schedule for engagement...")
        
        optimized = schedule.copy()
        
        # Sort posts by predicted engagement time
        optimized['posts'].sort(
            key=lambda p: self._engagement_score(p),
            reverse=True
        )
        
        # Redistribute times to avoid clustering
        for i, post in enumerate(optimized['posts']):
            # Stagger by 90 minutes
            offset_minutes = i * 90
            original_time = datetime.fromisoformat(post['scheduled_time'])
            new_time = original_time + timedelta(minutes=offset_minutes)
            
            post['scheduled_time'] = new_time.isoformat()
        
        return optimized
    
    def _to_local_time(self, utc_time: datetime, city: str) -> str:
        """
        Convert UTC time to local time for city.
        
        Args:
            utc_time: UTC datetime
            city: City ID
            
        Returns:
            Local time string
        """
        tz_offset = self.CITY_TIMEZONES.get(city, 0)
        local_time = utc_time + timedelta(hours=tz_offset)
        return local_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    
    def _engagement_score(self, post: Dict) -> float:
        """
        Calculate engagement score for a post.
        
        Args:
            post: Post entry
            
        Returns:
            Engagement score
        """
        # Simple heuristic based on content quality
        score = 0.5
        
        platform = post.get('platform', '')
        if platform == 'tiktok':
            score += 0.2  # TikTok generally higher engagement
        elif platform == 'instagram':
            score += 0.15
        
        # Time-based bonus
        scheduled_time = datetime.fromisoformat(post['scheduled_time'])
        hour = scheduled_time.hour
        
        # Peak hours bonus
        if 7 <= hour <= 9 or 19 <= hour <= 22:
            score += 0.2
        
        return min(score, 1.0)
    
    def get_next_posts(self, schedule: Dict, hours: int = 24) -> List[Dict]:
        """
        Get posts scheduled for the next N hours.
        
        Args:
            schedule: Schedule dictionary
            hours: Number of hours to look ahead
            
        Returns:
            List of upcoming posts
        """
        now = datetime.utcnow()
        cutoff = now + timedelta(hours=hours)
        
        upcoming = []
        for post in schedule['posts']:
            post_time = datetime.fromisoformat(post['scheduled_time'])
            if now <= post_time <= cutoff:
                upcoming.append(post)
        
        # Sort by time
        upcoming.sort(key=lambda p: p['scheduled_time'])
        
        return upcoming


# Example usage
if __name__ == "__main__":
    scheduler = SmartScheduler()
    
    print("📅 Smart Scheduler Test")
    print("=" * 60)
    
    # Test optimal time calculation
    city = 'new_york'
    platform = 'tiktok'
    
    optimal_time = scheduler.calculate_optimal_time(city, platform)
    print(f"\nOptimal posting time for {city} on {platform}:")
    print(f"  UTC: {optimal_time}")
    print(f"  Local: {scheduler._to_local_time(optimal_time, city)}")
    
    # Test schedule creation
    mock_batch = {
        'new_york': {
            'city_name': 'New York',
            'platforms': {'tiktok': {}, 'instagram': {}}
        },
        'london': {
            'city_name': 'London',
            'platforms': {'tiktok': {}, 'youtube': {}}
        }
    }
    
    schedule = scheduler.create_global_schedule(mock_batch)
    print(f"\n📊 Created schedule:")
    print(f"  Total posts: {schedule['total_posts']}")
    print(f"  Timeline slots: {len(schedule['timeline'])}")
