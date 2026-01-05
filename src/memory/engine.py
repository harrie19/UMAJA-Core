"""
Memory Persistence Engine for UMAJA
Provides semantic memory storage and retrieval using ChromaDB
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
import re
from dataclasses import dataclass, asdict

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False


@dataclass
class Memory:
    """Represents a single memory with metadata"""
    id: str
    content: str
    timestamp: str
    importance: float  # 0-1 scale
    entities: List[str]  # Extracted entities (people, tech, concepts)
    topics: List[str]  # Classified topics
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Context:
    """Represents restored context from memories"""
    memories: List[Memory]
    summary: str
    entities: List[str]
    topics: List[str]
    confidence: float


class MemoryEngine:
    """
    Complete memory persistence engine
    - ChromaDB for semantic search
    - GitHub for human-readable audit trail
    - Entity extraction and topic classification
    """
    
    def __init__(self, db_path: str = ".umaja-memory", repo_path: Optional[Path] = None):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        self.repo_path = repo_path or Path.cwd()
        
        # Initialize ChromaDB if available
        if CHROMADB_AVAILABLE:
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name="umaja_memories",
                metadata={"description": "UMAJA AI memory store"}
            )
        else:
            self.client = None
            self.collection = None
            
        # Initialize embeddings model if available
        if EMBEDDINGS_AVAILABLE:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedder = None
    
    def remember(self, content: str, metadata: Optional[Dict] = None) -> Memory:
        """
        Store a new memory with automatic enrichment
        """
        if metadata is None:
            metadata = {}
            
        # Generate memory ID
        memory_id = f"mem_{datetime.now(timezone.utc).timestamp()}"
        
        # Extract entities (simple pattern matching)
        entities = self._extract_entities(content)
        
        # Classify topics
        topics = self._classify_topics(content)
        
        # Calculate importance
        importance = self._calculate_importance(content, entities, topics)
        
        # Create memory object
        memory = Memory(
            id=memory_id,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            importance=importance,
            entities=entities,
            topics=topics,
            metadata=metadata
        )
        
        # Store in ChromaDB if available
        if self.collection is not None:
            embedding = self._generate_embedding(content)
            self.collection.add(
                ids=[memory_id],
                embeddings=[embedding] if embedding else None,
                documents=[content],
                metadatas=[{
                    "importance": importance,
                    "entities": json.dumps(entities),
                    "topics": json.dumps(topics),
                    "timestamp": memory.timestamp,
                    **metadata
                }]
            )
        
        # Persist to GitHub-friendly JSON
        self._persist_to_github(memory)
        
        return memory
    
    def recall(self, query: str, limit: int = 5, min_importance: float = 0.0) -> List[Memory]:
        """
        Retrieve relevant memories using semantic search
        """
        if self.collection is None:
            # Fallback to file-based search
            return self._recall_from_files(query, limit)
        
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding] if query_embedding else None,
            query_texts=[query] if not query_embedding else None,
            n_results=limit * 2  # Get more and filter
        )
        
        memories = []
        for i, doc_id in enumerate(results['ids'][0]):
            meta = results['metadatas'][0][i]
            
            # Filter by importance
            if meta.get('importance', 0) < min_importance:
                continue
                
            memory = Memory(
                id=doc_id,
                content=results['documents'][0][i],
                timestamp=meta.get('timestamp', ''),
                importance=meta.get('importance', 0.5),
                entities=json.loads(meta.get('entities', '[]')),
                topics=json.loads(meta.get('topics', '[]')),
                metadata={k: v for k, v in meta.items() 
                         if k not in ['importance', 'entities', 'topics', 'timestamp']}
            )
            memories.append(memory)
            
            if len(memories) >= limit:
                break
        
        return memories
    
    def build_context(self, query: str, max_memories: int = 10) -> Context:
        """
        Build a comprehensive context for AI restoration
        """
        memories = self.recall(query, limit=max_memories)
        
        # Extract unique entities and topics
        all_entities = set()
        all_topics = set()
        for mem in memories:
            all_entities.update(mem.entities)
            all_topics.update(mem.topics)
        
        # Build summary
        summary = self._build_summary(memories)
        
        # Calculate confidence based on memory count and relevance
        confidence = min(1.0, len(memories) / max_memories) if memories else 0.0
        
        return Context(
            memories=memories,
            summary=summary,
            entities=list(all_entities),
            topics=list(all_topics),
            confidence=confidence
        )
    
    def forget(self, memory_id: str, reason: str) -> None:
        """
        Remove a memory (with audit trail)
        """
        if self.collection is not None:
            self.collection.delete(ids=[memory_id])
        
        # Log deletion
        audit_log = self.db_path / "deletions.jsonl"
        with open(audit_log, 'a') as f:
            f.write(json.dumps({
                "memory_id": memory_id,
                "reason": reason,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }) + '\n')
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract entities using pattern matching"""
        entities = []
        
        # Extract capitalized words (potential names)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        entities.extend(capitalized[:5])  # Limit to 5
        
        # Extract technical terms
        tech_patterns = [
            r'\b(?:Python|JavaScript|React|Django|FastAPI|ChromaDB|Railway)\b',
            r'\b(?:API|CLI|UI|UX|DB|SQL)\b',
            r'\b(?:GitHub|Docker|Kubernetes)\b'
        ]
        for pattern in tech_patterns:
            entities.extend(re.findall(pattern, content, re.IGNORECASE))
        
        return list(set(entities))[:10]  # Unique, max 10
    
    def _classify_topics(self, content: str) -> List[str]:
        """Classify content into topics"""
        topics = []
        
        topic_keywords = {
            "development": ["code", "develop", "implement", "bug", "fix", "test"],
            "infrastructure": ["deploy", "server", "database", "api", "backend"],
            "documentation": ["docs", "readme", "guide", "documentation"],
            "planning": ["plan", "strategy", "roadmap", "todo", "task"],
            "security": ["security", "auth", "credential", "token", "vulnerability"]
        }
        
        content_lower = content.lower()
        for topic, keywords in topic_keywords.items():
            if any(kw in content_lower for kw in keywords):
                topics.append(topic)
        
        return topics
    
    def _calculate_importance(self, content: str, entities: List[str], topics: List[str]) -> float:
        """Calculate memory importance (0-1)"""
        score = 0.5  # Base score
        
        # Boost for entities
        score += min(0.2, len(entities) * 0.02)
        
        # Boost for critical keywords
        critical_keywords = ["critical", "important", "urgent", "security", "bug"]
        if any(kw in content.lower() for kw in critical_keywords):
            score += 0.2
        
        # Boost for multiple topics
        score += min(0.1, len(topics) * 0.05)
        
        return min(1.0, score)
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding vector for text"""
        if self.embedder is None:
            return None
        
        try:
            embedding = self.embedder.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception:
            return None
    
    def _persist_to_github(self, memory: Memory) -> None:
        """Persist memory to GitHub-friendly JSON file"""
        memories_dir = self.db_path / "memories"
        memories_dir.mkdir(exist_ok=True)
        
        # Save as individual file for easy git tracking
        memory_file = memories_dir / f"{memory.id}.json"
        with open(memory_file, 'w') as f:
            json.dump(memory.to_dict(), f, indent=2)
    
    def _recall_from_files(self, query: str, limit: int) -> List[Memory]:
        """Fallback: recall from JSON files"""
        memories_dir = self.db_path / "memories"
        if not memories_dir.exists():
            return []
        
        memories = []
        query_lower = query.lower()
        
        for memory_file in sorted(memories_dir.glob("*.json"), reverse=True):
            try:
                with open(memory_file) as f:
                    data = json.load(f)
                    
                # Simple text matching
                if query_lower in data['content'].lower():
                    memories.append(Memory(**data))
                    
                if len(memories) >= limit:
                    break
            except Exception:
                continue
        
        return memories
    
    def _build_summary(self, memories: List[Memory]) -> str:
        """Build a summary from memories"""
        if not memories:
            return "No relevant memories found."
        
        summary_parts = []
        for mem in memories[:5]:  # Top 5
            summary_parts.append(f"- {mem.content[:100]}...")
        
        return "\n".join(summary_parts)
