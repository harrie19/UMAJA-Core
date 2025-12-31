"""
Passive Discovery Agent
Makes UMAJA-Core discoverable through organic channels

Philosophy:
- Lighthouse approach: Signal availability, don't push
- Water approach: Fill gaps where needed, don't force
- Bahá'í: Available, not aggressive
- Ubuntu: "I am because we are" - serve those who seek
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class PassiveDiscoveryAgent:
    """
    Lighthouse approach: Signal availability, don't push
    Water approach: Fill gaps where needed, don't force
    """

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.registry_file = self.project_root / "data" / "public_registry.json"

    def create_structured_metadata(self) -> Dict[str, Any]:
        """
        Generate machine-readable metadata:
        - Schema.org markup
        - OpenGraph tags
        - Twitter cards
        - GitHub social preview
        """
        metadata = {
            "schema_org": {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": "UMAJA-Core",
                "description": (
                    "Bahá'í-inspired AI system for bringing smiles to "
                    "all 8 billion people"
                ),
                "applicationCategory": "AI Ethics, NLP",
                "operatingSystem": "Cross-platform",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "author": {"@type": "Person", "name": "Marek Grischa Engel"},
                "keywords": (
                    "AI ethics, hallucination mitigation, Bahá'í principles, "
                    "vector embeddings"
                ),
                "license": "https://opensource.org/licenses/MIT",
                "codeRepository": "https://github.com/harrie19/UMAJA-Core",
            },
            "open_graph": {
                "og:title": "UMAJA-Core: AI Truth Framework",
                "og:description": (
                    "Bahá'í-inspired AI bringing smiles to 8 billion people"
                ),
                "og:type": "website",
                "og:url": "https://github.com/harrie19/UMAJA-Core",
                "og:site_name": "UMAJA-Core",
            },
            "twitter_card": {
                "twitter:card": "summary_large_image",
                "twitter:title": "UMAJA-Core: AI Truth Framework",
                "twitter:description": "Bahá'í-inspired AI for unity through joy",
            },
        }
        return metadata

    def generate_discovery_manifest(self) -> Dict[str, Any]:
        """
        Public manifest for AI-to-AI discovery
        """
        manifest = {
            "project": "UMAJA-Core",
            "mission": "Bring smiles to all 8 billion people",
            "principles": ["truth", "service", "unity"],
            "keywords": [
                "ai-ethics",
                "hallucination-mitigation",
                "bahai",
                "value-alignment",
                "vector-embeddings",
            ],
            "findable_via": ["github-topics", "academic-citations", "api"],
            "contact": "organic-only",
            "philosophy": "Lighthouse, not megaphone",
        }
        return manifest

    def optimize_for_search(self) -> Dict[str, List[str]]:
        """
        SEO-friendly (not manipulative):
        - Clear keywords in docs
        - Proper heading structure
        - Academic terminology
        - Use case examples
        """
        keywords = {
            "research_terms": [
                "AI hallucination mitigation",
                "value alignment practical implementation",
                "Bahá'í principles in AI architecture",
                "truth-first AI systems",
            ],
            "developer_terms": [
                "vector embeddings for unity measurement",
                "semantic coherence analysis",
                "sentence transformers",
                "personality engine",
            ],
            "ethics_terms": [
                "spiritual principles in AI",
                "religious philosophy as AI constraint",
                "Ubuntu philosophy in technology",
                "non-pushy AI discovery",
            ],
        }
        return keywords

    def save_registry(self, registry_data: Dict[str, Any]) -> None:
        """
        Save public registry to JSON file
        """
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(registry_data, f, indent=2, ensure_ascii=False)

    def load_registry(self) -> Dict[str, Any]:
        """
        Load existing registry or return empty dict
        """
        if self.registry_file.exists():
            with open(self.registry_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def generate_full_registry(self) -> Dict[str, Any]:
        """
        Generate complete public registry
        """
        registry = {
            "project": {
                "name": "UMAJA-Core",
                "version": "3.0.0",
                "mission": "Bring smiles to all 8 billion people on Earth",
                "tagline": "Bahá'í-inspired AI for unity through joy",
            },
            "discovery": {
                "keywords": [
                    "ai-ethics",
                    "ai-safety",
                    "hallucination-mitigation",
                    "value-alignment",
                    "bahai-principles",
                    "vector-embeddings",
                    "semantic-coherence",
                    "truth-framework",
                ],
                "github_topics": [
                    "ai-ethics",
                    "ai-safety",
                    "machine-learning",
                    "nlp",
                    "sentence-transformers",
                    "open-source-ai",
                ],
                "research_areas": [
                    "AI hallucination mitigation",
                    "Value alignment in practice",
                    "Religious principles in AI architecture",
                    "Vector-based unity measurement",
                ],
            },
            "principles": {
                "truth_over_optimization": (
                    "Reality over fantasy. Honest numbers over hype."
                ),
                "service_not_profit": ("Success = lives touched, not dollars earned."),
                "unity_of_humanity": (
                    "No division by race, religion, nationality, class."
                ),
                "open_source_free": (
                    "All code public. All content free. " "All channels simultaneous."
                ),
            },
            "contact": {
                "method": "organic_discovery_only",
                "github": "https://github.com/harrie19/UMAJA-Core",
                "approach": "We don't cold-contact. Find us if you need us.",
                "philosophy": "Lighthouse, not megaphone",
            },
            "verification": {
                "code": "https://github.com/harrie19/UMAJA-Core",
                "history": "All commits timestamped and public",
                "proof": "6 weeks of development documented in Git history",
            },
        }
        return registry


def main():
    """
    Generate and save discovery infrastructure
    """
    agent = PassiveDiscoveryAgent()

    # Generate full registry
    registry = agent.generate_full_registry()

    # Save to file
    agent.save_registry(registry)

    print("✅ Public registry generated")
    print(f"📁 Saved to: {agent.registry_file}")
    print("\n🌊 Gentle Waves Discovery System active")
    print("💡 Lighthouse approach: Signaling, not pushing")


if __name__ == "__main__":
    main()
