"""
UMAJA WORLDTOUR - Bundle Builder
Smart pricing with bundle discounts and upsell engine
"""

from typing import Dict, List, Literal
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BundleBuilder:
    """
    Smart pricing with bundle discounts.
    Manages product tiers, dynamic pricing, and upsell recommendations.
    """
    
    # Product tiers and base prices (in EUR)
    PRODUCT_TIERS = {
        'text_only': {
            'name': 'Text Only',
            'description': 'Comedy text in personality style',
            'base_price': 1.50,
            'includes': ['text']
        },
        'audio_only': {
            'name': 'Audio Only',
            'description': 'Voice synthesis with personality',
            'base_price': 2.50,
            'includes': ['audio']
        },
        'text_audio': {
            'name': 'Text + Audio',
            'description': 'Complete audio experience with transcript',
            'base_price': 3.50,
            'includes': ['text', 'audio']
        },
        'image': {
            'name': 'Image/Quote Card',
            'description': 'Beautiful quote card or AI image',
            'base_price': 3.00,
            'includes': ['image']
        },
        'standard_bundle': {
            'name': 'Standard Bundle',
            'description': 'Text + Audio + Image',
            'base_price': 5.00,
            'includes': ['text', 'audio', 'image']
        },
        'worldtour_bundle': {
            'name': 'Worldtour Bundle',
            'description': 'Standard Bundle for a specific city',
            'base_price': 8.00,
            'includes': ['text', 'audio', 'image', 'city_specific']
        },
        'deluxe_video': {
            'name': 'Deluxe Video Package',
            'description': 'Complete multimedia: Text + Audio + Image + Video',
            'base_price': 12.00,
            'includes': ['text', 'audio', 'image', 'video']
        },
        'viral_kit': {
            'name': 'Viral Marketing Kit',
            'description': 'Everything + multiple formats + platform optimization',
            'base_price': 20.00,
            'includes': ['text', 'audio', 'image', 'video', 'multiple_platforms', 'optimization']
        }
    }
    
    # Extra add-ons
    EXTRAS = {
        'branding': {
            'name': 'Custom Branding',
            'description': 'Add your logo and branding',
            'price': 5.00
        },
        'commercial_license': {
            'name': 'Commercial License',
            'description': 'Use in commercial projects',
            'price': 10.00
        },
        'rush_delivery': {
            'name': 'Rush Delivery (24h)',
            'description': 'Priority processing within 24 hours',
            'price': 8.00
        },
        'extra_language': {
            'name': 'Extra Language',
            'description': 'Translation to another language',
            'price': 4.00
        },
        'extended_length': {
            'name': 'Extended Length',
            'description': 'Double the content length',
            'price': 6.00
        },
        'multiple_personalities': {
            'name': 'Multiple Personalities',
            'description': 'Get content from 2-3 different comedians',
            'price': 8.00
        }
    }
    
    # Discount tiers
    DISCOUNT_TIERS = {
        2: 0.10,  # 10% off for 2 items
        3: 0.15,  # 15% off for 3 items
        4: 0.20,  # 20% off for 4+ items
    }
    
    def __init__(self, charity_percentage: float = 0.40):
        """
        Initialize bundle builder.
        
        Args:
            charity_percentage: Percentage of profits to charity (0.0 to 1.0)
        """
        self.charity_percentage = charity_percentage
    
    def calculate_bundle_price(self,
                             items: List[str],
                             personality_count: int = 1,
                             extras: List[str] = None,
                             apply_discount: bool = True) -> Dict:
        """
        Calculate bundle price with discounts.
        
        Args:
            items: List of product tier IDs
            personality_count: Number of personalities (1-3)
            extras: List of extra add-on IDs
            apply_discount: Whether to apply volume discounts
            
        Returns:
            Dictionary with pricing breakdown
        """
        if extras is None:
            extras = []
        
        # Calculate base price
        base_total = Decimal('0.00')
        items_breakdown = []
        
        for item_id in items:
            if item_id not in self.PRODUCT_TIERS:
                logger.warning(f"Unknown product tier: {item_id}")
                continue
            
            tier = self.PRODUCT_TIERS[item_id]
            price = Decimal(str(tier['base_price']))
            
            items_breakdown.append({
                'id': item_id,
                'name': tier['name'],
                'base_price': float(price),
                'quantity': 1
            })
            
            base_total += price
        
        # Multiply by personality count if multiple personalities requested
        if personality_count > 1:
            base_total *= Decimal(str(personality_count))
            for item in items_breakdown:
                item['quantity'] = personality_count
        
        # Add extras
        extras_total = Decimal('0.00')
        extras_breakdown = []
        
        for extra_id in extras:
            if extra_id not in self.EXTRAS:
                logger.warning(f"Unknown extra: {extra_id}")
                continue
            
            extra = self.EXTRAS[extra_id]
            price = Decimal(str(extra['price']))
            
            extras_breakdown.append({
                'id': extra_id,
                'name': extra['name'],
                'price': float(price)
            })
            
            extras_total += price
        
        subtotal = base_total + extras_total
        
        # Apply volume discount
        discount_amount = Decimal('0.00')
        discount_percentage = 0.0
        
        if apply_discount and len(items) >= 2:
            # Get discount tier
            if len(items) >= 4:
                discount_percentage = self.DISCOUNT_TIERS[4]
            else:
                discount_percentage = self.DISCOUNT_TIERS.get(len(items), 0.0)
            
            discount_amount = base_total * Decimal(str(discount_percentage))
        
        # Calculate final total
        total = subtotal - discount_amount
        
        # Calculate charity allocation
        charity_amount = total * Decimal(str(self.charity_percentage))
        
        return {
            'items': items_breakdown,
            'extras': extras_breakdown,
            'base_total': float(base_total),
            'extras_total': float(extras_total),
            'subtotal': float(subtotal),
            'discount_percentage': discount_percentage * 100,
            'discount_amount': float(discount_amount),
            'total': float(total),
            'charity_amount': float(charity_amount),
            'charity_percentage': self.charity_percentage * 100,
            'currency': 'EUR',
            'savings_message': f"You save €{float(discount_amount):.2f}!" if discount_amount > 0 else None
        }
    
    def get_upsell_recommendations(self, current_items: List[str]) -> List[Dict]:
        """
        Get upsell recommendations based on current cart.
        
        Args:
            current_items: Current items in cart
            
        Returns:
            List of recommended upsells
        """
        recommendations = []
        current_set = set(current_items)
        
        # Recommend upgrades
        if 'text_only' in current_set:
            if 'audio_only' not in current_set:
                recommendations.append({
                    'type': 'upgrade',
                    'from': 'text_only',
                    'to': 'text_audio',
                    'message': "Add audio for just €2 more!",
                    'savings': 1.00
                })
        
        if 'text_audio' in current_set:
            if 'image' not in current_set:
                recommendations.append({
                    'type': 'add',
                    'item': 'image',
                    'message': "Complete the experience with a stunning image!",
                    'bundle_offer': 'standard_bundle'
                })
        
        if 'standard_bundle' in current_set:
            recommendations.append({
                'type': 'upgrade',
                'from': 'standard_bundle',
                'to': 'deluxe_video',
                'message': "Upgrade to video for maximum impact!",
                'savings': 6.00
            })
        
        # Recommend extras
        if len(current_items) >= 2:
            if 'commercial_license' not in current_set:
                recommendations.append({
                    'type': 'extra',
                    'item': 'commercial_license',
                    'message': "Planning to use this commercially? Add a license!"
                })
        
        # Recommend multiple personalities
        if len(current_items) >= 1:
            recommendations.append({
                'type': 'extra',
                'item': 'multiple_personalities',
                'message': "Get 3 different takes on your topic!"
            })
        
        return recommendations
    
    def create_custom_bundle(self, 
                           content_types: List[Literal['text', 'audio', 'image', 'video']],
                           extras: List[str] = None) -> str:
        """
        Create a custom bundle based on content types.
        
        Args:
            content_types: List of content types wanted
            extras: List of extras
            
        Returns:
            Recommended product tier ID
        """
        if extras is None:
            extras = []
        
        content_set = set(content_types)
        
        # Match to existing tiers
        if content_set == {'text'}:
            return 'text_only'
        elif content_set == {'audio'}:
            return 'audio_only'
        elif content_set == {'text', 'audio'}:
            return 'text_audio'
        elif content_set == {'image'}:
            return 'image'
        elif content_set == {'text', 'audio', 'image'}:
            return 'standard_bundle'
        elif content_set == {'text', 'audio', 'image', 'video'}:
            return 'deluxe_video'
        else:
            # Custom combination - recommend closest tier
            if 'video' in content_set:
                return 'deluxe_video'
            elif len(content_set) >= 3:
                return 'standard_bundle'
            elif 'audio' in content_set and 'text' in content_set:
                return 'text_audio'
            else:
                return 'text_only'
    
    def get_popular_bundles(self) -> List[Dict]:
        """Get list of most popular bundles."""
        popular = [
            'standard_bundle',
            'worldtour_bundle',
            'deluxe_video',
            'text_audio'
        ]
        
        return [
            {
                'id': tier_id,
                **self.PRODUCT_TIERS[tier_id],
                'recommended': True
            }
            for tier_id in popular
        ]
    
    def calculate_savings_comparison(self, bundle_id: str) -> Dict:
        """
        Calculate how much a bundle saves vs buying items individually.
        
        Args:
            bundle_id: Bundle tier ID
            
        Returns:
            Savings comparison
        """
        if bundle_id not in self.PRODUCT_TIERS:
            raise ValueError(f"Unknown bundle: {bundle_id}")
        
        bundle = self.PRODUCT_TIERS[bundle_id]
        bundle_price = Decimal(str(bundle['base_price']))
        
        # Calculate individual prices
        individual_total = Decimal('0.00')
        
        if 'text' in bundle['includes']:
            individual_total += Decimal(str(self.PRODUCT_TIERS['text_only']['base_price']))
        if 'audio' in bundle['includes']:
            individual_total += Decimal(str(self.PRODUCT_TIERS['audio_only']['base_price']))
        if 'image' in bundle['includes']:
            individual_total += Decimal(str(self.PRODUCT_TIERS['image']['base_price']))
        
        savings = individual_total - bundle_price
        savings_percentage = (savings / individual_total * 100) if individual_total > 0 else 0
        
        return {
            'bundle_id': bundle_id,
            'bundle_name': bundle['name'],
            'bundle_price': float(bundle_price),
            'individual_total': float(individual_total),
            'savings': float(savings),
            'savings_percentage': float(savings_percentage),
            'message': f"Save €{float(savings):.2f} ({float(savings_percentage):.0f}%) with this bundle!"
        }


# Example usage and testing
if __name__ == "__main__":
    builder = BundleBuilder()
    
    print("Bundle Builder Test")
    print("=" * 60)
    
    # Test standard bundle
    print("\nStandard Bundle (Text + Audio + Image):")
    result = builder.calculate_bundle_price(['standard_bundle'])
    print(f"  Base: €{result['base_total']:.2f}")
    print(f"  Total: €{result['total']:.2f}")
    print(f"  To charity: €{result['charity_amount']:.2f} ({result['charity_percentage']:.0f}%)")
    
    # Test multiple items with discount
    print("\nMultiple Items (3+ items get 15% off):")
    result = builder.calculate_bundle_price(['text_audio', 'image', 'video'])
    print(f"  Subtotal: €{result['subtotal']:.2f}")
    print(f"  Discount: -{result['discount_percentage']:.0f}% (€{result['discount_amount']:.2f})")
    print(f"  Total: €{result['total']:.2f}")
    
    # Test with extras
    print("\nDeluxe Video + Extras:")
    result = builder.calculate_bundle_price(
        ['deluxe_video'],
        extras=['commercial_license', 'rush_delivery']
    )
    print(f"  Base: €{result['base_total']:.2f}")
    print(f"  Extras: €{result['extras_total']:.2f}")
    print(f"  Total: €{result['total']:.2f}")
    
    # Test upsell recommendations
    print("\nUpsell Recommendations for text_only:")
    recommendations = builder.get_upsell_recommendations(['text_only'])
    for rec in recommendations:
        print(f"  - {rec['message']}")
    
    # Test savings comparison
    print("\nSavings Comparison for Standard Bundle:")
    savings = builder.calculate_savings_comparison('standard_bundle')
    print(f"  {savings['message']}")
