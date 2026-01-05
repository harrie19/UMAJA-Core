# 🥽 WhiteLab Reality Analyser

A futuristic 3D visualization system for the UMAJA Reality Agent, featuring Hollywood-quality graphics and real-time data streaming.

## Quick Start

### 1. Install Dependencies

```bash
# Run the automated setup script
./scripts/setup-reality-lab.sh
```

Or manually:

```bash
# Python dependencies
pip install -r requirements.txt

# Frontend dependencies
npm install

# Server dependencies
cd server && npm install
```

### 2. Run the System

You need **3 terminals**:

**Terminal 1 - WebSocket Server:**
```bash
cd server
node reality-stream.js
```

**Terminal 2 - 3D Frontend:**
```bash
npm run dev
```
Then open http://localhost:3000

**Terminal 3 - Streamlit Dashboard:**
```bash
streamlit run reality_dashboard.py
```
Then open http://localhost:8501

## Components

### 🎨 3D Scene
- **WhiteLaboratory**: Minimalist white room with reflective floor
- **IridescentBlob**: Central sphere with chromatic aberration that reacts to system status
- **HolographicPanel**: Transparent UI panels with glassmorphism effect
- **DNAHelix**: Animated spiral representing data flow
- **ParticleCloud**: 5000+ instanced particles for ambient visualization

### 🔌 Real-time Streaming
- WebSocket server streams reality checks every 10 seconds
- Live connection status indicator
- Manual refresh capability
- Automatic reconnection on disconnect

### 📊 Streamlit Dashboard
- System metrics overview
- Individual check details
- Confidence score charts
- Status distribution
- Auto-refresh every 10 seconds

## Features

✨ **Visual Effects:**
- Reflective surfaces using `MeshReflectorMaterial`
- Chromatic aberration on central blob
- Glassmorphism UI panels
- Smooth animations with `useFrame`
- Performance-optimized with instanced rendering

🎯 **Status Reactivity:**
- 🟢 Green = OK/Healthy
- 🟡 Yellow = Warning
- 🔴 Red = Critical/Error
- Colors update in real-time across all components

📡 **Data Flow:**
```
Reality Agent (Python)
         ↓
  WebSocket Server
         ↓
    ┌────┴────┐
    ↓         ↓
 3D UI   Dashboard
```

## Architecture

- **Frontend**: React + Three.js + React Three Fiber
- **Server**: Node.js + Socket.io + Express
- **Agent**: Python + Sentence Transformers
- **Dashboard**: Streamlit + Pandas

## Configuration

### Change WebSocket URL

Edit `.env` or set environment variable:
```bash
VITE_REALITY_STREAM_URL=http://localhost:3002
```

### Adjust Particle Count

Edit `src/3d/RealityLabUI.tsx`:
```typescript
<ParticleCloud count={5000} />  // Change to 1000 for low-end systems
```

### Change Check Interval

Edit `server/reality-stream.js`:
```javascript
setInterval(async () => {
  // ...
}, 10000);  // 10 seconds - change to 30000 for 30 seconds
```

## Performance

**System Requirements:**
- Modern browser with WebGL 2.0 support
- 4GB RAM (8GB recommended)
- Dedicated GPU (recommended)

**Optimization Tips:**
- Reduce particle count for low-end systems
- Disable floor reflections if needed
- Increase check interval to reduce CPU usage
- Close other GPU-intensive applications

## Troubleshooting

### WebSocket Connection Failed
1. Ensure server is running on port 3002
2. Check firewall settings
3. Verify `VITE_REALITY_STREAM_URL` in `.env` file

### Black Screen
1. Check browser console (F12)
2. Verify WebGL support: https://get.webgl.org/
3. Update graphics drivers
4. Try different browser (Chrome recommended)

### High CPU Usage
1. Reduce particle count
2. Lower geometry resolution
3. Disable reflections
4. Increase check interval

## Documentation

Full documentation: [docs/REALITY_LAB_GUIDE.md](docs/REALITY_LAB_GUIDE.md)

## Philosophy

This system embodies the **Reality Glasses** philosophy:

- ✅ **PROACTIVE** - Monitors before problems arise
- ✅ **VERIFY** - Checks facts, doesn't guess
- ✅ **TRUTH** - Reports confidence scores
- ✅ **REALITY** - Uses sensors, not assumptions

And Bahá'í principles:
- **Truth**: Reports verified facts only
- **Service**: Serves proactively
- **Humility**: Admits uncertainty
- **Unity**: Serves all equally

## Credits

Built with:
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [drei](https://github.com/pmndrs/drei) - Three.js helpers
- [Socket.io](https://socket.io/) - Real-time communication
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Sentence Transformers](https://www.sbert.net/) - Semantic analysis

---

*"Serving Truth with Humility"* 🥽✨
