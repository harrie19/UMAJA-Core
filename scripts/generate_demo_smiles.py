"""Generate 3 demo smiles for launch"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_daily_smile import DailySmileGenerator


def generate_launch_demos():
    generator = DailySmileGenerator()
    
    # Create output directory
    output_dir = Path("output/demos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cities = ['new_york', 'tokyo', 'paris']
    demos = []
    
    for city_id in cities:
        # Override next city temporarily
        generator.worldtour.override_next(city_id)
        smile = generator.generate_daily_smile()
        demos.append(smile)
        
        # Save to output/demos/
        output_path = output_dir / f"{city_id}_smile.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"City: {smile['city']['name']}\n")
            f.write(f"Personality: {smile['personality']}\n")
            f.write(f"Topic: {smile['topic']}\n")
            f.write(f"\n{'-'*60}\n\n")
            f.write(smile['text'])
            f.write(f"\n\n{'-'*60}\n\n")
            f.write(f"Hashtags: {' '.join(smile['hashtags'])}\n")
        
        print(f"✅ Generated demo for {city_id}")
    
    return demos


if __name__ == '__main__':
    demos = generate_launch_demos()
    print(f"\n🎉 3 demo smiles ready in output/demos/")
    print("\nDemo summaries:")
    for demo in demos:
        print(f"\n  📍 {demo['city']['name']}")
        print(f"     🎭 {demo['personality']}")
        print(f"     📝 {demo['topic']}")
