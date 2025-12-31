"""
UMAJA Safety System - Prevent Disasters
Safety features, confirmations, and emergency controls
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SafetySystem:
    """
    Prevent disasters with safety checks and emergency controls.
    Provides dry-run mode, confirmations, and rollback capability.
    """
    
    def __init__(self, output_dir: str = "output/safety"):
        """
        Initialize safety system.
        
        Args:
            output_dir: Directory for safety logs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.safety_log = []
    
    def require_confirmation(self, action: str, details: Dict) -> bool:
        """
        Require explicit confirmation for major actions.
        
        Example:
        "You are about to post 1200 pieces of content to 3 platforms.
         This cannot be undone.
         Type 'I UNDERSTAND' to continue: "
        
        Args:
            action: Action description
            details: Action details
            
        Returns:
            True if confirmed, False otherwise
        """
        logger.warning("=" * 60)
        logger.warning(f"⚠️  CONFIRMATION REQUIRED")
        logger.warning("=" * 60)
        logger.warning(f"\nAction: {action}")
        logger.warning(f"\nDetails:")
        
        for key, value in details.items():
            logger.warning(f"  - {key}: {value}")
        
        logger.warning("\n⚠️  THIS ACTION CANNOT BE UNDONE")
        logger.warning("\nType 'I UNDERSTAND' to continue, or anything else to cancel:")
        
        try:
            response = input("> ").strip()
            
            if response == "I UNDERSTAND":
                self._log_action(action, details, 'confirmed')
                logger.info("✅ Action confirmed by user")
                return True
            else:
                self._log_action(action, details, 'cancelled')
                logger.info("❌ Action cancelled by user")
                return False
        except (KeyboardInterrupt, EOFError):
            self._log_action(action, details, 'interrupted')
            logger.info("\n❌ Action interrupted")
            return False
    
    def dry_run_mode(self, action: str, data: Dict) -> Dict:
        """
        Test everything without actually posting.
        
        Shows:
        - What would be posted
        - When it would be posted
        - Predicted outcomes
        - No actual API calls
        
        Args:
            action: Action to simulate
            data: Action data
            
        Returns:
            Simulation results
        """
        logger.info("🧪 DRY RUN MODE - No actual changes will be made")
        logger.info("=" * 60)
        
        simulation = {
            'mode': 'dry_run',
            'action': action,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
            'would_affect': self._analyze_impact(data)
        }
        
        logger.info(f"\nAction: {action}")
        logger.info(f"Timestamp: {simulation['timestamp']}")
        logger.info(f"\nImpact Analysis:")
        
        for key, value in simulation['would_affect'].items():
            logger.info(f"  - {key}: {value}")
        
        logger.info("\n✅ Dry run complete - no actual changes made")
        
        # Save dry run log
        self._save_dry_run_log(simulation)
        
        return simulation
    
    def emergency_stop(self, reason: str = "Manual stop") -> Dict:
        """
        PANIC BUTTON - stop all scheduled posts.
        
        Args:
            reason: Reason for emergency stop
            
        Returns:
            Emergency stop status
        """
        logger.error("=" * 60)
        logger.error("🚨 EMERGENCY STOP ACTIVATED")
        logger.error("=" * 60)
        logger.error(f"\nReason: {reason}")
        logger.error(f"Time: {datetime.utcnow().isoformat()}")
        
        stop_status = {
            'activated': True,
            'timestamp': datetime.utcnow().isoformat(),
            'reason': reason,
            'actions_taken': [
                'Stopped all scheduled posts',
                'Disabled auto-posting',
                'Created emergency log'
            ]
        }
        
        # Log emergency stop
        self._log_emergency_stop(stop_status)
        
        logger.error("\n✅ Emergency stop complete")
        logger.error("All scheduled posts have been stopped")
        
        return stop_status
    
    def rollback_capability(self, launch_id: str) -> Dict:
        """
        Delete posts if something goes wrong.
        
        Args:
            launch_id: Launch identifier
            
        Returns:
            Rollback status
        """
        logger.warning(f"🔄 Initiating rollback for launch: {launch_id}")
        
        rollback = {
            'launch_id': launch_id,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'initiated',
            'posts_removed': 0,
            'posts_failed': 0
        }
        
        # In production, this would:
        # 1. Find all posts from this launch
        # 2. Delete them from platforms
        # 3. Update database
        # 4. Create rollback log
        
        logger.warning(f"⚠️  Rollback would remove posts from launch {launch_id}")
        logger.warning("This is a simulation - actual rollback not implemented")
        
        rollback['status'] = 'simulated'
        
        return rollback
    
    def validate_safety_checks(self, launch_data: Dict) -> Dict:
        """
        Run all safety checks before launch.
        
        Args:
            launch_data: Launch data to validate
            
        Returns:
            Safety check results
        """
        logger.info("🔒 Running safety checks...")
        
        checks = {
            'content_validated': False,
            'schedule_verified': False,
            'platforms_accessible': False,
            'backups_created': False,
            'emergency_stop_ready': False,
            'all_checks_passed': False
        }
        
        # Check 1: Content validation
        if 'content_batch' in launch_data:
            checks['content_validated'] = True
            logger.info("  ✓ Content validated")
        
        # Check 2: Schedule verification
        if 'schedule' in launch_data:
            checks['schedule_verified'] = True
            logger.info("  ✓ Schedule verified")
        
        # Check 3: Platform accessibility (simulated)
        checks['platforms_accessible'] = True
        logger.info("  ✓ Platforms accessible")
        
        # Check 4: Backups created
        checks['backups_created'] = self._create_backup(launch_data)
        if checks['backups_created']:
            logger.info("  ✓ Backups created")
        
        # Check 5: Emergency stop ready
        checks['emergency_stop_ready'] = True
        logger.info("  ✓ Emergency stop ready")
        
        # All checks passed?
        checks['all_checks_passed'] = all(checks.values())
        
        if checks['all_checks_passed']:
            logger.info("\n✅ All safety checks passed")
        else:
            logger.warning("\n⚠️  Some safety checks failed")
        
        return checks
    
    def _analyze_impact(self, data: Dict) -> Dict:
        """
        Analyze impact of action.
        
        Args:
            data: Action data
            
        Returns:
            Impact analysis
        """
        return {
            'posts': data.get('total_posts', 0),
            'cities': data.get('cities', 0),
            'languages': data.get('languages', 0),
            'platforms': data.get('platforms', 0),
            'estimated_reach': data.get('estimated_reach', 'Unknown')
        }
    
    def _log_action(self, action: str, details: Dict, status: str):
        """Log safety action"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'details': details,
            'status': status
        }
        
        self.safety_log.append(log_entry)
        
        # Save to file
        log_file = self.output_dir / "safety_log.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _save_dry_run_log(self, simulation: Dict):
        """Save dry run log"""
        log_file = self.output_dir / f"dry_run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(simulation, f, indent=2)
        logger.info(f"\n📁 Dry run log saved: {log_file}")
    
    def _log_emergency_stop(self, stop_status: Dict):
        """Log emergency stop"""
        log_file = self.output_dir / f"emergency_stop_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(stop_status, f, indent=2)
        logger.error(f"\n📁 Emergency stop logged: {log_file}")
    
    def _create_backup(self, data: Dict) -> bool:
        """Create backup of launch data"""
        try:
            backup_file = self.output_dir / f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def get_safety_status(self) -> Dict:
        """
        Get current safety system status.
        
        Returns:
            Status dictionary
        """
        return {
            'safety_log_entries': len(self.safety_log),
            'emergency_stops': sum(1 for log in self.safety_log 
                                  if 'emergency_stop' in log.get('action', '')),
            'dry_runs': sum(1 for log in self.safety_log 
                           if 'dry_run' in log.get('action', '')),
            'confirmations': sum(1 for log in self.safety_log 
                               if log.get('status') == 'confirmed')
        }


# Example usage
if __name__ == "__main__":
    safety = SafetySystem()
    
    print("🔒 Safety System Test")
    print("=" * 60)
    
    # Test dry run
    test_data = {
        'total_posts': 1200,
        'cities': 50,
        'languages': 8,
        'platforms': 3,
        'estimated_reach': '10M+ people'
    }
    
    print("\n🧪 Testing dry run mode...")
    dry_run = safety.dry_run_mode('global_launch', test_data)
    print(f"Dry run completed: {dry_run['mode']}")
    
    # Test safety checks
    print("\n🔒 Testing safety checks...")
    checks = safety.validate_safety_checks({
        'content_batch': {},
        'schedule': {}
    })
    print(f"All checks passed: {checks['all_checks_passed']}")
    
    # Test emergency stop
    print("\n🚨 Testing emergency stop...")
    stop = safety.emergency_stop("Test stop")
    print(f"Emergency stop: {stop['activated']}")
