"""
🤖 Autonomous Agent System für UMAJA-Core
Erstellt und verwaltet autonome Agenten, die parallel arbeiten

Dieses System ermöglicht:
- Erstellung von Worker-Agenten für verschiedene Aufgaben
- Parallele Ausführung (skalierbar)
- Task Queue Management
- Agent Monitoring und Health Checks
- Auto-Scaling basierend auf Last
"""

import json
import time
import threading
import queue
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Typen von Agenten"""
    CONTENT_GENERATOR = "content_generator"  # Erstellt Daily Smiles
    WORLD_TOUR_GUIDE = "worldtour_guide"     # Führt World Tour durch
    DISTRIBUTOR = "distributor"              # Verteilt Content
    TRANSLATOR = "translator"                # Übersetzt Content
    QUALITY_CHECKER = "quality_checker"      # Prüft Qualität
    SOCIAL_MEDIA_POSTER = "social_poster"    # Posted auf Social Media
    EMAIL_SENDER = "email_sender"            # Sendet Emails
    SMS_SENDER = "sms_sender"                # Sendet SMS
    ANALYTICS = "analytics"                  # Analysiert Engagement


class TaskStatus(Enum):
    """Status von Tasks"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class Task:
    """Eine Aufgabe für einen Agenten"""
    id: str
    type: str
    agent_type: AgentType
    data: Dict[str, Any]
    priority: int = 5  # 1-10, höher = wichtiger
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = None
    started_at: str = None
    completed_at: str = None
    result: Any = None
    error: str = None
    retries: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()
    
    def __lt__(self, other):
        """Vergleichsoperator für PriorityQueue"""
        return self.priority > other.priority  # Höhere Priorität = wichtiger


@dataclass
class Agent:
    """Ein autonomer Agent"""
    id: str
    type: AgentType
    status: str = "idle"  # idle, working, error, stopped
    tasks_completed: int = 0
    tasks_failed: int = 0
    created_at: str = None
    last_heartbeat: str = None
    current_task: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


class AgentOrchestrator:
    """
    Zentraler Orchestrator für autonome Agenten
    Verwaltet Agent Pool, Task Queue, Monitoring
    """
    
    def __init__(self, data_dir: str = "data/agents"):
        """
        Initialisiere Agent Orchestrator
        
        Args:
            data_dir: Verzeichnis für Agent-Daten
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Task Queue (Thread-safe)
        self.task_queue = queue.PriorityQueue()
        
        # Agent Pool
        self.agents: Dict[str, Agent] = {}
        self.agent_threads: Dict[str, threading.Thread] = {}
        
        # Statistics
        self.stats = {
            "total_agents": 0,
            "active_agents": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "started_at": datetime.utcnow().isoformat()
        }
        
        # Task handlers (registrierte Funktionen für Task-Typen)
        self.task_handlers: Dict[str, Callable] = {}
        
        # Lade gespeicherte Daten
        self._load_state()
        
        logger.info("🤖 Agent Orchestrator initialisiert")
    
    def register_task_handler(self, task_type: str, handler: Callable):
        """
        Registriere einen Handler für einen Task-Typ
        
        Args:
            task_type: Typ der Task (z.B. "generate_smile")
            handler: Funktion die Task ausführt
        """
        self.task_handlers[task_type] = handler
        logger.info(f"Handler für '{task_type}' registriert")
    
    def create_agent(self, agent_type: AgentType) -> str:
        """
        Erstelle einen neuen autonomen Agenten
        
        Args:
            agent_type: Typ des Agenten
            
        Returns:
            Agent ID
        """
        agent_id = f"{agent_type.value}_{len(self.agents) + 1}_{int(time.time())}"
        
        agent = Agent(
            id=agent_id,
            type=agent_type
        )
        
        self.agents[agent_id] = agent
        self.stats["total_agents"] += 1
        
        logger.info(f"✅ Agent erstellt: {agent_id} (Type: {agent_type.value})")
        
        return agent_id
    
    def start_agent(self, agent_id: str):
        """
        Starte einen Agenten (in eigenem Thread)
        
        Args:
            agent_id: ID des Agenten
        """
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} nicht gefunden")
            return False
        
        if agent_id in self.agent_threads and self.agent_threads[agent_id].is_alive():
            logger.warning(f"Agent {agent_id} läuft bereits")
            return False
        
        # Starte Agent Thread
        thread = threading.Thread(
            target=self._agent_worker,
            args=(agent_id,),
            daemon=True
        )
        thread.start()
        
        self.agent_threads[agent_id] = thread
        self.stats["active_agents"] += 1
        
        logger.info(f"🚀 Agent gestartet: {agent_id}")
        
        return True
    
    def _agent_worker(self, agent_id: str):
        """
        Worker-Funktion für Agent (läuft in eigenem Thread)
        
        Args:
            agent_id: ID des Agenten
        """
        agent = self.agents[agent_id]
        agent.status = "idle"
        
        logger.info(f"🤖 Agent {agent_id} wartet auf Tasks...")
        
        while agent.status != "stopped":
            try:
                # Hole nächste Task aus Queue (mit Timeout)
                try:
                    task = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    # Keine Task verfügbar, heartbeat und weitermachen
                    agent.last_heartbeat = datetime.utcnow().isoformat()
                    continue
                
                # Prüfe ob Agent für diesen Task-Typ zuständig ist
                if task.agent_type != agent.type:
                    # Task zurück in Queue (falscher Agent)
                    self.task_queue.put(task)
                    continue
                
                # Führe Task aus
                agent.status = "working"
                agent.current_task = task.id
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.utcnow().isoformat()
                
                logger.info(f"▶️  Agent {agent_id} arbeitet an Task {task.id}")
                
                try:
                    # Führe Task Handler aus
                    if task.type in self.task_handlers:
                        result = self.task_handlers[task.type](task.data)
                        task.result = result
                        task.status = TaskStatus.COMPLETED
                        agent.tasks_completed += 1
                        self.stats["completed_tasks"] += 1
                        
                        logger.info(f"✅ Task {task.id} abgeschlossen von {agent_id}")
                    else:
                        raise Exception(f"Kein Handler für Task-Typ '{task.type}'")
                
                except Exception as e:
                    logger.error(f"❌ Task {task.id} fehlgeschlagen: {e}")
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    agent.tasks_failed += 1
                    self.stats["failed_tasks"] += 1
                    
                    # Retry?
                    if task.retries < task.max_retries:
                        task.retries += 1
                        task.status = TaskStatus.RETRY
                        self.task_queue.put(task)
                        logger.info(f"🔄 Task {task.id} wird wiederholt (Versuch {task.retries})")
                
                finally:
                    task.completed_at = datetime.utcnow().isoformat()
                    agent.status = "idle"
                    agent.current_task = None
                    agent.last_heartbeat = datetime.utcnow().isoformat()
            
            except Exception as e:
                logger.error(f"Fehler in Agent {agent_id}: {e}")
                agent.status = "error"
                time.sleep(5)  # Warte vor Retry
                agent.status = "idle"
        
        logger.info(f"🛑 Agent {agent_id} gestoppt")
        self.stats["active_agents"] -= 1
    
    def add_task(
        self,
        task_type: str,
        agent_type: AgentType,
        data: Dict[str, Any],
        priority: int = 5
    ) -> str:
        """
        Füge eine neue Task zur Queue hinzu
        
        Args:
            task_type: Typ der Task
            agent_type: Welcher Agent-Typ soll diese Task ausführen
            data: Task-Daten
            priority: Priorität (1-10, höher = wichtiger)
            
        Returns:
            Task ID
        """
        task_id = f"task_{int(time.time())}_{self.stats['total_tasks']}"
        
        task = Task(
            id=task_id,
            type=task_type,
            agent_type=agent_type,
            data=data,
            priority=priority
        )
        
        # Task mit Priority in Queue (Task hat __lt__ für Vergleich)
        self.task_queue.put(task)
        
        self.stats["total_tasks"] += 1
        
        logger.info(f"📝 Task hinzugefügt: {task_id} (Type: {task_type}, Priority: {priority})")
        
        return task_id
    
    def stop_agent(self, agent_id: str):
        """
        Stoppe einen Agenten
        
        Args:
            agent_id: ID des Agenten
        """
        if agent_id in self.agents:
            self.agents[agent_id].status = "stopped"
            logger.info(f"🛑 Agent {agent_id} wird gestoppt...")
    
    def stop_all_agents(self):
        """Stoppe alle Agenten"""
        logger.info("🛑 Stoppe alle Agenten...")
        for agent_id in self.agents:
            self.stop_agent(agent_id)
    
    def get_status(self) -> Dict:
        """
        Hole aktuellen Status des Systems
        
        Returns:
            Status Dictionary
        """
        return {
            "stats": self.stats,
            "agents": {
                agent_id: {
                    "type": agent.type.value,
                    "status": agent.status,
                    "tasks_completed": agent.tasks_completed,
                    "tasks_failed": agent.tasks_failed,
                    "current_task": agent.current_task
                }
                for agent_id, agent in self.agents.items()
            },
            "queue_size": self.task_queue.qsize()
        }
    
    def scale_agents(self, agent_type: AgentType, count: int):
        """
        Skaliere Agenten eines Typs
        
        Args:
            agent_type: Typ der Agenten
            count: Gewünschte Anzahl
        """
        current_count = sum(
            1 for agent in self.agents.values()
            if agent.type == agent_type and agent.status != "stopped"
        )
        
        if count > current_count:
            # Erstelle neue Agenten
            for _ in range(count - current_count):
                agent_id = self.create_agent(agent_type)
                self.start_agent(agent_id)
            
            logger.info(f"📈 Skaliert: {agent_type.value} von {current_count} auf {count}")
        
        elif count < current_count:
            # Stoppe überzählige Agenten
            agents_to_stop = [
                agent_id for agent_id, agent in self.agents.items()
                if agent.type == agent_type and agent.status != "stopped"
            ][count:]
            
            for agent_id in agents_to_stop:
                self.stop_agent(agent_id)
            
            logger.info(f"📉 Skaliert: {agent_type.value} von {current_count} auf {count}")
    
    def _load_state(self):
        """Lade gespeicherten State"""
        state_file = self.data_dir / "orchestrator_state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.stats = state.get("stats", self.stats)
                logger.info("📂 State geladen")
            except Exception as e:
                logger.warning(f"Konnte State nicht laden: {e}")
    
    def save_state(self):
        """Speichere aktuellen State"""
        state_file = self.data_dir / "orchestrator_state.json"
        
        # Convert agents to JSON-serializable format
        agents_dict = {}
        for agent_id, agent in self.agents.items():
            agent_dict = asdict(agent)
            # Convert AgentType enum to string
            agent_dict['type'] = agent.type.value
            agents_dict[agent_id] = agent_dict
        
        state = {
            "stats": self.stats,
            "agents": agents_dict,
            "saved_at": datetime.utcnow().isoformat()
        }
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info("💾 State gespeichert")


# ============================================================================
# Beispiel Task Handlers
# ============================================================================

def generate_smile_handler(data: Dict) -> Dict:
    """Handler für Daily Smile Generierung"""
    from generate_daily_smile import generate_smile
    
    personality = data.get('personality', 'random')
    smile = generate_smile(personality=personality)
    
    return {
        "success": True,
        "smile": smile
    }


def worldtour_city_handler(data: Dict) -> Dict:
    """Handler für World Tour Stadt-Besuch"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    
    from worldtour_generator import WorldtourGenerator
    
    generator = WorldtourGenerator()
    city_id = data.get('city_id')
    
    if not city_id:
        # Nächste Stadt auswählen
        next_city = generator.get_next_city()
        if not next_city:
            return {"success": False, "error": "Keine Städte verfügbar"}
        city_id = next_city['id']
    
    # Generiere Content
    content = generator.generate_city_content(
        city_id=city_id,
        personality=data.get('personality', 'john_cleese'),
        content_type=data.get('content_type', 'city_review')
    )
    
    # Markiere als besucht
    generator.mark_city_visited(city_id)
    
    return {
        "success": True,
        "city_id": city_id,
        "content": content
    }


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🤖 UMAJA Autonomous Agent System"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Start Command
    start_parser = subparsers.add_parser('start', help='Start agent system')
    start_parser.add_argument(
        '--agents',
        type=int,
        default=3,
        help='Number of agents per type'
    )
    start_parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Run duration in seconds (0 = forever)'
    )
    
    # Status Command
    status_parser = subparsers.add_parser('status', help='Show status')
    
    # Scale Command
    scale_parser = subparsers.add_parser('scale', help='Scale agents')
    scale_parser.add_argument('agent_type', help='Agent type to scale')
    scale_parser.add_argument('count', type=int, help='Number of agents')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        print("=" * 70)
        print("🤖 UMAJA AUTONOMOUS AGENT SYSTEM")
        print("=" * 70)
        print()
        
        # Erstelle Orchestrator
        orchestrator = AgentOrchestrator()
        
        # Registriere Handler
        orchestrator.register_task_handler("generate_smile", generate_smile_handler)
        orchestrator.register_task_handler("worldtour_city", worldtour_city_handler)
        
        # Erstelle und starte Agenten
        print(f"📦 Erstelle {args.agents} Agenten pro Typ...")
        print()
        
        agent_types = [
            AgentType.CONTENT_GENERATOR,
            AgentType.WORLD_TOUR_GUIDE
        ]
        
        for agent_type in agent_types:
            for _ in range(args.agents):
                agent_id = orchestrator.create_agent(agent_type)
                orchestrator.start_agent(agent_id)
        
        # Füge Test-Tasks hinzu
        print()
        print("📝 Füge Test-Tasks hinzu...")
        print()
        
        # Daily Smile Tasks
        for i in range(5):
            orchestrator.add_task(
                task_type="generate_smile",
                agent_type=AgentType.CONTENT_GENERATOR,
                data={"personality": "random"},
                priority=7
            )
        
        # World Tour Tasks
        for i in range(3):
            orchestrator.add_task(
                task_type="worldtour_city",
                agent_type=AgentType.WORLD_TOUR_GUIDE,
                data={"personality": "john_cleese"},
                priority=8
            )
        
        print()
        print("✅ System gestartet!")
        print()
        print(f"Laufzeit: {args.duration}s" if args.duration > 0 else "Laufzeit: ∞")
        print()
        
        # Laufe für angegebene Dauer
        try:
            if args.duration > 0:
                time.sleep(args.duration)
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            print()
            print("🛑 Interrupt empfangen...")
        
        # Stoppe Agenten
        orchestrator.stop_all_agents()
        time.sleep(2)  # Warte auf sauberes Shutdown
        
        # Zeige finalen Status
        print()
        print("-" * 70)
        print("📊 Finaler Status:")
        print("-" * 70)
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))
        
        # Speichere State
        orchestrator.save_state()
        
        print()
        print("=" * 70)
        print("Happy Landing! 🚀")
        print("=" * 70)
    
    elif args.command == 'status':
        orchestrator = AgentOrchestrator()
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.command == 'scale':
        orchestrator = AgentOrchestrator()
        agent_type = AgentType(args.agent_type)
        orchestrator.scale_agents(agent_type, args.count)
        orchestrator.save_state()
        print(f"✅ Skaliert: {agent_type.value} auf {args.count} Agenten")
