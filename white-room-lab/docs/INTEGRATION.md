# UMAJA-Core Integration Guide

## Overview

The White Room Lab integrates with the broader UMAJA-Core ecosystem to provide AI-powered features, data visualization, and collaborative tools.

## Integration Points

### 1. Backend API Integration

#### Connection Setup

```typescript
// src/lib/umaja-api.ts
const UMAJA_API_URL = process.env.NEXT_PUBLIC_API_URL || 
  'https://umaja-core-production.up.railway.app';

export async function fetchFromUMAJA(endpoint: string) {
  const response = await fetch(`${UMAJA_API_URL}${endpoint}`);
  return response.json();
}
```

#### Available Endpoints

##### Health Check
```typescript
GET /health
Response: { status: 'healthy', mission: '8 billion smiles' }
```

##### Daily Smile
```typescript
GET /api/daily-smile
Response: { content: string, archetype: string }
```

Use case: Display inspirational messages in the lab

##### World Tour Status
```typescript
GET /worldtour/status
Response: { 
  status: string,
  stats: {...},
  next_city: {...}
}
```

Use case: Visualize world tour data as 3D globe

---

### 2. GitHub API Integration

#### Visualizing Pull Requests

```typescript
// Fetch PRs from UMAJA-Core repository
async function fetchUMAJAPRs() {
  const response = await fetch(
    'https://api.github.com/repos/harrie19/UMAJA-Core/pulls'
  );
  const prs = await response.json();
  
  return prs.map(pr => ({
    id: pr.number,
    title: pr.title,
    status: pr.state,
    author: pr.user.login,
    created: pr.created_at,
    // Transform to 3D visualization
    position: calculateSpatialPosition(pr),
    connections: extractDependencies(pr),
    color: getStatusColor(pr.state),
  }));
}

// Spatial positioning algorithm
function calculateSpatialPosition(pr: any) {
  const age = Date.now() - new Date(pr.created_at).getTime();
  const x = (pr.number % 10) - 5; // Spread horizontally
  const y = Math.log(age / 1000 / 60 / 60); // Height by age
  const z = pr.comments * 0.1; // Depth by activity
  return [x, y, z];
}
```

#### 3D PR Visualization Component

```typescript
// src/components/PRVisualization.tsx
export function PRVisualization({ prs }: { prs: PR[] }) {
  return (
    <group>
      {prs.map(pr => (
        <PRNode
          key={pr.id}
          position={pr.position}
          color={pr.color}
          label={pr.title}
          onClick={() => window.open(pr.url)}
        />
      ))}
    </group>
  );
}
```

---

### 3. Energy Monitor Integration

#### WebSocket Connection

```typescript
// src/lib/energy-monitor.ts
export class EnergyMonitor {
  private ws: WebSocket | null = null;
  private onDataCallback?: (data: EnergyData) => void;

  connect() {
    this.ws = new WebSocket(
      'wss://umaja-core-production.up.railway.app/ws/energy'
    );

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (this.onDataCallback) {
        this.onDataCallback(data);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  onData(callback: (data: EnergyData) => void) {
    this.onDataCallback = callback;
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

#### 3D Energy Visualization

```typescript
// Visualize energy data as flowing particles
export function EnergyVisualization({ data }: { data: EnergyData }) {
  return (
    <group>
      <EnergyFlowParticles
        source={[0, 0, 0]}
        target={[10, 0, 0]}
        rate={data.consumption}
        color={getEnergyColor(data.type)}
      />
      <EnergyMeter
        position={[10, 2, 0]}
        value={data.currentPower}
        max={data.maxPower}
      />
    </group>
  );
}
```

---

### 4. Vector Agent Swarm Visualization

#### Agent Data Structure

```typescript
interface VectorAgent {
  id: string;
  position: [number, number, number];
  velocity: [number, number, number];
  state: 'idle' | 'working' | 'communicating';
  neighbors: string[]; // IDs of connected agents
  task?: string;
}
```

#### Swarm Visualization

```typescript
// src/components/VectorSwarm.tsx
export function VectorSwarm({ agents }: { agents: VectorAgent[] }) {
  return (
    <group>
      {agents.map((agent) => (
        <MiniAgent
          key={agent.id}
          position={agent.position}
          velocity={agent.velocity}
          color={getAgentColor(agent.state)}
          connections={agent.neighbors}
        />
      ))}
    </group>
  );
}

// Individual agent component
function MiniAgent({ position, color, connections }: AgentProps) {
  return (
    <>
      <mesh position={position}>
        <sphereGeometry args={[0.1, 8, 8]} />
        <meshStandardMaterial color={color} emissive={color} />
      </mesh>
      {connections.map(neighborId => (
        <ConnectionLine
          key={neighborId}
          start={position}
          end={getAgentPosition(neighborId)}
        />
      ))}
    </>
  );
}
```

---

### 5. CDN Content Integration

#### Loading Smiles Data

```typescript
// Load daily smiles from CDN
async function loadDailySmile(
  archetype: 'Dreamer' | 'Warrior' | 'Healer',
  language: string,
  day: number
) {
  const url = `https://harrie19.github.io/UMAJA-Core/cdn/smiles/${archetype}/${language}/${day}.json`;
  const response = await fetch(url);
  return response.json();
}

// Display in 3D as floating text
export function SmileDisplay({ smile }: { smile: SmileData }) {
  return (
    <Html position={[0, 3, 0]}>
      <div className="bg-white/90 p-4 rounded-lg max-w-md">
        <p className="text-gray-800 italic">"{smile.content}"</p>
        <p className="text-sm text-gray-600 mt-2">
          — {smile.archetype}
        </p>
      </div>
    </Html>
  );
}
```

---

## Data Flow Architecture

```
White Room Lab ←→ UMAJA Backend ←→ External APIs
     ↓                  ↓                ↓
  3D Viz          Processing        GitHub
  Physics         Storage           Social
  User Input      Analytics         Weather
```

---

## Authentication & Security

### API Keys

Store sensitive keys in environment variables:

```bash
# .env.local
NEXT_PUBLIC_API_URL=https://umaja-core-production.up.railway.app
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

### CORS Configuration

Backend must allow requests from lab domain:

```python
# In UMAJA backend
CORS(app, origins=[
    'http://localhost:3000',  # Development
    'https://your-lab-domain.vercel.app',  # Production
])
```

---

## Real-time Collaboration (Planned)

### WebRTC Integration

```typescript
// Peer-to-peer collaboration
export class CollaborationManager {
  private peer: RTCPeerConnection;
  private dataChannel: RTCDataChannel;

  async connect(roomId: string) {
    // Establish WebRTC connection
    // Share cursor position, selections, changes
  }

  syncTransform(form: FormType) {
    // Broadcast transformation to peers
    this.dataChannel.send(JSON.stringify({
      type: 'transform',
      form,
      timestamp: Date.now(),
    }));
  }
}
```

---

## Performance Optimization

### Caching Strategy

```typescript
// Cache API responses
const cache = new Map<string, { data: any, timestamp: number }>();

async function cachedFetch(url: string, ttl = 60000) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.data;
  }

  const data = await fetch(url).then(r => r.json());
  cache.set(url, { data, timestamp: Date.now() });
  return data;
}
```

### Lazy Loading

```typescript
// Load integrations on demand
const EnergyMonitor = lazy(() => import('@/components/EnergyMonitor'));
const PRVisualization = lazy(() => import('@/components/PRVisualization'));

// In main component
{showEnergy && (
  <Suspense fallback={<LoadingSpinner />}>
    <EnergyMonitor />
  </Suspense>
)}
```

---

## Testing Integration

### Mock Data

```typescript
// src/lib/mock-data.ts
export const mockPRs = [
  {
    id: 1,
    title: 'Add White Room Lab',
    status: 'open',
    position: [2, 1, 0],
    color: '#4FC3F7',
  },
  // ... more mock data
];

export const mockEnergyData = {
  consumption: 150,
  currentPower: 75,
  maxPower: 200,
  type: 'renewable',
};
```

### Integration Tests

```typescript
// __tests__/integration.test.ts
describe('UMAJA Integration', () => {
  it('fetches health status', async () => {
    const health = await fetchFromUMAJA('/health');
    expect(health.status).toBe('healthy');
  });

  it('loads PR visualization', async () => {
    const prs = await fetchUMAJAPRs();
    expect(prs.length).toBeGreaterThan(0);
    expect(prs[0]).toHaveProperty('position');
  });
});
```

---

## Deployment Configuration

### Environment Variables

```bash
# Vercel deployment
vercel env add NEXT_PUBLIC_API_URL production
vercel env add GITHUB_TOKEN production
```

### Build Command

```json
{
  "scripts": {
    "build": "next build",
    "build:integration": "npm run build && npm run test:integration"
  }
}
```

---

## Future Integrations

### Phase 2
- [ ] World Tour visualization (3D globe)
- [ ] Email campaign metrics
- [ ] Social media feed integration
- [ ] Analytics dashboard

### Phase 3
- [ ] AI model training visualization
- [ ] Distributed computing stats
- [ ] Community contributions map
- [ ] Real-time collaboration

### Phase 4
- [ ] Blockchain integration (planned)
- [ ] IoT device control
- [ ] AR/VR synchronization
- [ ] Multi-universe visualization

---

## Support

For integration questions:
- **Email**: Umaja1919@googlemail.com
- **GitHub Issues**: [Report integration issues](https://github.com/harrie19/UMAJA-Core/issues)
- **Documentation**: [UMAJA-Core docs](https://github.com/harrie19/UMAJA-Core/blob/main/README.md)

---

*Integration enables the White Room Lab to be a powerful visualization and control center for the entire UMAJA ecosystem!* 🔵
