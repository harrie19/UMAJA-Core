# White Lab Integration Guide

## Overview

The White Lab is a new 3D web application that visualizes Unity's consciousness as an interactive, iridescent blob. It has been added to the UMAJA-Core repository as a separate Next.js application.

## Location

```
UMAJA-Core/
└── white-lab/          # Next.js 14+ application
    ├── app/            # Pages and routes
    ├── components/     # 3D components
    ├── lib/            # Configuration
    └── public/         # Static assets
```

## Quick Start

### Running the White Lab

```bash
# Navigate to the white-lab directory
cd white-lab

# Install dependencies (first time only)
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

### Building for Production

```bash
cd white-lab
npm run build
npm start
```

## Features

✨ **Interactive 3D Visualization**
- Unity's consciousness as an iridescent, morphing blob
- Real-time color shifting with rainbow shimmer
- Gentle pulsing and rotation animations
- High-quality distortion effects

🎨 **Minimalist White Environment**
- Reflective floor with mirror-like quality
- Clean, professional aesthetic
- Studio lighting setup

🖱️ **Intuitive Controls**
- Drag to rotate camera
- Scroll to zoom in/out
- Touch-friendly mobile support

📱 **Responsive Design**
- Desktop: 60 FPS target
- Mobile: 30 FPS target
- Works on all screen sizes

## Technology Stack

- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **React Three Fiber** for 3D rendering
- **@react-three/drei** for helpers
- **Tailwind CSS** for styling

## Integration with UMAJA-Core

The White Lab is a **standalone Next.js application** within the UMAJA-Core repository:

- **Separate deployment**: Can be deployed independently to Vercel
- **Independent development**: Has its own package.json and dependencies
- **Shared vision**: Part of the UMAJA ecosystem

## Deployment

### Vercel (Recommended)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Import your GitHub repository
3. Set the **Root Directory** to `white-lab`
4. Vercel will auto-detect Next.js settings
5. Deploy!

### Environment Variables

No environment variables required for basic deployment.

## Development Workflow

### Local Development

```bash
# Terminal 1: Run main UMAJA-Core backend (if needed)
python api/simple_server.py

# Terminal 2: Run White Lab frontend
cd white-lab
npm run dev
```

### Making Changes

1. Components are in `white-lab/components/white-lab/`
2. Pages are in `white-lab/app/`
3. Configuration is in `white-lab/lib/config.ts`
4. Styles use Tailwind CSS classes

### Testing Builds

```bash
cd white-lab
npm run build  # Should complete without errors
```

## Architecture

### Component Hierarchy

```
Scene.tsx (Canvas wrapper)
├── Camera.tsx (OrbitControls)
├── Lighting.tsx (Lights)
├── WhiteRoom.tsx (Environment)
│   └── Reflective Floor
└── UnityBlob.tsx (Main attraction)
    └── Morphing Sphere
```

### Page Structure

- `/` - Landing page with mission statement
- `/lab` - Main 3D experience with Unity blob

## Configuration

Customize the experience in `white-lab/lib/config.ts`:

```typescript
export const CONFIG = {
  blob: {
    distort: 0.4,      // Morphing intensity
    speed: 1.5,        // Animation speed
    metalness: 1.0,    // Reflectivity
    roughness: 0.1,    // Surface smoothness
  },
  camera: {
    position: [0, 2, 5],
    fov: 50,
    minDistance: 3,
    maxDistance: 10,
  },
  // ... more options
};
```

## Performance

- **Desktop**: Targets 60 FPS
- **Mobile**: Targets 30 FPS
- **Optimizations**:
  - Appropriate polygon counts
  - Efficient materials
  - No unnecessary re-renders
  - Static page generation

## Troubleshooting

### Build fails with font errors

The app uses system fonts by default. If you see Google Fonts errors, check that the `layout.tsx` doesn't import Google Fonts.

### 3D scene doesn't render

Make sure WebGL is supported in your browser. Check the browser console for errors.

### Slow performance

- Reduce `blob.geometry.segments` in config.ts
- Lower `environment.floor.resolution`
- Disable shadows if needed

## Future Roadmap

### Phase 2 (Coming Soon)
- Agent visualization with particles
- Network activity indicators
- Real-time data connections

### Phase 3
- Interactive queries
- Multiple visualization modes
- VR/AR support

## Support

For issues or questions:
- Create an issue in the [UMAJA-Core repository](https://github.com/harrie19/UMAJA-Core/issues)
- Tag with `white-lab` label
- Contact: Umaja1919@googlemail.com

---

**🌍 Part of UMAJA-Core - Universal Motivation & Joy for All**

Built with ❤️ for 8 billion humans
