# White Room Lab Architecture

## System Overview

The White Room Lab is a 3D web application built with Next.js 14, React Three Fiber, and Cannon.js. It provides an interactive environment for AI-human co-creation.

## Architecture Layers

### 1. Presentation Layer (UI)
- **React Components**: ChatInterface, PermissionManager, SystemStatus, VoiceInput
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React useState/useEffect hooks

### 2. 3D Rendering Layer
- **Three.js**: Low-level 3D graphics
- **React Three Fiber**: React renderer for Three.js
- **@react-three/drei**: Useful 3D helpers and abstractions
- **Environment**: Studio lighting preset for professional appearance

### 3. Physics Layer
- **Cannon.js**: Physics engine for realistic simulations
- **@react-three/cannon**: React bindings for Cannon.js
- **Physics Bodies**: Static (floor, walls) and Dynamic (Blue Bubble, objects)

### 4. Logic Layer
- **Command Parser**: Natural language processing (lib/commands.ts)
- **Transform System**: Morphing animations between forms (lib/transforms.ts)
- **Voice Recognition**: Web Speech API wrapper (lib/voice.ts)

### 5. Data Layer
- **TypeScript Types**: Strongly typed interfaces
- **State**: Component-level state management
- **Future**: Integration with UMAJA-Core backend API

## Component Architecture

```
WhiteRoomLab (Main Container)
│
├── Canvas (3D Scene)
│   ├── Lighting
│   │   ├── Ambient Light
│   │   ├── Spot Light (with shadows)
│   │   └── Point Light
│   │
│   ├── Physics World
│   │   ├── WhiteRoom (Environment)
│   │   │   ├── Floor (static body)
│   │   │   ├── Back Wall
│   │   │   ├── Left Wall
│   │   │   └── Right Wall
│   │   │
│   │   └── BlueBubble (AI Agent)
│   │       ├── Sphere Geometry
│   │       ├── Material (emissive, transparent)
│   │       ├── Point Light (glow)
│   │       └── Speech Bubble (HTML overlay)
│   │
│   ├── OrbitControls (Camera interaction)
│   └── Environment (Studio preset)
│
├── UI Overlay
│   ├── SystemStatus (top-right)
│   │   ├── FPS counter
│   │   ├── Object count
│   │   ├── Physics status
│   │   ├── Current form
│   │   └── Active simulations
│   │
│   └── Bottom Interface
│       ├── ChatInterface
│       │   ├── Message history
│       │   ├── Input field
│       │   └── Send button
│       │
│       └── VoiceInput
│           ├── Microphone button
│           └── Transcript display
│
└── PermissionManager (Modal)
    ├── Request details
    ├── Risk indicator
    ├── ACCEPT button
    ├── REJECT button
    └── MORE INFO button
```

## Data Flow

### Command Processing Flow

```
User Input (Text/Voice)
    ↓
parseCommand() → ParsedCommand
    ↓
Command Router
    ├─→ Transform Intent → morphToForm()
    ├─→ Build Intent → PermissionRequest
    ├─→ Simulate Intent → Simulation Engine
    ├─→ Analyze Intent → Analysis System
    └─→ Query Intent → Information Retrieval
```

### Permission Request Flow

```
AI needs resource
    ↓
Create PermissionRequest
    ↓
Add to request queue
    ↓
Show PermissionManager modal
    ↓
User Decision
    ├─→ ACCEPT → Grant access → Execute action
    ├─→ REJECT → Deny access → Inform AI
    └─→ MORE INFO → Show detailed explanation
```

### Transform Flow

```
User: "Verwandle dich in DNA"
    ↓
parseCommand() → { intent: 'transform', target: 'dna' }
    ↓
mapTargetToForm('dna') → 'dna'
    ↓
morphToForm('bubble', 'dna', config)
    ├─→ Calculate morph path
    ├─→ Generate intermediate geometries
    ├─→ Animate vertex positions
    ├─→ Update material properties
    └─→ Emit completion event
    ↓
Update UI → Speech bubble: "Ich bin jetzt DNA!"
```

## Performance Considerations

### Optimization Strategies

1. **React.memo**: Memoize expensive components
2. **useMemo/useCallback**: Prevent unnecessary recalculations
3. **Three.js LOD**: Level of Detail for distant objects
4. **Frustum Culling**: Don't render off-screen objects
5. **Instanced Meshes**: For repeated geometry
6. **Texture Compression**: Optimize model textures

### Target Metrics

- FPS: ≥60 on modern hardware (2020+)
- Load Time: <3 seconds
- Memory: <500 MB
- Bundle Size: <2 MB (gzipped)

## Security Considerations

### Permission System

- **Risk Levels**: Low (verified), Medium (third-party), High (unverified)
- **User Consent**: Required for all resource access
- **Audit Trail**: Log all permission requests and responses
- **Sandboxing**: Isolate executed code when possible

### Input Validation

- Sanitize user commands before parsing
- Prevent XSS in speech bubbles
- Validate all API responses
- Rate limiting on command processing

## Extensibility

### Adding New Forms

1. Create geometry/model in `/public/models/`
2. Add form type to `FormType` enum in `types/index.ts`
3. Add configuration in `getFormConfig()` in `lib/transforms.ts`
4. Add mapping in `mapTargetToForm()` in `lib/commands.ts`
5. Implement transform animation

### Adding New Commands

1. Add intent type to `ParsedCommand` interface
2. Add pattern matching in `parseCommand()`
3. Implement handler in main page component
4. Update UI to display results

### Integration Points

- **UMAJA-Core API**: Backend integration for data
- **GitHub API**: Fetch PRs and issues
- **External Simulations**: Connect to external engines
- **Database**: Store user preferences and history

## Technology Choices

### Why Next.js?

- Server-side rendering for fast initial load
- API routes for backend integration
- Automatic code splitting
- Excellent developer experience
- Vercel deployment optimized

### Why Three.js?

- Industry standard for web 3D
- Mature ecosystem
- Excellent performance
- Wide browser support
- Active community

### Why Cannon.js?

- Lightweight physics engine
- Good performance for simple simulations
- Easy integration with Three.js
- React bindings available

### Why Tailwind CSS?

- Utility-first approach
- Excellent for responsive design
- Small bundle size
- Fast development
- Good documentation

## Future Architecture

### Phase 2: Advanced Simulations

- WebAssembly for compute-heavy simulations
- Web Workers for parallel processing
- SharedArrayBuffer for physics calculations
- GPU compute shaders for particles

### Phase 3: Multiplayer

- WebRTC for peer-to-peer communication
- WebSockets for server synchronization
- Conflict resolution for simultaneous edits
- State synchronization

### Phase 4: VR/AR

- WebXR API integration
- Hand tracking
- Spatial audio
- Room-scale interactions

## Deployment Architecture

```
Developer → Git Push
    ↓
GitHub Actions (CI/CD)
    ├─→ Run tests
    ├─→ Build Next.js app
    ├─→ Optimize assets
    └─→ Deploy to Vercel
    ↓
Vercel Edge Network
    ├─→ Static assets (CDN)
    ├─→ API routes (serverless)
    └─→ Server-side rendering
    ↓
User Browser
```

## Monitoring & Analytics

### Metrics to Track

- FPS performance
- Load times
- Error rates
- User engagement
- Command success rate
- Transform completion time
- Permission accept/reject rate

### Tools

- Vercel Analytics
- Sentry (error tracking)
- Custom telemetry
- Performance API

---

*This architecture is designed to scale from MVP to production while maintaining code quality and user experience.*
