#!/usr/bin/env python3
"""
🌍 LAUNCH THE WORLD TOUR

One-command script to generate and launch world tour content at scale.

Usage:
    python scripts/launch_world_tour.py --date "2026-01-01" --dry-run
    python scripts/launch_world_tour.py --cities all --languages all
    python scripts/launch_world_tour.py --go-live  # THE BIG ONE

Options:
    --date DATE          Launch date (default: today)
    --cities LIST        Comma-separated city IDs or "all" (default: all)
    --languages LIST     Comma-separated language codes or "all" (default: all)
    --platforms LIST     tiktok,instagram,youtube (default: all)
    --dry-run            Test run without actually posting
    --go-live            ACTUALLY POST (requires confirmation)
    --monitor            Start real-time monitoring dashboard
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from world_tour_automation import WorldTourAutomation
from safety_system import SafetySystem
from launch_day_monitor import LaunchDayMonitor


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="🌍 Launch UMAJA World Tour - Global content generation at scale",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Dry run for testing
  python scripts/launch_world_tour.py --date "2026-01-01" --dry-run
  
  # Launch with specific cities and languages
  python scripts/launch_world_tour.py --cities "new_york,london,tokyo" --languages "en,es"
  
  # Full global launch (requires confirmation)
  python scripts/launch_world_tour.py --go-live
  
  # Launch with monitoring
  python scripts/launch_world_tour.py --go-live --monitor
        """
    )
    
    parser.add_argument(
        '--date',
        type=str,
        default=datetime.utcnow().strftime('%Y-%m-%d'),
        help='Launch date in YYYY-MM-DD format (default: today)'
    )
    
    parser.add_argument(
        '--cities',
        type=str,
        default='all',
        help='Comma-separated city IDs or "all" (default: all)'
    )
    
    parser.add_argument(
        '--languages',
        type=str,
        default='all',
        help='Comma-separated language codes or "all" (default: all)'
    )
    
    parser.add_argument(
        '--platforms',
        type=str,
        default='all',
        help='Comma-separated platform names: tiktok,instagram,youtube (default: all)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test run without actually posting'
    )
    
    parser.add_argument(
        '--go-live',
        action='store_true',
        help='ACTUALLY POST content (requires confirmation)'
    )
    
    parser.add_argument(
        '--monitor',
        action='store_true',
        help='Start real-time monitoring dashboard'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        help='Limit number of cities (for testing)'
    )
    
    return parser.parse_args()


def parse_list_arg(arg: str, all_values: list = None) -> list:
    """
    Parse list argument.
    
    Args:
        arg: Argument string
        all_values: List of all possible values
        
    Returns:
        List of values
    """
    if arg.lower() == 'all':
        return all_values or []
    
    return [item.strip() for item in arg.split(',')]


def main():
    """Main entry point for world tour launch"""
    args = parse_arguments()
    
    print("=" * 70)
    print("🌍 UMAJA WORLD TOUR LAUNCHER")
    print("=" * 70)
    print()
    
    # Parse date
    try:
        launch_date = datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        print(f"❌ Invalid date format: {args.date}")
        print("   Use YYYY-MM-DD format (e.g., 2026-01-01)")
        sys.exit(1)
    
    # Initialize systems
    automation = WorldTourAutomation()
    safety = SafetySystem()
    
    # Parse cities
    if args.cities == 'all':
        from worldtour_generator import WorldtourGenerator
        wt_gen = WorldtourGenerator()
        cities = list(wt_gen.cities.keys())
        if args.count:
            cities = cities[:args.count]
    else:
        cities = parse_list_arg(args.cities)
    
    # Parse languages
    languages = parse_list_arg(
        args.languages,
        ['en', 'es', 'fr', 'de', 'ja', 'zh', 'ar', 'pt']
    )
    
    # Parse platforms
    platforms = parse_list_arg(
        args.platforms,
        ['tiktok', 'instagram', 'youtube']
    )
    
    # Calculate totals
    total_posts = len(cities) * len(languages) * len(platforms)
    
    # Display configuration
    print(f"📅 Launch Date: {launch_date.strftime('%Y-%m-%d')}")
    print(f"🌆 Cities: {len(cities)}")
    print(f"🌐 Languages: {len(languages)}")
    print(f"📱 Platforms: {len(platforms)}")
    print(f"📊 Total Posts: {total_posts}")
    print()
    
    # Dry run mode
    if args.dry_run:
        print("🧪 DRY RUN MODE - No actual posting will occur")
        print("=" * 70)
        print()
        
        simulation_data = {
            'total_posts': total_posts,
            'cities': len(cities),
            'languages': len(languages),
            'platforms': len(platforms),
            'launch_date': args.date
        }
        
        simulation = safety.dry_run_mode('global_launch', simulation_data)
        
        print()
        print("✅ Dry run complete!")
        print(f"📁 Simulation log saved")
        print()
        print("To perform actual launch, use --go-live flag")
        sys.exit(0)
    
    # Go live - require confirmation
    if args.go_live:
        print("⚠️  GO LIVE MODE - Content will be ACTUALLY POSTED")
        print("=" * 70)
        print()
        
        # Safety confirmation
        confirmed = safety.require_confirmation(
            action="Global World Tour Launch",
            details={
                'Total Posts': total_posts,
                'Cities': len(cities),
                'Languages': len(languages),
                'Platforms': ', '.join(platforms),
                'Launch Date': args.date,
                'Estimated Reach': automation._calculate_reach(total_posts)
            }
        )
        
        if not confirmed:
            print()
            print("❌ Launch cancelled")
            sys.exit(0)
        
        print()
        print("✅ Launch confirmed - proceeding...")
        print()
    else:
        # Neither dry-run nor go-live
        print("⚠️  Please specify either --dry-run or --go-live")
        print()
        print("Examples:")
        print("  python scripts/launch_world_tour.py --dry-run")
        print("  python scripts/launch_world_tour.py --go-live")
        sys.exit(1)
    
    # Generate content
    print("🚀 Starting content generation...")
    print("=" * 70)
    print()
    
    try:
        launch_data = automation.generate_global_launch(
            launch_date=launch_date,
            cities=cities,
            languages=languages,
            platforms=platforms
        )
        
        print()
        print("=" * 70)
        print("✨ CONTENT GENERATION COMPLETE")
        print("=" * 70)
        print()
        print(f"📊 Stats:")
        print(f"   Total Posts: {launch_data['total_posts']}")
        print(f"   Content Ready: {launch_data['content_ready']}")
        print(f"   Schedule Created: {launch_data['schedule_created']}")
        print(f"   QA Passed: {launch_data['qa_passed']}")
        print(f"   Estimated Reach: {launch_data['estimated_reach']}")
        print()
        
        # QA Summary
        qa_summary = launch_data['qa_summary']
        print(f"✅ Quality Assurance:")
        print(f"   Passed: {qa_summary['passed']}")
        print(f"   Failed: {qa_summary['failed']}")
        print(f"   Warnings: {qa_summary['warnings']}")
        print()
        
        # Start monitoring if requested
        if args.monitor:
            print("📊 Starting launch day monitoring...")
            print("=" * 70)
            print()
            
            monitor = LaunchDayMonitor()
            monitoring = automation.monitor_launch_day(launch_data)
            
            print(f"✅ Monitoring dashboard created:")
            print(f"   Dashboard: {monitoring['dashboard_url']}")
            print()
            print("🔄 Dashboard will update in real-time")
            print(f"   Open {monitoring['dashboard_url']} in your browser")
            print()
        
        # Success message
        print("=" * 70)
        print("🎉 LAUNCH COMPLETE!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Review the generated content")
        print("  2. Monitor engagement metrics")
        print("  3. Respond to community comments")
        print()
        print("🚨 Emergency stop available if needed:")
        print("   safety.emergency_stop('reason')")
        print()
        print("😊 Let's put smiles on faces around the world!")
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR OCCURRED")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("🚨 Initiating safety protocols...")
        
        # Emergency stop
        safety.emergency_stop(f"Launch error: {e}")
        
        print()
        print("✅ Safety protocols activated")
        print("   All scheduled posts have been stopped")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
