# White Room Lab Usage Guide

## Getting Started

### First Launch

When you first open the White Room Lab, you'll see:

1. **White Room Environment**: A clean, minimalist 3D space
2. **Blue Bubble**: The AI agent floating in the center
3. **Chat Interface**: Bottom-left corner for text input
4. **System Status**: Top-right corner showing metrics
5. **Voice Input**: Bottom-right (if supported)

### Basic Navigation

#### Mouse Controls

- **Left Click + Drag**: Rotate camera around the scene
- **Right Click + Drag**: Pan camera (move view)
- **Scroll Wheel**: Zoom in/out
- **Click Blue Bubble**: Trigger speech bubble

#### Keyboard Shortcuts (Planned)

- `Space`: Toggle physics simulation
- `R`: Reset camera position
- `1-9`: Quick transform presets
- `Esc`: Close modals
- `Enter`: Send chat message

## Interacting with Blue Bubble

### Speech Bubbles

The Blue Bubble communicates through speech bubbles that appear above it.

- **Automatic Dismiss**: Speech bubbles fade after 5 seconds
- **Hover Effect**: Bubble glows brighter when you hover over it
- **Click Interaction**: Click to see greeting message

### Transformations

The Blue Bubble can transform into many different forms:

#### Available Forms (Week 1)

1. **Bubble** (default) - Pulsating sphere
2. **Human** - Humanoid silhouette
3. **DNA** - Double helix structure
4. **Turbine** - Mechanical turbine
5. **Neural Network** - Connected nodes

#### How to Transform

**German Commands:**
```
"Verwandle dich in DNA"
"Werde zu einem Menschen"
"Sei eine Turbine"
```

**English Commands:**
```
"Transform into DNA"
"Become a human"
"Be a turbine"
```

## Using the Chat Interface

### Message Types

#### User Messages (Blue, Right-aligned)
Your commands and questions appear on the right side in blue bubbles.

#### AI Messages (Gray, Left-aligned)
Blue Bubble's responses appear on the left side in gray bubbles.

### Command Categories

#### 1. Transform Commands

Transform the Blue Bubble into different forms.

**Examples:**
- `"Verwandle dich in DNA"`
- `"Transform into human"`
- `"Werde zu einer Turbine"`

**Response:**
Blue Bubble acknowledges and begins transformation animation.

#### 2. Build Commands

Request to build objects in the lab.

**Examples:**
- `"Baue eine Gasturbine"`
- `"Erstelle ein Molekül"`
- `"Build a neural network"`

**Response:**
Blue Bubble requests permission to install necessary tools.

#### 3. Simulate Commands

Run simulations and tests.

**Examples:**
- `"Simuliere Luftstrom"`
- `"Test the turbine"`
- `"Analysiere die Struktur"`

**Response:**
Blue Bubble initializes simulation systems.

#### 4. Query Commands

Ask questions and request information.

**Examples:**
- `"Was ist deine aktuelle Form?"`
- `"Zeig mir GitHub PRs"`
- `"What can you do?"`

**Response:**
Blue Bubble provides information and explanations.

### Chat Features

- **Auto-scroll**: Automatically scrolls to latest message
- **Message History**: Keeps all conversation visible
- **Enter to Send**: Press Enter to send (Shift+Enter for new line)
- **Responsive**: Adjusts size on mobile devices

## Permission System

### When Permissions Are Requested

The Blue Bubble will ask permission when it needs to:

1. **Install Tools**: CAD software, simulation engines
2. **Access APIs**: GitHub, external databases
3. **Execute Code**: Run simulations or computations
4. **Use Resources**: Heavy CPU/GPU operations

### Permission Modal

When a permission is requested, a modal appears with:

#### Information Displayed

- **Action**: What the AI wants to do
- **Tool Name**: Software/library to be used
- **Size**: Download/install size
- **Source**: Where the tool comes from
- **Risk Level**: 🟢 Low / 🟡 Medium / 🔴 High

#### Your Options

1. **✅ ACCEPT**: Grant permission and proceed
2. **❌ REJECT**: Deny permission (AI will explain alternatives)
3. **ℹ️ MORE INFO**: Get detailed explanation before deciding

### Risk Levels Explained

#### 🟢 Low Risk
- Open source, verified packages
- Small size (<5 MB)
- From trusted sources (npm, GitHub)
- No system access required

**Examples:**
- Three.js helpers
- Math libraries
- Visualization tools

#### 🟡 Medium Risk
- Third-party packages
- Moderate size (5-50 MB)
- Limited system access
- Popular but not verified

**Examples:**
- CAD engines
- Simulation frameworks
- External APIs

#### 🔴 High Risk
- Unverified sources
- Large size (>50 MB)
- System-level access
- New/untested packages

**Examples:**
- Custom compiled code
- System utilities
- Experimental features

## Voice Input

### Enabling Voice Input

1. Click the microphone button (bottom-right)
2. Browser will ask for microphone permission
3. Grant permission when prompted
4. Microphone button turns red and pulses when listening

### Using Voice Commands

1. Click microphone button to start
2. Speak your command clearly
3. Transcript appears below button
4. Command is automatically sent to chat
5. Click button again to stop listening

### Supported Languages

- **German (de-DE)**: Primary language
- **English (en-US)**: Secondary language
- Auto-detection based on browser settings

### Troubleshooting Voice Input

**"Microphone button not visible"**
- Voice input not supported in your browser
- Use text chat instead

**"No transcript appearing"**
- Speak louder or closer to microphone
- Check browser microphone permissions
- Background noise may interfere

**"Wrong language detected"**
- Switch browser language settings
- Use text chat for mixed-language commands

## System Status Monitor

### Metrics Explained

#### FPS (Frames Per Second)
- **Green (≥50)**: Smooth performance
- **Yellow (<50)**: Reduced performance
- **Target**: 60 FPS

#### Objects
- Number of 3D objects in the scene
- Includes Blue Bubble, walls, floor, created objects

#### Physics
- **🟢 Active**: Physics simulation running
- **🔴 Inactive**: Physics disabled or paused

#### Form
- Current shape of Blue Bubble
- Updates when transformations occur

#### Simulations
- Number of active simulations running
- 0 = idle, 1+ = simulations in progress

## Advanced Features (Coming Soon)

### Object Creation
- Build complex 3D objects
- CAD-style editing
- Material customization

### Simulations
- Fluid dynamics
- Thermal analysis
- Structural testing
- Particle systems

### Collaboration
- Multi-user sessions
- Shared workspaces
- Real-time synchronization

### Export/Import
- Save scenes as files
- Load previous work
- Share with others

## Tips & Tricks

### Performance Optimization

1. **Reduce Camera Distance**: Closer view = better performance
2. **Limit Objects**: Remove unused objects from scene
3. **Disable Shadows**: If FPS drops below 30
4. **Close Other Tabs**: Free up browser resources

### Best Practices

1. **Clear Commands**: Be specific in your requests
2. **One Action at a Time**: Don't combine multiple commands
3. **Wait for Completion**: Let transformations finish before next command
4. **Check Permissions**: Review what you're accepting
5. **Monitor FPS**: Keep eye on performance

### Common Patterns

**Iteration Loop:**
```
1. "Baue eine Turbine" → ACCEPT permission
2. "Simuliere Luftstrom" → Review results
3. "Optimiere die Form" → Repeat
```

**Exploration:**
```
1. "Verwandle dich in DNA" → Observe structure
2. "Zeig mir Details" → Learn about components
3. "Vergleiche mit Protein" → Compare forms
```

## Troubleshooting

### Common Issues

**Blue Bubble not visible**
- Zoom out (scroll wheel)
- Reset camera position
- Refresh page

**Chat not responding**
- Check internet connection
- Verify command syntax
- Refresh page

**Low FPS / Lag**
- Close other browser tabs
- Reduce number of objects
- Check browser hardware acceleration
- Update graphics drivers

**Permission modal stuck**
- Click ACCEPT or REJECT
- Refresh page if unresponsive
- Check browser console for errors

**Voice input not working**
- Grant microphone permissions
- Check browser compatibility
- Use text chat as fallback

## Keyboard Shortcuts Quick Reference

| Key | Action |
|-----|--------|
| Enter | Send chat message |
| Esc | Close modals |
| Space | Toggle physics (planned) |
| R | Reset camera (planned) |
| 1-9 | Quick transforms (planned) |

## Best Supported Browsers

- ✅ **Chrome 90+**: Full support
- ✅ **Edge 90+**: Full support
- ⚠️ **Firefox 88+**: Good support (voice limited)
- ⚠️ **Safari 14+**: Good support (voice limited)

## Getting Help

### Resources

- **Documentation**: [Full docs](/docs)
- **GitHub Issues**: [Report bugs](https://github.com/harrie19/UMAJA-Core/issues)
- **Email**: Umaja1919@googlemail.com

### Debug Information

When reporting issues, include:
- Browser and version
- System Status metrics (FPS, object count)
- Command that caused issue
- Error messages from browser console

---

*Enjoy exploring and creating in the White Room Lab!* 🔵
