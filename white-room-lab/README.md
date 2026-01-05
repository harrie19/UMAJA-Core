# 🔵 White Room Lab - Interactive 3D AI-Human Co-Creation Laboratory

Welcome to the White Room Lab! This is a revolutionary 3D web-based laboratory where users can interact with an AI agent (Blue Bubble) to co-create, simulate, and explore complex systems in real-time.

## 🌟 Features

### ✅ Implemented and Working

- **3D Interactive Environment**: Fully immersive white room with realistic lighting
- **AI Formwandler Agent (Blue Bubble)**: Can transform into 6+ forms (DNA, Neural Network, Molecule, City, Galaxy, and more)
- **Natural Language Interface**: Chat with the AI using German or English commands
- **Voice Input**: Voice commands using Web Speech API (browser-dependent)
- **GitHub PR Visualization**: Real-time 3D network of pull requests from this repository
- **Energy Monitor**: Live energy flow visualization with particle system
- **Vector Agent Swarm**: 15 autonomous agents that move and communicate
- **World Tour Globe**: Interactive 3D Earth with visited cities
- **System Monitoring**: Live FPS, object count, and system status
- **Permission System**: AI asks permission before installing tools or accessing resources

### 📊 Transformations Available

1. **DNA Helix** - Double helix with 20 base pairs, rotating animation
2. **Neural Network** - 3-layer network (4-6-2) with animated signal flow
3. **Water Molecule (H2O)** - Chemically accurate with 104.5° bond angle
4. **Procedural City** - 10x10 grid with 100 random-height buildings
5. **Spiral Galaxy** - 10,000 particles in logarithmic spiral arms
6. **Blue Bubble** - Default pulsating sphere form

### 🎨 Visualizations

- **GitHub PRs** - Live data from harrie19/UMAJA-Core displayed as 3D network
- **Energy Monitor** - Real-time power metrics with particle effects
- **Agent Swarm** - 15 mini-agents with dynamic connections
- **World Tour** - 3D rotating Earth with 8 city pins and visit tracking

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

```bash
# Navigate to the white-room-lab directory
cd white-room-lab

# Install dependencies
npm install

# Run development server
npm run dev

# Open browser to http://localhost:3000
```

### Building for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

## 📖 Usage

### Basic Interactions

1. **Click the Blue Bubble**: Opens speech bubble with greeting
2. **Type Commands**: Use natural language in the chat interface
3. **Voice Commands**: Click microphone button for voice input (optional)
4. **Camera Controls**: 
   - Left mouse: Rotate
   - Right mouse: Pan
   - Scroll: Zoom

### Example Commands

#### Transform Commands (Working ✅)
- `"Verwandle dich in DNA"` - Transform to DNA helix
- `"Zeig mir ein neuronales Netzwerk"` - Show neural network
- `"Werde zu einem Molekül"` / `"Show me H2O"` - Water molecule
- `"Bau eine Stadt"` / `"Build a city"` - Procedural city
- `"Zeig mir eine Galaxie"` / `"Show me a galaxy"` - Spiral galaxy
- `"Transform into bubble"` - Return to default form

#### Query Commands (Working ✅)
- `"Hilfe"` / `"Help"` - Show available commands
- `"Was kannst du?"` / `"What can you do?"` - Show capabilities

#### Visualization Viewing (Always Visible)
- GitHub PRs are visible at position (0, 3, -5)
- Energy Monitor at position (5, 2, -5)
- Vector Swarm at position (0, 0, 0)
- World Tour Globe at position (-5, 0, -5)

## 🏗️ Architecture

### Technology Stack

- **Framework**: Next.js 14 with TypeScript (strict mode)
- **3D Graphics**: Three.js + React Three Fiber + Drei
- **Physics**: @react-three/cannon + Cannon-es (basic integration)
- **Animation**: React Three Fiber useFrame
- **Styling**: Tailwind CSS
- **Deployment**: Vercel-ready (zero-config)
- **APIs**: GitHub API, Mock WebSocket for energy data

### Project Structure

```
white-room-lab/
├── src/
│   ├── app/
│   │   ├── page.tsx                 # Main lab interface
│   │   ├── layout.tsx               # App layout
│   │   └── globals.css              # Global styles
│   ├── components/
│   │   ├── BlueBubble.tsx           # Formwandler AI agent
│   │   ├── WhiteRoom.tsx            # 3D environment
│   │   ├── ChatInterface.tsx        # Natural language interaction
│   │   ├── PermissionManager.tsx    # ACCEPT/REJECT system
│   │   ├── VoiceInput.tsx           # Voice recognition
│   │   ├── SystemStatus.tsx         # Real-time metrics
│   │   ├── PRVisualization.tsx      # ✨ GitHub PR 3D network
│   │   ├── EnergyVisualization.tsx  # ✨ Energy monitor with particles
│   │   ├── VectorSwarm.tsx          # ✨ Agent swarm visualization
│   │   └── WorldTourGlobe.tsx       # ✨ 3D Earth with cities
│   ├── lib/
│   │   ├── transforms.tsx           # ✨ 6 working 3D transformations
│   │   ├── voice.ts                 # Web Speech API wrapper
│   │   ├── commands.ts              # ✨ NLP command parser
│   │   └── umaja-api.ts             # ✨ API integration layer
│   └── types/
│       └── index.ts                 # TypeScript definitions
├── docs/                            # Documentation
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

## 🎨 Components

### BlueBubble
The main AI agent with pulsating animation, speech bubbles, and transformation capabilities.

### WhiteRoom
3D environment with reflective floor, walls, and grid for depth perception.

### ChatInterface
Natural language chat UI with message history and command parsing.

### PermissionManager
Modal popup system for AI permission requests with risk levels.

### SystemStatus
Real-time metrics display showing FPS, object count, and system status.

### VoiceInput
Voice recognition interface using Web Speech API (gracefully degrades if not supported).

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file for local development:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_GITHUB_TOKEN=your_github_token
```

### Tailwind Configuration

Customize colors in `tailwind.config.ts`:

```typescript
colors: {
  'blue-bubble': '#4FC3F7',
  'blue-emissive': '#2196F3',
}
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Open lab → See Blue Bubble in White Room
- [ ] Click bubble → See speech bubble
- [ ] Type "baue turbine" → See permission request
- [ ] Click ACCEPT → Tool "installs"
- [ ] Type "verwandle dich in DNA" → Bubble morphs
- [ ] Test camera controls (orbit, zoom, pan)
- [ ] Check FPS ≥ 60 on modern hardware
- [ ] Test on Chrome, Firefox, Safari

## 🔗 Integration with UMAJA-Core

The White Room Lab integrates with the main UMAJA-Core system:

- **GitHub API**: Fetch and visualize PRs
- **Energy Monitor**: Live data visualization
- **Vector Agents**: Swarm visualization (planned)

## 📚 Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - System design details
- [Usage Guide](docs/USAGE.md) - User manual
- [Transform Guide](docs/TRANSFORMS.md) - Available forms
- [Integration Guide](docs/INTEGRATION.md) - UMAJA-Core integration

## 🐛 Known Status & Limitations

### ✅ Working Features
- All 6 transformations render correctly
- GitHub PR API integration (real data)
- Energy monitor with live updates
- Vector swarm with movement
- World tour globe with rotation
- Command parsing (German + English)
- Voice input (browser-dependent)
- Build system (0 errors)

### ⚠️ Known Limitations
- Voice input not supported in all browsers (Safari has limited support)
- Transformations are displayed but not yet integrated with Blue Bubble morphing
- Some placeholder transformations (Turbine, Tool, Vehicle, Human, Bugs Bunny) not implemented
- Real physics simulations not yet implemented (basic collision only)

### 🚧 Planned Enhancements
- Smooth morphing animations between forms
- Integration of transformations with Blue Bubble
- Form Library UI browser
- Scene Controls component
- Additional transformations
- Advanced physics simulations

## 🚧 Status & Roadmap

### ✅ Phase 1: Foundation (Complete)
- [x] Core 3D environment
- [x] Blue Bubble agent
- [x] Chat interface with command parsing
- [x] Permission system
- [x] System status display
- [x] Voice input integration

### ✅ Phase 2: Visualizations (Complete)
- [x] GitHub PR visualization (3D network)
- [x] Energy monitor with particles
- [x] Vector agent swarm
- [x] World tour 3D globe

### ✅ Phase 3: Transformations (Partial - 6 of 11)
- [x] DNA Helix
- [x] Neural Network
- [x] Water Molecule (H2O)
- [x] Procedural City
- [x] Spiral Galaxy
- [x] Blue Bubble (default)
- [ ] Turbine (placeholder)
- [ ] Tool/Hammer (placeholder)
- [ ] Vehicle/Car (placeholder)
- [ ] Human (placeholder)
- [ ] Bugs Bunny (placeholder)

### 🚧 Phase 4: Integration & Polish (In Progress)
- [ ] Morphing animations between forms
- [ ] Form Library UI
- [ ] Scene Controls
- [ ] Complete remaining transformations

### 🔮 Phase 5: Advanced Features (Planned)
- [ ] WebRTC collaboration
- [ ] VR/AR support
- [ ] Advanced physics simulations
- [ ] AI co-creation agent

## 🤝 Contributing

Contributions are welcome! This is part of the UMAJA-Core mission to bring AI-powered tools to everyone.

### Areas for Contribution

- 🎨 3D models for transformations
- 🧠 Advanced NLP command parsing
- 🔬 Simulation engines (fluid, thermal, etc.)
- 🌐 Translations
- 📚 Documentation

## 📄 License

Part of UMAJA-Core - Universal Motivation & Joy for All  
Licensed under CC-BY 4.0

## 💡 Philosophy

This is not just a 3D viewer - it's a **co-creation laboratory** where human and AI work together to understand and build complex systems. Every interaction should feel magical yet purposeful.

## 📞 Support

- **Email**: Umaja1919@googlemail.com
- **GitHub Issues**: [Report a bug](https://github.com/harrie19/UMAJA-Core/issues)
- **Documentation**: [Full docs](docs/)

---

<div align="center">

**🔵 Built with ❤️ for 8 billion humans 🔵**

[⭐ Star](https://github.com/harrie19/UMAJA-Core) • [🐛 Report Bug](https://github.com/harrie19/UMAJA-Core/issues) • [✨ Request Feature](https://github.com/harrie19/UMAJA-Core/issues)

</div>
