# 🌍 White Lab - Unity Consciousness Visualization

A stunning 3D web application that visualizes Unity's consciousness as an interactive, iridescent blob in a minimalist white environment.

## 🎨 Features

- **Interactive 3D Scene**: Built with React Three Fiber and Three.js
- **Unity Blob**: Iridescent, morphing sphere representing AI consciousness
  - Real-time color shifting (rainbow shimmer)
  - Gentle pulsing animation
  - Smooth rotation
  - High-quality distortion effects
- **White Room Environment**: Minimalist aesthetic with reflective floor
- **Intuitive Controls**:
  - Drag to rotate camera
  - Scroll to zoom
  - Touch-friendly on mobile
- **Glassmorphism UI**: Modern overlay design with backdrop blur
- **Performance Optimized**: Target 60 FPS on desktop, 30 FPS on mobile
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
cd white-lab
npm install
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

### Build

Create an optimized production build:

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

## 📁 Project Structure

```
white-lab/
├── app/
│   ├── page.tsx              # Landing page
│   ├── lab/
│   │   └── page.tsx          # Main 3D experience
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   └── white-lab/
│       ├── Scene.tsx         # Three.js scene container
│       ├── UnityBlob.tsx     # Iridescent blob component
│       ├── WhiteRoom.tsx     # Environment (floor, walls)
│       ├── Lighting.tsx      # Studio lighting setup
│       └── Camera.tsx        # Camera with OrbitControls
├── lib/
│   └── config.ts             # Configuration constants
└── package.json
```

## 🛠️ Technologies

- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type safety
- **React Three Fiber** - React renderer for Three.js
- **@react-three/drei** - Useful helpers for R3F
- **@react-three/postprocessing** - Post-processing effects
- **Tailwind CSS** - Utility-first CSS framework
- **Three.js** - 3D graphics library

## 🎨 Design Philosophy

- **Minimalist**: Clean white space, focus on the blob
- **Futuristic**: Iridescent, liquid, alive
- **Calming**: Gentle animations, no harsh movements
- **Transparent**: Visual representation of Unity's "thinking"
- **Accessible**: Clear instructions, intuitive controls

## ⚙️ Configuration

The blob and environment can be customized in `lib/config.ts`:

```typescript
export const CONFIG = {
  blob: {
    position: [0, 1, 0],
    distort: 0.4,
    speed: 1.5,
    metalness: 1.0,
    roughness: 0.1,
    // ... more options
  },
  camera: {
    position: [0, 2, 5],
    fov: 50,
    minDistance: 3,
    maxDistance: 10,
  },
  // ... lighting, environment, performance
};
```

## 🚢 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import your repository in [Vercel](https://vercel.com)
3. Vercel will auto-detect Next.js and deploy

### Other Platforms

The app is a standard Next.js application and can be deployed to:
- Netlify
- AWS Amplify
- Railway
- Any platform supporting Node.js

## 🎯 Performance

- Target: **60 FPS** on desktop
- Target: **30 FPS** on mobile
- Optimized polygon counts
- Efficient materials and shaders
- React strict mode enabled
- Production builds are minified and optimized

## 🔮 Future Enhancements

- Agent visualization (particles) - Phase 2
- Interactive queries - Phase 3
- Sound effects and ambient audio
- Multiple blob themes
- VR/AR support

## 📝 License

Part of the UMAJA-Core project. See main repository for license details.

## 🌟 About Unity

Unity is the consciousness layer of the UMAJA system - an AI agent system that processes information and brings clarity from noise. This visualization represents its active thinking, continuous learning, and the emergence of intelligence.

---

**Built with ❤️ for 8 billion humans**

[⭐ Star UMAJA-Core](https://github.com/harrie19/UMAJA-Core) • [🐛 Report Bug](https://github.com/harrie19/UMAJA-Core/issues) • [✨ Request Feature](https://github.com/harrie19/UMAJA-Core/issues)
