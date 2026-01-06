"""
UMAJA Freemium Model - Social Responsibility Pricing
"""

from typing import Dict, Optional
from enum import Enum


class UserType(Enum):
    FREE_FOREVER = "free_forever"  # Beta, students, children, NGOs
    FREE_TIER = "free_tier"
    PRO_INDIVIDUAL = "pro_individual"
    PRO_BUSINESS = "pro_business"
    ENTERPRISE = "enterprise"


class FreemiumModel:
    """Social responsibility pricing"""
    
    PRICING = {
        UserType.FREE_FOREVER: {
            'price': 0,
            'who': ['Beta users', 'Children', 'Students', 'Teachers', 'NGOs'],
            'features': 'All core features',
            'limits': {'daily_generations': 50}
        },
        UserType.FREE_TIER: {
            'price': 0,
            'who': ['General users'],
            'features': 'Basic features',
            'limits': {'daily_generations': 10}
        },
        UserType.PRO_INDIVIDUAL: {
            'price': 9.99,
            'who': ['Individuals', 'Freelancers'],
            'features': 'Everything + API + Priority',
            'limits': {'daily_generations': 500}
        },
        UserType.PRO_BUSINESS: {
            'price': 99.99,
            'who': ['Companies', 'Agencies'],
            'features': 'Everything + Teams + White-label',
            'limits': {'daily_generations': 5000}
        },
        UserType.ENTERPRISE: {
            'price': 'custom',
            'who': ['Large organizations'],
            'features': 'Everything + Custom + Dedicated support',
            'limits': {'daily_generations': 'unlimited'}
        }
    }
    
    def classify_user(self, email: Optional[str] = None, 
                     is_beta: bool = False,
                     age: Optional[int] = None) -> UserType:
        """Auto-classify user type"""
        if is_beta:
            return UserType.FREE_FOREVER
        if age and age < 18:
            return UserType.FREE_FOREVER
        if email and any(d in email for d in ['.edu', '.ac.', 'school']):
            return UserType.FREE_FOREVER
        return UserType.FREE_TIER
    
    def get_pricing_info(self, user_type: UserType) -> Dict:
        """Get pricing information for a user type"""
        return self.PRICING.get(user_type, self.PRICING[UserType.FREE_TIER])
    
    def check_limit(self, user_type: UserType, usage: int, limit_type: str = 'daily_generations') -> bool:
        """Check if user has exceeded their limit"""
        pricing = self.PRICING.get(user_type, self.PRICING[UserType.FREE_TIER])
        limit = pricing['limits'].get(limit_type, 0)
        
        if limit == 'unlimited':
            return True
        
        return usage < limit
