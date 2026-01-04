# 🔵 White Room Lab - Interactive 3D AI-Human Co-Creation Laboratory

Welcome to the White Room Lab! This is a revolutionary 3D web-based laboratory where users can interact with an AI agent (Blue Bubble) to co-create, simulate, and explore complex systems in real-time.

## 🌟 Features

- **3D Interactive Environment**: Fully immersive white room with realistic lighting and physics
- **AI Formwandler Agent**: Blue Bubble can transform into ANY form (human, DNA, turbine, galaxy, etc.)
- **Natural Language Interface**: Chat with the AI using German or English commands
- **Permission System**: AI asks permission before installing tools or accessing resources
- **Voice Input**: Optional voice commands using Web Speech API
- **Real-time Physics**: Powered by Cannon.js for realistic simulations
- **System Monitoring**: Live FPS, object count, and simulation status

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

#### Transform Commands
- `"Verwandle dich in DNA"` - Transform to DNA helix
- `"Transform into human"` - Transform to human form
- `"Sei eine Turbine"` - Become a turbine

#### Build Commands
- `"Baue eine Gasturbine"` - Build a gas turbine
- `"Erstelle ein Molekül"` - Create a molecule
- `"Build a neural network"` - Build a neural network

#### Simulate Commands
- `"Simuliere Luftstrom"` - Simulate air flow
- `"Test the turbine"` - Test turbine simulation

#### Query Commands
- `"Zeig mir PRs"` - Show GitHub pull requests
- `"Was ist deine aktuelle Form?"` - What is your current form?

## 🏗️ Architecture

### Technology Stack

- **Framework**: Next.js 14 with TypeScript
- **3D Graphics**: Three.js + React Three Fiber + Drei
- **Physics**: Cannon-es + @react-three/cannon
- **Animation**: Framer Motion (planned)
- **Styling**: Tailwind CSS
- **Deployment**: Vercel-ready

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
│   │   └── SystemStatus.tsx         # Real-time metrics
│   ├── lib/
│   │   ├── transforms.ts            # Morphing animations
│   │   ├── voice.ts                 # Web Speech API wrapper
│   │   ├── physics.ts               # Physics utilities
│   │   └── commands.ts              # NLP command parser
│   └── types/
│       └── index.ts                 # TypeScript definitions
├── public/
│   └── models/                      # 3D models (GLTF)
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

## 🐛 Known Issues

- Voice input not supported in all browsers (Safari limited support)
- Some 3D models need to be added to `/public/models/`
- Transform animations are placeholder (smooth morphing in progress)

## 🚧 Roadmap

### Week 1 (Current) ✅
- [x] Core 3D environment
- [x] Blue Bubble agent
- [x] Chat interface
- [x] Permission system
- [x] System status display
- [x] Basic command parsing

### Week 2 (Planned)
- [ ] Object creation & CAD integration
- [ ] Fluid dynamics simulation
- [ ] Advanced transform animations
- [ ] More form types (DNA, turbine, etc.)

### Week 3 (Planned)
- [ ] Molecular visualization
- [ ] Neural network visualization
- [ ] City builder
- [ ] Cosmic structures

### Week 4 (Planned)
- [ ] Performance optimization
- [ ] Advanced materials (PBR)
- [ ] Multiplayer support (optional)
- [ ] VR/AR ready

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
