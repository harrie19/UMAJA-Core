# 🥽 WhiteLab Reality Analyser Guide

## Overview

The WhiteLab Reality Analyser is a complete futuristic 3D visualization system for the UMAJA Reality Agent. It provides Hollywood-quality graphics, real-time data streaming, and holographic UI elements to visualize system health and reality checks.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   WHITELAB REALITY ANALYSER                  │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌──────────┐      ┌──────────────┐   ┌─────────────┐
    │ 3D UI    │      │  WebSocket   │   │  Streamlit  │
    │ (React)  │◄────►│   Server     │◄──│  Dashboard  │
    │          │      │  (Node.js)   │   │  (Python)   │
    └──────────┘      └──────────────┘   └─────────────┘
         │                    │                   │
         │                    ▼                   │
         │           ┌─────────────────┐          │
         └──────────►│ Reality Agent   │◄─────────┘
                     │   (Python)      │
                     └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Reality Checks │
                     │  (JSON/MD)      │
                     └─────────────────┘
```

## Components

### 1. Reality Agent (Python)
- **File**: `src/reality_agent.py`
- **Purpose**: Core system that runs proactive reality checks
- **Output**: JSON and Markdown reports in `data/reality_checks/`

### 2. WebSocket Server (Node.js)
- **File**: `server/reality-stream.js`
- **Purpose**: Streams reality check data in real-time to connected clients
- **Port**: 3002
- **Protocol**: Socket.io

### 3. 3D UI (React Three Fiber)
- **Files**: `src/3d/*`
- **Purpose**: Immersive 3D visualization of reality data
- **Port**: 3000 (Vite dev server)

**Components**:
- **WhiteLaboratory**: White room environment with reflective floor
- **IridescentBlob**: Central sphere that reacts to system status
- **HolographicPanel**: Glassmorphism UI panels displaying data
- **DNAHelix**: Animated helix representing data flow
- **ParticleCloud**: 5000+ particle system for organic visualization

### 4. Streamlit Dashboard (Python)
- **File**: `reality_dashboard.py`
- **Purpose**: Interactive web dashboard with charts and metrics
- **Port**: 8501 (default Streamlit port)

## Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Quick Setup

```bash
# Run the setup script
./scripts/setup-reality-lab.sh
```

### Manual Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies
npm install

# 3. Install server dependencies
cd server && npm install && cd ..

# 4. Create directories
mkdir -p data/reality_checks
```

## Running the System

You'll need **3 terminal windows** to run all components:

### Terminal 1: WebSocket Server

```bash
cd server
node reality-stream.js
```

**Expected output**:
```
🥽 Reality Stream Server
==================================================
🚀 Server running on port 3002
📁 Repository: /path/to/UMAJA-Core
🔍 Reality Agent: /path/to/src/reality_agent.py
==================================================

Waiting for client connections...
```

### Terminal 2: 3D Frontend

```bash
npm run dev
```

**Expected output**:
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

Open browser to `http://localhost:3000`

### Terminal 3: Streamlit Dashboard

```bash
streamlit run reality_dashboard.py
```

**Expected output**:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## API Reference

### WebSocket Events

**Server → Client Events:**

| Event | Data Type | Description |
|-------|-----------|-------------|
| `reality-update` | `RealityData` | Reality check results |
| `reality-error` | `ErrorData` | Error during check execution |
| `connect` | - | Connection established |
| `disconnect` | - | Connection closed |

**Client → Server Events:**

| Event | Description |
|-------|-------------|
| `request-update` | Manually trigger a reality check |

### Data Types

**RealityData**:
```typescript
{
  timestamp: string;           // ISO 8601 timestamp
  overall_status: string;      // "HEALTHY" | "WARNING" | "CRITICAL"
  checks: RealityCheck[];      // Array of individual checks
}
```

**RealityCheck**:
```typescript
{
  name: string;                // Check name
  status: string;              // "OK" | "WARNING" | "CRITICAL" | "ERROR"
  confidence: number;          // 0.0 to 1.0
  message: string;             // Human-readable message
  details: object;             // Additional check-specific data
  timestamp: string;           // Check execution time
}
```

## Customization

### Changing Colors

Edit `src/3d/components/IridescentBlob.tsx`:

```typescript
const getColorByStatus = (status: string): string => {
  switch (status?.toUpperCase()) {
    case 'OK':
      return '#00ff88'; // Change this for OK status
    case 'WARNING':
      return '#ffaa00'; // Change this for WARNING
    // ...
  }
};
```

### Adjusting Particle Count

Edit `src/3d/RealityLabUI.tsx`:

```typescript
<ParticleCloud 
  count={5000}  // Change this number
  status={realityData?.overall_status}
/>
```

### Modifying Check Interval

Edit `server/reality-stream.js`:

```javascript
checkInterval = setInterval(async () => {
  // ...
}, 10000);  // Change 10000 to desired milliseconds
```

### Custom Reality Checks

Add new checks in `src/reality_agent.py`:

```python
def my_custom_check(self) -> RealityCheck:
    """Custom reality check"""
    # Your check logic here
    return RealityCheck(
        name="My Custom Check",
        status="OK",
        confidence=1.0,
        message="Check passed",
        details={},
        timestamp=datetime.now(timezone.utc).isoformat()
    )
```

Then add to check list:

```python
checks = [
    # ... existing checks
    ("My Custom Check", self.sensor.my_custom_check),
]
```

## Troubleshooting

### Issue: WebSocket Connection Failed

**Symptoms**: Red "DISCONNECTED" indicator in 3D UI

**Solutions**:
1. Ensure server is running: `cd server && node reality-stream.js`
2. Check port 3002 is not in use: `lsof -i :3002`
3. Check firewall settings
4. Verify `REACT_APP_REALITY_STREAM_URL` environment variable

### Issue: 3D Scene Not Rendering

**Symptoms**: Black screen or console errors

**Solutions**:
1. Check browser console for errors (F12)
2. Ensure WebGL is supported: Visit `https://get.webgl.org/`
3. Update graphics drivers
4. Try a different browser (Chrome recommended)
5. Check if `node_modules` is installed: `npm install`

### Issue: Reality Agent Fails

**Symptoms**: Server logs show Python errors

**Solutions**:
1. Verify Python dependencies: `pip install -r requirements.txt`
2. Check Python version: `python --version` (need 3.8+)
3. Ensure repository structure is intact
4. Check file permissions

### Issue: Streamlit Dashboard Shows No Data

**Symptoms**: "No reality check data found" error

**Solutions**:
1. Run Reality Agent first: `python src/reality_agent.py`
2. Check `data/reality_checks/` directory exists
3. Verify JSON files are being created
4. Check file permissions on data directory

### Issue: High CPU/GPU Usage

**Solutions**:
1. Reduce particle count in `ParticleCloud`
2. Lower camera `fov` in `RealityLabUI.tsx`
3. Disable `Environment` lighting preset
4. Close other GPU-intensive applications

## Performance Optimization

### For Low-End Systems

1. **Reduce Particle Count**:
```typescript
<ParticleCloud count={1000} /> // Instead of 5000
```

2. **Lower Geometry Resolution**:
```typescript
<sphereGeometry args={[1, 64, 64]} /> // Instead of 128
```

3. **Disable Reflections**:
Comment out `MeshReflectorMaterial` in `WhiteLaboratory.tsx`

4. **Reduce Check Frequency**:
Increase interval in `reality-stream.js` to 30000 (30 seconds)

### For High-End Systems

1. **Increase Visual Fidelity**:
```typescript
resolution={4096} // In MeshReflectorMaterial
```

2. **More Particles**:
```typescript
<ParticleCloud count={10000} />
```

3. **Add Post-Processing**:
```typescript
import { EffectComposer, Bloom } from '@react-three/postprocessing';
// Add to Canvas
```

## Deployment

### GitHub Pages (Static Build)

```bash
npm run build
# Deploy 'dist/' folder to GitHub Pages
```

### Railway Backend

The system is designed to work with existing Railway backend:
- URL: `https://umaja-core-production.up.railway.app`
- Configure in `.env`: `REACT_APP_BACKEND_URL=...`

### Docker (Optional)

```dockerfile
# Dockerfile example
FROM node:18 as frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --from=frontend /app/dist ./dist
COPY . .
CMD ["gunicorn", "wsgi:app"]
```

## Philosophy

The WhiteLab Reality Analyser embodies the **Reality Glasses** philosophy:

- ✅ **PROACTIVE over Reactive**: Continuously monitors system health
- ✅ **VERIFY over Assume**: Checks facts, doesn't guess
- ✅ **TRUTH over Plausibility**: Measures reality with confidence scores
- ✅ **REALITY over Hallucination**: Uses sensors, not assumptions

And Bahá'í principles:
- **Truth**: Reports verified facts only
- **Service**: Serves proactively without being asked
- **Humility**: Admits uncertainty via confidence scores
- **Unity**: Serves all users equally

## Contributing

When adding features:
1. Maintain the minimalist white aesthetic
2. Keep confidence scores for all checks
3. Follow TypeScript strict mode
4. Document all complex calculations
5. Test on multiple browsers
6. Optimize for 60 FPS performance

## Support

For issues or questions:
- Check this guide first
- Review console logs (browser & server)
- Test individual components
- Check GitHub issues

## Credits

Built with:
- React Three Fiber (3D rendering)
- drei (3D helpers)
- Socket.io (real-time communication)
- Streamlit (dashboard)
- Sentence Transformers (semantic analysis)

Inspired by:
- Bahá'í principles of Truth, Service, and Unity
- Reality Glasses philosophy
- Hollywood sci-fi aesthetics

---

*"The purpose of the Reality Agent is to serve truth with humility"* 🥽✨
