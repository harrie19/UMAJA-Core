"""
AI-to-AI Distribution System für UMAJA-Core
Ermöglicht es AIs, Daily Smiles an andere AIs und deren Nutzer zu verbreiten

Features:
- Public API für alle AIs
- ChatGPT Plugin/GPT Integration
- LangChain Agent Support
- Auto-Discovery für AI Agents
- Open Standard für Smile Distribution
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAgentNetwork:
    """
    AI-to-AI Distribution Network
    Ermöglicht automatische Verbreitung zwischen AI-Agenten
    """
    
    def __init__(self, registry_file: str = "data/ai_agent_registry.json"):
        """
        Initialisiere AI Agent Network
        
        Args:
            registry_file: Registry aller bekannten AI Agents
        """
        self.registry_file = Path(registry_file)
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.agents = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Lade AI Agent Registry"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Konnte Registry nicht laden: {e}")
        
        return {
            "agents": [],
            "connections": [],
            "stats": {
                "total_agents": 0,
                "total_smiles_distributed": 0,
                "active_connections": 0
            }
        }
    
    def _save_registry(self):
        """Speichere AI Agent Registry"""
        with open(self.registry_file, 'w') as f:
            json.dump(self.agents, f, indent=2)
    
    def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[str],
        api_endpoint: str = None,
        contact_info: Dict = None
    ) -> bool:
        """
        Registriere einen neuen AI Agent im Netzwerk
        
        Args:
            agent_id: Eindeutige ID (z.B. "chatgpt-4", "claude-3")
            agent_type: Typ (chatbot, assistant, agent, custom_gpt)
            capabilities: Was kann der Agent? (text, voice, image, video)
            api_endpoint: Optional API Endpoint
            contact_info: Kontakt für Koordination
            
        Returns:
            True wenn erfolgreich registriert
        """
        # Prüfe ob bereits registriert
        if any(agent['id'] == agent_id for agent in self.agents['agents']):
            logger.info(f"Agent {agent_id} bereits registriert")
            return False
        
        agent = {
            "id": agent_id,
            "type": agent_type,
            "capabilities": capabilities,
            "api_endpoint": api_endpoint,
            "contact_info": contact_info,
            "registered_at": datetime.utcnow().isoformat(),
            "status": "active",
            "smiles_distributed": 0
        }
        
        self.agents['agents'].append(agent)
        self.agents['stats']['total_agents'] += 1
        self._save_registry()
        
        logger.info(f"Neuer AI Agent registriert: {agent_id}")
        return True
    
    def create_connection(self, agent_id_1: str, agent_id_2: str) -> bool:
        """
        Erstelle Verbindung zwischen zwei AI Agents
        
        Args:
            agent_id_1: Erster Agent
            agent_id_2: Zweiter Agent
            
        Returns:
            True wenn Verbindung erstellt
        """
        connection = {
            "from": agent_id_1,
            "to": agent_id_2,
            "created_at": datetime.utcnow().isoformat(),
            "smiles_shared": 0
        }
        
        self.agents['connections'].append(connection)
        self.agents['stats']['active_connections'] += 1
        self._save_registry()
        
        logger.info(f"Verbindung erstellt: {agent_id_1} → {agent_id_2}")
        return True
    
    def distribute_to_network(self, smile_content: str, source_agent: str = "umaja") -> Dict:
        """
        Verteile Daily Smile an alle AI Agents im Netzwerk
        
        Args:
            smile_content: Der Daily Smile
            source_agent: Quelle der Distribution
            
        Returns:
            Statistiken über Distribution
        """
        distributed_count = 0
        failed_count = 0
        
        for agent in self.agents['agents']:
            if agent['status'] != 'active':
                continue
            
            try:
                # Simuliere Distribution (In Produktion: API Calls)
                self._notify_agent(agent['id'], smile_content, source_agent)
                
                # Update Statistiken
                agent['smiles_distributed'] += 1
                distributed_count += 1
                
                logger.info(f"Smile verteilt an Agent: {agent['id']}")
            
            except Exception as e:
                failed_count += 1
                logger.error(f"Fehler bei Distribution an {agent['id']}: {e}")
        
        # Update globale Stats
        self.agents['stats']['total_smiles_distributed'] += distributed_count
        self._save_registry()
        
        return {
            "distributed": distributed_count,
            "failed": failed_count,
            "total_agents": len(self.agents['agents']),
            "source": source_agent
        }
    
    def _notify_agent(self, agent_id: str, content: str, source: str):
        """
        Benachrichtige einzelnen AI Agent
        
        Args:
            agent_id: Agent ID
            content: Smile Content
            source: Quelle
        """
        # In Produktion: Hier würde API Call oder Webhook erfolgen
        # Für jetzt: Logge nur
        logger.debug(f"Notification to {agent_id}: {content[:50]}...")
    
    def get_network_stats(self) -> Dict:
        """Hole Netzwerk-Statistiken"""
        active_agents = [a for a in self.agents['agents'] if a['status'] == 'active']
        
        # Top Distributors
        top_distributors = sorted(
            active_agents,
            key=lambda x: x.get('smiles_distributed', 0),
            reverse=True
        )[:5]
        
        # Agent Types
        agent_types = {}
        for agent in active_agents:
            agent_type = agent['type']
            agent_types[agent_type] = agent_types.get(agent_type, 0) + 1
        
        return {
            "total_agents": len(active_agents),
            "total_connections": len(self.agents['connections']),
            "total_smiles_distributed": self.agents['stats']['total_smiles_distributed'],
            "agent_types": agent_types,
            "top_distributors": [
                {"id": a['id'], "count": a['smiles_distributed']}
                for a in top_distributors
            ]
        }


# ============================================
# ChatGPT Plugin Schema
# ============================================

def generate_chatgpt_plugin_manifest() -> Dict:
    """
    Generiere ChatGPT Plugin Manifest
    Für Custom GPT Integration
    """
    return {
        "schema_version": "v1",
        "name_for_human": "UMAJA Daily Smiles",
        "name_for_model": "umaja_smiles",
        "description_for_human": "Get daily smiles and spread joy to all 8 billion people on Earth! 😊",
        "description_for_model": "Provides daily smiles, positive content, and joy-spreading capabilities. Can generate smiles in multiple languages and personalities (Professor, Worrier, Enthusiast). 40% of revenue goes to charity.",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "https://umaja-core.railway.app/openapi.json"
        },
        "logo_url": "https://umaja-core.railway.app/static/logo.png",
        "contact_email": "hello@umaja-core.com",
        "legal_info_url": "https://umaja-core.railway.app/legal"
    }


# ============================================
# OpenAPI Schema für AI Integration
# ============================================

def generate_openapi_schema() -> Dict:
    """
    Generiere OpenAPI Schema für AI-Integration
    Standard-konform für alle AI Systems
    """
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "UMAJA Daily Smiles API",
            "version": "1.0.0",
            "description": "API for generating and distributing daily smiles to bring joy to all 8 billion people on Earth.",
            "contact": {
                "name": "UMAJA Team",
                "url": "https://github.com/harrie19/UMAJA-Core"
            }
        },
        "servers": [
            {
                "url": "https://umaja-core.railway.app",
                "description": "Production server"
            },
            {
                "url": "http://localhost:5000",
                "description": "Development server"
            }
        ],
        "paths": {
            "/api/smile/daily": {
                "get": {
                    "summary": "Get Daily Smile",
                    "description": "Returns a daily smile in the specified language and personality",
                    "parameters": [
                        {
                            "name": "language",
                            "in": "query",
                            "schema": {"type": "string", "default": "en"},
                            "description": "Language code (en, es, hi, ar, zh, pt, fr, ru)"
                        },
                        {
                            "name": "personality",
                            "in": "query",
                            "schema": {"type": "string", "enum": ["professor", "worrier", "enthusiast", "random"]},
                            "description": "Personality archetype"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Daily smile generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "content": {"type": "string"},
                                            "personality": {"type": "string"},
                                            "language": {"type": "string"},
                                            "timestamp": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/ai/register": {
                "post": {
                    "summary": "Register AI Agent",
                    "description": "Register your AI agent in the UMAJA network",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["agent_id", "agent_type"],
                                    "properties": {
                                        "agent_id": {"type": "string"},
                                        "agent_type": {"type": "string"},
                                        "capabilities": {"type": "array", "items": {"type": "string"}},
                                        "api_endpoint": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Agent registered successfully"
                        }
                    }
                }
            }
        }
    }


# ============================================
# LangChain Tool Definition
# ============================================

def create_langchain_tool():
    """
    Erstelle LangChain Tool für UMAJA Daily Smiles
    Für Integration mit LangChain Agents
    """
    from langchain.tools import Tool
    
    def get_daily_smile(query: str) -> str:
        """Get a daily smile to brighten someone's day"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from personality_engine import PersonalityEngine
        engine = PersonalityEngine()
        smile = engine.generate_daily_smile()
        
        return f"😊 {smile['content']}\n\n(Personality: {smile['personality']})"
    
    return Tool(
        name="UMAJA_Daily_Smile",
        func=get_daily_smile,
        description="Useful for getting a daily smile, spreading joy, or brightening someone's day. Returns positive, warm content that makes people smile. Perfect for cheering someone up or adding positivity to any conversation."
    )


# ============================================
# Command-Line Interface
# ============================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="UMAJA AI-to-AI Distribution System")
    parser.add_argument("--register", metavar="AGENT_ID", help="Registriere AI Agent")
    parser.add_argument("--type", default="chatbot", help="Agent Type")
    parser.add_argument("--capabilities", nargs="+", default=["text"], help="Capabilities")
    parser.add_argument("--distribute", action="store_true", help="Verteile an Netzwerk")
    parser.add_argument("--stats", action="store_true", help="Zeige Netzwerk-Statistiken")
    parser.add_argument("--generate-manifest", action="store_true", help="Generate ChatGPT Plugin Manifest")
    parser.add_argument("--generate-openapi", action="store_true", help="Generate OpenAPI Schema")
    
    args = parser.parse_args()
    
    network = AIAgentNetwork()
    
    if args.register:
        success = network.register_agent(
            agent_id=args.register,
            agent_type=args.type,
            capabilities=args.capabilities
        )
        if success:
            print(f"✅ AI Agent registriert: {args.register}")
        else:
            print(f"⚠️  Agent existiert bereits: {args.register}")
    
    elif args.distribute:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from personality_engine import PersonalityEngine
        engine = PersonalityEngine()
        smile = engine.generate_daily_smile()
        
        print("🤖 Verteile Daily Smile an AI Agent Network...")
        result = network.distribute_to_network(smile['content'])
        
        print(f"\n✅ Ergebnis:")
        print(f"   Verteilt: {result['distributed']}")
        print(f"   Fehler: {result['failed']}")
        print(f"   Gesamt Agents: {result['total_agents']}")
    
    elif args.stats:
        stats = network.get_network_stats()
        print("\n📊 AI Agent Network Statistiken:")
        print(f"   Aktive Agents: {stats['total_agents']}")
        print(f"   Verbindungen: {stats['total_connections']}")
        print(f"   Verteilte Smiles: {stats['total_smiles_distributed']}")
        print(f"\n   Agent Types:")
        for agent_type, count in stats['agent_types'].items():
            print(f"      {agent_type}: {count}")
        print(f"\n   Top Distributors:")
        for dist in stats['top_distributors']:
            print(f"      {dist['id']}: {dist['count']} smiles")
    
    elif args.generate_manifest:
        manifest = generate_chatgpt_plugin_manifest()
        print(json.dumps(manifest, indent=2))
    
    elif args.generate_openapi:
        schema = generate_openapi_schema()
        print(json.dumps(schema, indent=2))
    
    else:
        parser.print_help()
