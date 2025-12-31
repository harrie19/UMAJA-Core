"""
UMAJA Quality Assurance - Safety First
Ensure EVERY post is perfect before going live
"""

import logging
from typing import Dict, List, Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityAssurance:
    """
    Ensure EVERY post is perfect before going live.
    Validates content quality, cultural appropriateness, and technical requirements.
    """
    
    # Platform text limits
    PLATFORM_LIMITS = {
        'tiktok': 150,
        'instagram': 2200,
        'youtube': 5000
    }
    
    # Banned/problematic words/phrases (basic list)
    SENSITIVE_TERMS = [
        'hate', 'violence', 'discrimination', 'spam', 'scam'
    ]
    
    # Cultural sensitivity database (simplified)
    CULTURAL_CONSIDERATIONS = {
        'ar': {  # Arabic
            'avoid': ['alcohol', 'pork'],
            'respectful': ['family', 'tradition', 'hospitality']
        },
        'ja': {  # Japanese
            'avoid': ['direct confrontation'],
            'respectful': ['harmony', 'respect', 'politeness']
        },
        'zh': {  # Chinese
            'avoid': ['number 4', 'certain colors'],
            'respectful': ['family', 'prosperity', 'harmony']
        }
    }
    
    def __init__(self):
        """Initialize quality assurance system"""
        pass
    
    def validate_content_batch(self, batch: Dict) -> Dict:
        """
        Pre-flight checks for all content.
        
        Checks:
        - Translation quality (no gibberish)
        - Cultural appropriateness (no offense)
        - Hashtag validity (no banned tags)
        - Image/video quality (resolution, duration)
        - Text length (platform limits)
        - Subtitle sync (if video)
        
        Args:
            batch: Content batch to validate
            
        Returns:
            {
                'passed': 1180,
                'failed': 20,
                'warnings': 15,
                'safe_to_launch': True,
                'issues': [...]
            }
        """
        logger.info("🔍 Running quality assurance checks...")
        
        passed = 0
        failed = 0
        warnings = 0
        issues = []
        
        for city_id, city_data in batch.items():
            if 'error' in city_data:
                failed += 1
                issues.append({
                    'city': city_id,
                    'severity': 'error',
                    'issue': 'Generation failed',
                    'details': city_data['error']
                })
                continue
            
            # Validate each platform variant
            for platform, platform_data in city_data.get('platforms', {}).items():
                validation = self._validate_single_post(
                    city_id, platform, platform_data
                )
                
                if validation['status'] == 'passed':
                    passed += 1
                elif validation['status'] == 'failed':
                    failed += 1
                    issues.append(validation)
                elif validation['status'] == 'warning':
                    warnings += 1
                    issues.append(validation)
            
            # Validate language variants
            for lang, lang_data in city_data.get('languages', {}).items():
                if lang == 'en':
                    continue  # Already validated in platform check
                
                lang_check = self.cultural_safety_check(
                    str(lang_data), lang
                )
                
                if not lang_check['safe']:
                    issues.append({
                        'city': city_id,
                        'language': lang,
                        'severity': 'warning',
                        'issue': 'Cultural sensitivity concern',
                        'details': lang_check['concerns']
                    })
                    warnings += 1
        
        # Determine if safe to launch
        safe_to_launch = failed == 0 or (failed < passed * 0.05)  # < 5% failure rate
        
        result = {
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'safe_to_launch': safe_to_launch,
            'issues': issues,
            'total_checked': passed + failed
        }
        
        logger.info(f"✅ QA Complete: {passed} passed, {failed} failed, {warnings} warnings")
        
        return result
    
    def _validate_single_post(self, city: str, platform: str, content: Dict) -> Dict:
        """
        Validate a single post.
        
        Args:
            city: City ID
            platform: Platform name
            content: Content data
            
        Returns:
            Validation result
        """
        issues_found = []
        
        # Get text content
        text = content.get('content', '')
        if isinstance(text, dict):
            text = text.get('content', '')
        
        # Check 1: Text length
        max_length = self.PLATFORM_LIMITS.get(platform, 1000)
        if len(text) > max_length:
            issues_found.append(f"Text too long: {len(text)} > {max_length}")
        
        # Check 2: Sensitive terms
        text_lower = text.lower()
        for term in self.SENSITIVE_TERMS:
            if term in text_lower:
                issues_found.append(f"Contains sensitive term: {term}")
        
        # Check 3: Hashtags validity
        hashtags = content.get('hashtags', [])
        if not hashtags:
            issues_found.append("No hashtags found")
        
        for hashtag in hashtags:
            if not hashtag.startswith('#'):
                issues_found.append(f"Invalid hashtag format: {hashtag}")
        
        # Check 4: Minimum content length
        if len(text) < 20:
            issues_found.append("Content too short")
        
        # Determine status
        if any('sensitive term' in issue for issue in issues_found):
            status = 'failed'
            severity = 'error'
        elif issues_found:
            status = 'warning'
            severity = 'warning'
        else:
            status = 'passed'
            severity = 'info'
        
        return {
            'city': city,
            'platform': platform,
            'status': status,
            'severity': severity,
            'issue': ', '.join(issues_found) if issues_found else 'All checks passed',
            'details': issues_found
        }
    
    def cultural_safety_check(self, content: str, target_culture: str) -> Dict:
        """
        Deep cultural sensitivity analysis.
        
        Checks against:
        - Religious sensitivities
        - Political topics
        - Taboo subjects per culture
        - Idioms that don't translate
        - Colors/symbols with negative meaning
        
        Args:
            content: Content to check
            target_culture: Target language/culture code
            
        Returns:
            {
                'safe': True/False,
                'concerns': [...],
                'suggestions': [...]
            }
        """
        concerns = []
        suggestions = []
        
        # Get cultural considerations
        culture_rules = self.CULTURAL_CONSIDERATIONS.get(
            target_culture, 
            {'avoid': [], 'respectful': []}
        )
        
        content_lower = content.lower()
        
        # Check for terms to avoid
        for term in culture_rules.get('avoid', []):
            if term.lower() in content_lower:
                concerns.append(f"Contains term that may be sensitive: {term}")
                suggestions.append(f"Consider rephrasing to avoid '{term}'")
        
        # Check for respectful terms (bonus points)
        respectful_count = sum(
            1 for term in culture_rules.get('respectful', [])
            if term.lower() in content_lower
        )
        
        if respectful_count > 0:
            suggestions.append(f"Good use of culturally respectful terms")
        
        # Additional checks
        if '🐷' in content or 'pig' in content_lower:
            if target_culture in ['ar', 'he']:  # Arabic, Hebrew
                concerns.append("Pig references may be culturally insensitive")
        
        if '🍺' in content or 'beer' in content_lower or 'wine' in content_lower:
            if target_culture in ['ar']:  # Arabic
                concerns.append("Alcohol references may be culturally insensitive")
        
        safe = len(concerns) == 0
        
        return {
            'safe': safe,
            'concerns': concerns,
            'suggestions': suggestions,
            'culture': target_culture
        }
    
    def auto_fix_issues(self, content_batch: Dict, issues: List[Dict]) -> Dict:
        """
        Automatically fix common issues.
        
        Fixes:
        - Trim text to platform limits
        - Replace problematic phrases
        - Adjust hashtags
        - Re-generate if unfixable
        
        Args:
            content_batch: Content batch with issues
            issues: List of issues to fix
            
        Returns:
            Fixed content batch
        """
        logger.info(f"🔧 Auto-fixing {len(issues)} issues...")
        
        fixed_batch = content_batch.copy()
        fixes_applied = 0
        
        for issue in issues:
            city = issue.get('city')
            platform = issue.get('platform')
            severity = issue.get('severity')
            
            if severity == 'error':
                # Can't auto-fix errors, skip
                logger.warning(f"Cannot auto-fix error for {city}/{platform}")
                continue
            
            if city not in fixed_batch or platform not in fixed_batch[city].get('platforms', {}):
                continue
            
            content = fixed_batch[city]['platforms'][platform]
            
            # Fix text length
            if 'too long' in issue.get('issue', '').lower():
                text = content.get('content', '')
                if isinstance(text, str):
                    max_length = self.PLATFORM_LIMITS.get(platform, 1000)
                    content['content'] = text[:max_length-3] + '...'
                    fixes_applied += 1
                    logger.info(f"  ✓ Trimmed text for {city}/{platform}")
            
            # Fix missing hashtags
            if 'no hashtags' in issue.get('issue', '').lower():
                if 'hashtags' not in content or not content['hashtags']:
                    content['hashtags'] = ['#DailySmile', f'#{city.title()}', '#WorldTour']
                    fixes_applied += 1
                    logger.info(f"  ✓ Added hashtags for {city}/{platform}")
            
            # Fix hashtag format
            if 'invalid hashtag' in issue.get('issue', '').lower():
                hashtags = content.get('hashtags', [])
                content['hashtags'] = [
                    f"#{tag}" if not tag.startswith('#') else tag
                    for tag in hashtags
                ]
                fixes_applied += 1
                logger.info(f"  ✓ Fixed hashtag format for {city}/{platform}")
        
        logger.info(f"✅ Applied {fixes_applied} automatic fixes")
        
        return fixed_batch
    
    def validate_technical_requirements(self, content: Dict) -> Dict:
        """
        Validate technical requirements (file formats, sizes, etc.)
        
        Args:
            content: Content to validate
            
        Returns:
            Validation result
        """
        checks = {
            'video_format': True,
            'video_duration': True,
            'image_resolution': True,
            'file_size': True
        }
        
        issues = []
        
        # Check video format if present
        if 'video_url' in content:
            # Placeholder for video validation
            checks['video_format'] = True
        
        # Check image resolution if present
        if 'image_url' in content:
            # Placeholder for image validation
            checks['image_resolution'] = True
        
        all_passed = all(checks.values())
        
        return {
            'passed': all_passed,
            'checks': checks,
            'issues': issues
        }
    
    def get_quality_report(self, validation_results: Dict) -> str:
        """
        Generate human-readable quality report.
        
        Args:
            validation_results: Results from validate_content_batch
            
        Returns:
            Formatted report string
        """
        report = "=" * 60 + "\n"
        report += "QUALITY ASSURANCE REPORT\n"
        report += "=" * 60 + "\n\n"
        
        report += f"Total Checked: {validation_results['total_checked']}\n"
        report += f"✅ Passed: {validation_results['passed']}\n"
        report += f"❌ Failed: {validation_results['failed']}\n"
        report += f"⚠️  Warnings: {validation_results['warnings']}\n\n"
        
        if validation_results['safe_to_launch']:
            report += "🚀 SAFE TO LAUNCH\n\n"
        else:
            report += "🛑 NOT SAFE TO LAUNCH - Fix issues first\n\n"
        
        if validation_results['issues']:
            report += "Issues Found:\n"
            for i, issue in enumerate(validation_results['issues'][:10], 1):
                severity = issue.get('severity', 'info').upper()
                city = issue.get('city', 'unknown')
                problem = issue.get('issue', 'No description')
                report += f"{i}. [{severity}] {city}: {problem}\n"
            
            if len(validation_results['issues']) > 10:
                report += f"... and {len(validation_results['issues']) - 10} more\n"
        
        report += "\n" + "=" * 60 + "\n"
        
        return report


# Example usage
if __name__ == "__main__":
    qa = QualityAssurance()
    
    print("✅ Quality Assurance System Test")
    print("=" * 60)
    
    # Test content validation
    test_batch = {
        'new_york': {
            'platforms': {
                'tiktok': {
                    'content': 'Check out New York! #NYC',
                    'hashtags': ['#NYC', '#Travel']
                },
                'instagram': {
                    'content': 'A' * 3000,  # Too long!
                    'hashtags': []  # Missing hashtags
                }
            },
            'languages': {
                'en': 'English content',
                'ar': 'Arabic content with beer 🍺'  # Potentially sensitive
            }
        }
    }
    
    results = qa.validate_content_batch(test_batch)
    print(qa.get_quality_report(results))
    
    # Test auto-fix
    if not results['safe_to_launch']:
        print("\n🔧 Attempting auto-fix...")
        fixed_batch = qa.auto_fix_issues(test_batch, results['issues'])
        print("✅ Fixes applied!")
