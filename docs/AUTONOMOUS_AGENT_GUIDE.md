# UMAJA Autonomous Agent System Guide

## 🤖 Welcome to the Future of AI Automation!

The UMAJA Autonomous Agent System allows you to control everything with natural language. Just chat naturally and say "Accept" - the AI handles ALL technical operations automatically!

Think of it like **JARVIS from Iron Man** - you just talk, and the AI does everything behind the scenes.

## 🌟 What Can It Do?

The autonomous agent can handle:

- **PR Operations**: Merge, close, fix conflicts
- **Deployment**: Deploy to Railway, Render, or GitHub Pages
- **Code Generation**: Create features, write tests, update docs
- **Status Checks**: Get system status anytime
- **Self-Healing**: Automatically fix issues every 6 hours
- **Multi-Language**: Understands English and German

## 🚀 Quick Start

### Method 1: API Endpoints

```bash
# Send a command
curl -X POST https://your-umaja-instance.com/api/agent/command \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Merge PR #90",
    "require_approval": true
  }'

# Get system status
curl https://your-umaja-instance.com/api/agent/status

# Get help
curl https://your-umaja-instance.com/api/agent/help?lang=en
```

### Method 2: GitHub Actions

Create an issue with your command:

```
Title: Autonomous Agent Command
Body: Merge PR #90
```

The agent will respond automatically!

### Method 3: Workflow Dispatch

Go to Actions → Autonomous Holographic Agent → Run workflow

Enter your command: `Deploy to Railway`

## 📝 Available Commands

### PR Operations

**English:**
- `Merge PR #90` - Merge a pull request
- `Close PR #89` - Close a pull request  
- `Close old PRs` - Cleanup old pull requests
- `Fix conflicts in PR #87` - Resolve merge conflicts
- `Accept PR #90` - Same as merge

**German:**
- `Merge PR #90` - PR zusammenführen
- `Schließe PR #89` - PR schließen
- `Schließe alte PRs` - Alte PRs aufräumen
- `Konflikte lösen in PR #87` - Konflikte beheben
- `Akzeptiere PR #90` - PR akzeptieren

### Deployment Operations

**English:**
- `Deploy to Railway` - Deploy to Railway platform
- `Deploy to Render` - Deploy to Render platform
- `Deploy to production` - Deploy to production

**German:**
- `Deploy zu Railway` - Auf Railway deployen
- `Deploy zu Render` - Auf Render deployen
- `Veröffentliche auf Railway` - Veröffentlichen

### Code & Features

**English:**
- `Create feature: User dashboard` - Generate feature code
- `Create issue: Bug in login` - Create new issue
- `Implement: Payment system` - Implement feature

**German:**
- `Erstelle Feature: Benutzer-Dashboard` - Feature erstellen
- `Erstelle Issue: Bug im Login` - Issue erstellen
- `Implementiere: Zahlungssystem` - Feature implementieren

### Status & Help

**English:**
- `What's the status?` - Check system status
- `Show status` - Display status
- `Help` - Get help

**German:**
- `Was ist der Status?` - Status prüfen
- `Zeige Status` - Status anzeigen
- `Hilfe` - Hilfe anzeigen

## 🔒 Security Features

### Approval Requirements

Destructive operations require explicit approval by default:

```python
# With approval (safe, default)
result = await agent.process_command("Merge PR #90", require_approval=True)
# Returns: {'status': 'awaiting_approval'}

# Without approval (use with caution)
result = await agent.process_command("Merge PR #90", require_approval=False)
# Returns: {'success': True}
```

### What Requires Approval?

- Merging PRs
- Closing PRs
- Closing multiple old PRs
- Any destructive GitHub operations

### Safe Operations (No Approval)

- Status checks
- Creating issues
- Getting PR information
- Help commands

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────┐
│       Master Orchestrator               │
│  (Routes commands to agents)            │
└─────────────────────────────────────────┘
                │
                ├─────────────────┬─────────────────┬──────────────────┐
                │                 │                 │                  │
        ┌───────▼────────┐ ┌─────▼─────┐  ┌───────▼────────┐ ┌──────▼────────┐
        │ NL Command     │ │  GitHub   │  │  Deployment   │ │    Coding     │
        │  Processor     │ │  Agent    │  │    Agent      │ │    Agent      │
        └────────────────┘ └───────────┘  └───────────────┘ └───────────────┘
                │                 │                 │                  │
        Understands         Merges PRs       Deploys to       Generates Code
        German/English      Fixes Conflicts  Railway/Render   Writes Tests
```

### Data Flow

1. **User Input** → Natural language command
2. **NL Processor** → Parses intent and parameters
3. **Orchestrator** → Routes to appropriate agent
4. **Agent** → Executes operation
5. **Response** → Returns result to user

## 🔧 Configuration

### Environment Variables

```bash
# GitHub Operations
GITHUB_TOKEN=your_github_token
GITHUB_REPO_OWNER=harrie19
GITHUB_REPO_NAME=UMAJA-Core

# Deployment
RAILWAY_TOKEN=your_railway_token
RENDER_API_KEY=your_render_key

# Agent Behavior
LOG_LEVEL=INFO
DEPLOYMENT_TIMEOUT=300

# Energy Monitoring
ENABLE_ENERGY_MONITORING=true
ENERGY_ALERT_THRESHOLD=50.0
```

### Config File

Location: `src/autonomous/config.py`

```python
from autonomous.config import get_config

config = get_config()
print(config['github'])  # GitHub settings
print(config['deployment'])  # Deployment settings
```

## 💡 Examples

### Example 1: Merge Workflow

```python
import asyncio
from autonomous.master_orchestrator import MasterOrchestrator

async def merge_pr():
    orchestrator = MasterOrchestrator()
    
    # User: "Merge PR #90"
    result = await orchestrator.process_command("Merge PR #90")
    
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    if result['success']:
        print("✅ PR merged successfully!")
    elif result['status'] == 'awaiting_approval':
        print("⏳ Waiting for approval...")

asyncio.run(merge_pr())
```

### Example 2: Deployment Workflow

```python
async def deploy_application():
    orchestrator = MasterOrchestrator()
    
    # Deploy to Railway with health checks
    result = await orchestrator.process_command("Deploy to Railway")
    
    if result['success']:
        print(f"✅ Deployed to: {result.get('url')}")
    else:
        print(f"❌ Deployment failed: {result.get('error')}")

asyncio.run(deploy_application())
```

### Example 3: Feature Creation Workflow

```python
async def create_feature():
    orchestrator = MasterOrchestrator()
    
    # Multi-step workflow: code generation → tests → docs → PR
    result = await orchestrator.process_command(
        "Create feature: Add user authentication system"
    )
    
    # Check workflow steps
    for step in result.get('steps', []):
        print(f"{step['step']}: {step['result']['success']}")

asyncio.run(create_feature())
```

## 🔍 Monitoring & Debugging

### Check System Status

```bash
curl https://your-umaja-instance.com/api/agent/status
```

Response:
```json
{
  "success": true,
  "agents": {
    "nl_processor": "online",
    "github_agent": "online",
    "deployment_agent": "online",
    "coding_agent": "online"
  },
  "operations": {
    "total_processed": 42,
    "recent_operations": [...]
  }
}
```

### View Operation History

```bash
curl https://your-umaja-instance.com/api/agent/history?limit=10
```

### Energy Monitoring

```bash
curl https://your-umaja-instance.com/api/energy/report
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test autonomous agents
pytest tests/test_autonomous_agent.py -v

# Test holographic AI
pytest tests/test_holographic_ai.py -v

# Test all
pytest tests/test_*.py -v
```

## 🛠️ Extending the System

### Add New Command Pattern

Edit `data/command_patterns.json`:

```json
{
  "my_action": [
    {
      "pattern": "do\\s+something\\s+(\\w+)",
      "lang": "en",
      "groups": ["parameter"]
    }
  ]
}
```

### Add New Agent

Create `src/autonomous/my_agent.py`:

```python
class MyAgent:
    async def do_something(self, param):
        # Your logic here
        return {'success': True}
```

Integrate in `master_orchestrator.py`:

```python
from .my_agent import MyAgent

self.my_agent = MyAgent()
```

## 🌐 Integration with Holographic AI

The autonomous agent integrates with the holographic AI system:

```python
async def process_with_holographic():
    orchestrator = MasterOrchestrator()
    
    # Holographic AI enhances decision making
    if orchestrator.holographic_ai:
        # Self-healing kicks in
        await orchestrator.self_heal()
        
        # Get holographic insights
        health = orchestrator.holographic_ai.get_system_health()
        print(f"System health: {health}")

asyncio.run(process_with_holographic())
```

## 📊 Best Practices

### 1. Always Use Approval for Production

```python
# ✅ Good - Safe for production
await orchestrator.process_command(
    "Merge PR #90", 
    require_approval=True
)

# ❌ Bad - Dangerous in production
await orchestrator.process_command(
    "Merge PR #90",
    require_approval=False
)
```

### 2. Handle Errors Gracefully

```python
result = await orchestrator.process_command(command)

if not result['success']:
    if 'suggestion' in result:
        print(f"Try: {result['suggestion']}")
    logger.error(f"Error: {result['error']}")
```

### 3. Monitor Energy Usage

```python
from energy_monitor import get_energy_monitor

monitor = get_energy_monitor()
report = monitor.get_report()

if report['efficiency']['score'] < 0.8:
    print("⚠️ Low efficiency - optimize operations")
```

### 4. Regular Self-Healing

The system automatically self-heals every 6 hours via GitHub Actions schedule. You can also trigger manually:

```python
await orchestrator.self_heal()
```

## 🎯 Troubleshooting

### Command Not Understood

```python
# Low confidence
result = await orchestrator.process_command("asdfghjkl")
# Result: {'success': False, 'error': 'Could not understand command'}
```

**Solution**: Use help command to see available commands.

### Operation Awaiting Approval

```python
# Requires approval
result = await orchestrator.process_command("Merge PR #90")
# Result: {'status': 'awaiting_approval'}
```

**Solution**: Set `require_approval=False` (use with caution) or implement approval workflow.

### Agent Offline

```python
# Check status first
status = await orchestrator._get_system_status()
print(status['agents'])
```

**Solution**: Check logs and restart affected agent.

## 📚 Additional Resources

- [Holographic AI Guide](HOLOGRAPHIC_AI_GUIDE.md)
- [API Documentation](../api/README.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Energy Monitor Guide](../VECTOR_UNIVERSE_ENERGIE.md)

## 🚀 Next Steps

1. **Try It Out**: Send your first command via API
2. **Set Up Approvals**: Configure approval workflow
3. **Enable Monitoring**: Turn on energy and operation monitoring
4. **Customize**: Add your own command patterns
5. **Deploy**: Enable GitHub Actions workflow

---

**Remember**: The autonomous agent is designed to make you feel like you have superpowers. Just chat naturally, say "Accept", and watch the magic happen! 🌟

**Made with ❤️ by the UMAJA Team**

*"The earth is but one country, and mankind its citizens." - Bahá'u'lláh*
