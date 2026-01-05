#!/usr/bin/env node
/**
 * Reality Stream Server
 * WebSocket server for streaming Reality Agent data in real-time
 * 
 * Philosophy: PROACTIVE streaming - Push reality checks to clients automatically
 */

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

const PORT = process.env.PORT || 3002;
const REPO_ROOT = path.resolve(__dirname, '..');
const REALITY_AGENT_PATH = path.join(REPO_ROOT, 'src', 'reality_agent.py');

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    service: 'reality-stream-server',
    timestamp: new Date().toISOString()
  });
});

/**
 * Run reality check and return parsed results
 */
function runRealityCheck() {
  return new Promise((resolve, reject) => {
    console.log('🔍 Running reality check...');
    
    const python = spawn('python', [REALITY_AGENT_PATH], {
      cwd: REPO_ROOT
    });

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    python.on('close', (code) => {
      if (code !== 0) {
        console.error('❌ Reality check failed:', stderr);
        reject(new Error(`Reality check exited with code ${code}`));
        return;
      }

      try {
        // Find the latest JSON file
        const fs = require('fs');
        const checksDir = path.join(REPO_ROOT, 'data', 'reality_checks');
        
        if (!fs.existsSync(checksDir)) {
          throw new Error('Reality checks directory not found');
        }

        const files = fs.readdirSync(checksDir)
          .filter(f => f.endsWith('.json'))
          .map(f => ({
            name: f,
            time: fs.statSync(path.join(checksDir, f)).mtime.getTime()
          }))
          .sort((a, b) => b.time - a.time);

        if (files.length === 0) {
          throw new Error('No reality check results found');
        }

        const latestFile = path.join(checksDir, files[0].name);
        const data = JSON.parse(fs.readFileSync(latestFile, 'utf8'));
        
        console.log('✅ Reality check complete');
        resolve(data);
      } catch (error) {
        console.error('❌ Error parsing reality check results:', error);
        reject(error);
      }
    });

    // Timeout after 60 seconds
    setTimeout(() => {
      python.kill();
      reject(new Error('Reality check timeout'));
    }, 60000);
  });
}

/**
 * Handle client connections
 */
io.on('connection', (socket) => {
  console.log('👤 Client connected:', socket.id);
  
  let checkInterval = null;

  // Send initial reality check immediately
  runRealityCheck()
    .then(data => {
      socket.emit('reality-update', data);
    })
    .catch(error => {
      socket.emit('reality-error', { 
        message: error.message,
        timestamp: new Date().toISOString()
      });
    });

  // Schedule periodic checks every 10 seconds
  checkInterval = setInterval(async () => {
    try {
      const data = await runRealityCheck();
      socket.emit('reality-update', data);
    } catch (error) {
      socket.emit('reality-error', { 
        message: error.message,
        timestamp: new Date().toISOString()
      });
    }
  }, 10000);

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('👋 Client disconnected:', socket.id);
    if (checkInterval) {
      clearInterval(checkInterval);
    }
  });

  // Handle manual refresh request
  socket.on('request-update', async () => {
    console.log('🔄 Manual update requested by:', socket.id);
    try {
      const data = await runRealityCheck();
      socket.emit('reality-update', data);
    } catch (error) {
      socket.emit('reality-error', { 
        message: error.message,
        timestamp: new Date().toISOString()
      });
    }
  });
});

// Start server
server.listen(PORT, () => {
  console.log('🥽 Reality Stream Server');
  console.log('=' .repeat(50));
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📁 Repository: ${REPO_ROOT}`);
  console.log(`🔍 Reality Agent: ${REALITY_AGENT_PATH}`);
  console.log('=' .repeat(50));
  console.log('');
  console.log('Waiting for client connections...');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('👋 SIGTERM received, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Server closed');
    process.exit(0);
  });
});
