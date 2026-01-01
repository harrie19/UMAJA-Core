# UMAJA-Core Deployment Guide

**Version:** 1.0  
**Last Updated:** 2026-01-01  
**Maintained By:** UMAJA Development Team

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [GitHub Pages Setup](#github-pages-setup)
5. [Backend Deployment](#backend-deployment)
6. [CDN Configuration & Testing](#cdn-configuration--testing)
7. [Environment Configuration](#environment-configuration)
8. [Verification & Testing](#verification--testing)
9. [Cost Breakdown](#cost-breakdown)
10. [Scaling Considerations](#scaling-considerations)
11. [Monitoring & Maintenance](#monitoring--maintenance)
12. [Troubleshooting Guide](#troubleshooting-guide)
13. [Emergency Procedures](#emergency-procedures)
14. [Rollback Procedures](#rollback-procedures)
15. [Security Best Practices](#security-best-practices)

---

## Overview

UMAJA-Core is a modern web application designed for high availability and scalability. This guide covers the complete deployment process for production environments, including GitHub Pages for static frontend hosting, backend services, CDN integration, and operational procedures.

### Deployment Architecture
- **Frontend:** GitHub Pages (Static hosting)
- **Backend:** Cloud-based API services
- **CDN:** Content delivery network for global distribution
- **Database:** Managed database service
- **Monitoring:** Application performance monitoring (APM)

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CDN Layer                             │
│  (CloudFlare/AWS CloudFront/Azure CDN)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────────┐
│  GitHub Pages │         │   API Gateway    │
│   (Frontend)  │         │   (Backend)      │
└───────────────┘         └────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌──────────┐   ┌──────────┐   ┌──────────┐
            │   Auth   │   │   Core   │   │  Media   │
            │ Service  │   │ Service  │   │ Service  │
            └────┬─────┘   └────┬─────┘   └────┬─────┘
                 │              │              │
                 └──────────────┼──────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Database Cluster    │
                    │  (Primary + Replica)  │
                    └───────────────────────┘
```

### Component Details

#### Frontend (GitHub Pages)
- **Hosting:** GitHub Pages
- **Domain:** Custom domain with SSL/TLS
- **Build:** Static HTML/CSS/JavaScript
- **Framework:** React/Vue/Vanilla JS

#### Backend Services
- **API Gateway:** NGINX/Kong/AWS API Gateway
- **Authentication:** JWT-based auth service
- **Core Service:** Main application logic
- **Media Service:** File upload and processing

#### Data Layer
- **Primary Database:** PostgreSQL/MySQL (Production)
- **Read Replicas:** For read-heavy operations
- **Cache:** Redis for session and data caching
- **Object Storage:** S3-compatible for media files

---

## Prerequisites

### Required Tools
- **Git:** Version 2.30 or higher
- **Node.js:** Version 18.x or higher
- **npm/yarn:** Latest stable version
- **Docker:** Version 20.x or higher (for backend)
- **kubectl:** For Kubernetes deployments (optional)

### Required Accounts
- GitHub account with repository access
- Cloud provider account (AWS/Azure/GCP)
- Domain registrar access
- CDN provider account
- Monitoring service account (DataDog/New Relic/etc.)

### Access Requirements
- Repository admin access for GitHub Pages configuration
- Cloud infrastructure admin access
- DNS management access
- SSL certificate management access

---

## GitHub Pages Setup

### Step 1: Repository Configuration

1. **Navigate to Repository Settings**
   ```bash
   # Clone the repository
   git clone https://github.com/harrie19/UMAJA-Core.git
   cd UMAJA-Core
   ```

2. **Enable GitHub Pages**
   - Go to: `Settings` → `Pages`
   - Source: Select `Deploy from a branch`
   - Branch: Select `main` (or `gh-pages`)
   - Folder: Select `/ (root)` or `/docs`
   - Click **Save**

3. **Configure Build Settings**
   
   Create `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   concurrency:
     group: "pages"
     cancel-in-progress: false

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout
           uses: actions/checkout@v4

         - name: Setup Node.js
           uses: actions/setup-node@v4
           with:
             node-version: '18'
             cache: 'npm'

         - name: Install dependencies
           run: npm ci

         - name: Build
           run: npm run build
           env:
             NODE_ENV: production
             VITE_API_URL: ${{ secrets.API_URL }}
             VITE_CDN_URL: ${{ secrets.CDN_URL }}

         - name: Setup Pages
           uses: actions/configure-pages@v4

         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: './dist'

     deploy:
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       runs-on: ubuntu-latest
       needs: build
       steps:
         - name: Deploy to GitHub Pages
           id: deployment
           uses: actions/deploy-pages@v4
   ```

### Step 2: Custom Domain Configuration

1. **Add Custom Domain**
   - In GitHub Pages settings, add your custom domain
   - Example: `umaja.yourdomain.com`

2. **Configure DNS Records**
   
   Add the following DNS records at your domain registrar:
   ```
   # A Records (IPv4)
   A     @    185.199.108.153
   A     @    185.199.109.153
   A     @    185.199.110.153
   A     @    185.199.111.153

   # AAAA Records (IPv6)
   AAAA  @    2606:50c0:8000::153
   AAAA  @    2606:50c0:8001::153
   AAAA  @    2606:50c0:8002::153
   AAAA  @    2606:50c0:8003::153

   # CNAME for subdomain
   CNAME umaja harrie19.github.io
   ```

3. **Verify DNS Propagation**
   ```bash
   # Check DNS propagation
   nslookup umaja.yourdomain.com
   
   # Or use dig
   dig umaja.yourdomain.com +short
   ```

### Step 3: Enable HTTPS

1. **Enforce HTTPS**
   - In GitHub Pages settings, check "Enforce HTTPS"
   - Wait for SSL certificate to be provisioned (can take up to 24 hours)

2. **Verify SSL Certificate**
   ```bash
   # Check SSL certificate
   openssl s_client -connect umaja.yourdomain.com:443 -servername umaja.yourdomain.com
   ```

### Step 4: Build Configuration

1. **Create Production Build Script**
   
   Update `package.json`:
   ```json
   {
     "scripts": {
       "dev": "vite",
       "build": "vite build",
       "build:prod": "NODE_ENV=production vite build",
       "preview": "vite preview",
       "deploy": "npm run build:prod && gh-pages -d dist"
     }
   }
   ```

2. **Configure Base URL**
   
   Update `vite.config.js` (or webpack config):
   ```javascript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   export default defineConfig({
     plugins: [react()],
     base: process.env.NODE_ENV === 'production' ? '/' : '/',
     build: {
       outDir: 'dist',
       sourcemap: false,
       minify: 'terser',
       rollupOptions: {
         output: {
           manualChunks: {
             vendor: ['react', 'react-dom'],
             router: ['react-router-dom']
           }
         }
       }
     }
   })
   ```

---

## Backend Deployment

### Option 1: Docker Container Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM node:18-alpine AS builder

   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production

   COPY . .
   RUN npm run build

   FROM node:18-alpine
   WORKDIR /app

   COPY --from=builder /app/dist ./dist
   COPY --from=builder /app/node_modules ./node_modules
   COPY package*.json ./

   EXPOSE 3000

   ENV NODE_ENV=production
   CMD ["node", "dist/server.js"]
   ```

2. **Build and Push Docker Image**
   ```bash
   # Build image
   docker build -t umaja-core-backend:latest .

   # Tag for registry
   docker tag umaja-core-backend:latest registry.example.com/umaja-core-backend:latest

   # Push to registry
   docker push registry.example.com/umaja-core-backend:latest
   ```

3. **Deploy with Docker Compose**
   ```yaml
   version: '3.8'

   services:
     backend:
       image: registry.example.com/umaja-core-backend:latest
       ports:
         - "3000:3000"
       environment:
         - NODE_ENV=production
         - DATABASE_URL=${DATABASE_URL}
         - REDIS_URL=${REDIS_URL}
         - JWT_SECRET=${JWT_SECRET}
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
         interval: 30s
         timeout: 10s
         retries: 3

     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       depends_on:
         - backend
       restart: unless-stopped
   ```

### Option 2: Kubernetes Deployment

1. **Create Deployment Manifest**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: umaja-backend
     namespace: production
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: umaja-backend
     template:
       metadata:
         labels:
           app: umaja-backend
       spec:
         containers:
         - name: backend
           image: registry.example.com/umaja-core-backend:latest
           ports:
           - containerPort: 3000
           env:
           - name: NODE_ENV
             value: "production"
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: umaja-secrets
                 key: database-url
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
           livenessProbe:
             httpGet:
               path: /health
               port: 3000
             initialDelaySeconds: 30
             periodSeconds: 10
           readinessProbe:
             httpGet:
               path: /ready
               port: 3000
             initialDelaySeconds: 5
             periodSeconds: 5
   ```

2. **Create Service**
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: umaja-backend-service
     namespace: production
   spec:
     selector:
       app: umaja-backend
     ports:
     - protocol: TCP
       port: 80
       targetPort: 3000
     type: LoadBalancer
   ```

3. **Deploy to Kubernetes**
   ```bash
   # Apply configurations
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml

   # Verify deployment
   kubectl get pods -n production
   kubectl get services -n production
   ```

### Backend Verification

```bash
# Check health endpoint
curl -i https://api.umaja.com/health

# Expected response:
# HTTP/2 200
# Content-Type: application/json
# {"status":"healthy","timestamp":"2026-01-01T12:16:31.000Z"}

# Check version endpoint
curl https://api.umaja.com/version

# Test authentication endpoint
curl -X POST https://api.umaja.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass"}'
```

---

## CDN Configuration & Testing

### CloudFlare Setup

1. **Add Site to CloudFlare**
   ```bash
   # Update nameservers at domain registrar
   ns1.cloudflare.com
   ns2.cloudflare.com
   ```

2. **Configure SSL/TLS**
   - Go to SSL/TLS settings
   - Set encryption mode to "Full (strict)"
   - Enable "Always Use HTTPS"
   - Enable "Automatic HTTPS Rewrites"

3. **Create Page Rules**
   ```
   Rule 1: Cache Everything
   URL: umaja.yourdomain.com/*
   Settings:
     - Cache Level: Cache Everything
     - Edge Cache TTL: 1 month
     - Browser Cache TTL: 4 hours

   Rule 2: Force HTTPS
   URL: http://umaja.yourdomain.com/*
   Settings:
     - Always Use HTTPS: On
   ```

4. **Enable Performance Features**
   - Auto Minify: HTML, CSS, JavaScript
   - Brotli compression
   - HTTP/2 and HTTP/3
   - 0-RTT Connection Resumption

### AWS CloudFront Setup

1. **Create Distribution**
   ```bash
   # Using AWS CLI
   aws cloudfront create-distribution \
     --origin-domain-name harrie19.github.io \
     --default-root-object index.html \
     --viewer-protocol-policy redirect-to-https
   ```

2. **Configure Origin Settings**
   ```json
   {
     "Origins": {
       "Items": [{
         "Id": "github-pages",
         "DomainName": "harrie19.github.io",
         "CustomOriginConfig": {
           "HTTPPort": 80,
           "HTTPSPort": 443,
           "OriginProtocolPolicy": "https-only",
           "OriginSslProtocols": {
             "Items": ["TLSv1.2"],
             "Quantity": 1
           }
         }
       }]
     }
   }
   ```

3. **Configure Cache Behaviors**
   ```json
   {
     "CacheBehaviors": [{
       "PathPattern": "/static/*",
       "TargetOriginId": "github-pages",
       "ViewerProtocolPolicy": "redirect-to-https",
       "AllowedMethods": ["GET", "HEAD", "OPTIONS"],
       "CachedMethods": ["GET", "HEAD"],
       "Compress": true,
       "DefaultTTL": 86400,
       "MaxTTL": 31536000,
       "MinTTL": 0
     }]
   }
   ```

### CDN Testing

1. **Test CDN Performance**
   ```bash
   # Test response headers
   curl -I https://umaja.yourdomain.com

   # Look for CDN headers:
   # cf-cache-status: HIT (CloudFlare)
   # x-cache: Hit from cloudfront (AWS)
   # x-cdn: Served from CDN

   # Test from multiple locations
   curl -w "@curl-format.txt" -o /dev/null -s https://umaja.yourdomain.com
   ```

2. **Create curl-format.txt**
   ```
   time_namelookup:  %{time_namelookup}s\n
   time_connect:     %{time_connect}s\n
   time_appconnect:  %{time_appconnect}s\n
   time_pretransfer: %{time_pretransfer}s\n
   time_redirect:    %{time_redirect}s\n
   time_starttransfer: %{time_starttransfer}s\n
   ----------\n
   time_total:       %{time_total}s\n
   ```

3. **Performance Testing Tools**
   ```bash
   # Use WebPageTest
   # Visit: https://www.webpagetest.org/
   # Test URL: https://umaja.yourdomain.com

   # Use GTmetrix
   # Visit: https://gtmetrix.com/
   # Test URL: https://umaja.yourdomain.com

   # Use Lighthouse
   npx lighthouse https://umaja.yourdomain.com --view
   ```

### Cache Invalidation

**CloudFlare:**
```bash
# Purge everything
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'

# Purge specific files
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://umaja.yourdomain.com/style.css"]}'
```

**AWS CloudFront:**
```bash
# Create invalidation
aws cloudfront create-invalidation \
  --distribution-id EDFDVBD6EXAMPLE \
  --paths "/*"

# Check invalidation status
aws cloudfront get-invalidation \
  --distribution-id EDFDVBD6EXAMPLE \
  --id IDFDVBD6EXAMPLE
```

---

## Environment Configuration

### Frontend Environment Variables

Create `.env.production`:
```env
# API Configuration
VITE_API_URL=https://api.umaja.com
VITE_API_VERSION=v1
VITE_API_TIMEOUT=30000

# CDN Configuration
VITE_CDN_URL=https://cdn.umaja.com
VITE_STATIC_URL=https://static.umaja.com

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_TRACKING=true
VITE_ENABLE_PERFORMANCE_MONITORING=true

# Third-party Services
VITE_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
VITE_SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# Application Settings
VITE_APP_NAME=UMAJA Core
VITE_APP_VERSION=1.0.0
VITE_APP_ENV=production
```

### Backend Environment Variables

Create `.env.production`:
```env
# Application
NODE_ENV=production
PORT=3000
APP_NAME=UMAJA-Core-Backend
APP_VERSION=1.0.0

# Database
DATABASE_URL=postgresql://user:pass@host:5432/umaja_prod
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10
DATABASE_SSL=true

# Redis
REDIS_URL=redis://user:pass@host:6379
REDIS_TLS=true
REDIS_DB=0

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_EXPIRATION=7d
JWT_REFRESH_EXPIRATION=30d
BCRYPT_ROUNDS=12

# API Configuration
API_RATE_LIMIT=100
API_RATE_WINDOW=15m
CORS_ORIGIN=https://umaja.yourdomain.com

# Storage
S3_BUCKET=umaja-prod-storage
S3_REGION=us-east-1
S3_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
S3_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# Monitoring
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
LOG_LEVEL=info
ENABLE_METRICS=true

# Email Service
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=notifications@umaja.com
SMTP_PASSWORD=smtp-password
SMTP_FROM=noreply@umaja.com
```

### Secrets Management

**Using GitHub Secrets:**
```bash
# Add secrets via GitHub CLI
gh secret set API_URL --body "https://api.umaja.com"
gh secret set CDN_URL --body "https://cdn.umaja.com"
gh secret set DATABASE_URL --body "postgresql://..."
```

**Using Kubernetes Secrets:**
```bash
# Create secret from file
kubectl create secret generic umaja-secrets \
  --from-file=.env.production \
  --namespace=production

# Or create from literals
kubectl create secret generic umaja-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=jwt-secret='your-secret' \
  --namespace=production
```

---

## Verification & Testing

### Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] SSL certificates valid
- [ ] DNS records properly configured
- [ ] Database migrations completed
- [ ] Backup systems in place
- [ ] Monitoring configured
- [ ] CDN properly configured
- [ ] Load balancer health checks passing

### Automated Testing

1. **Health Check Script**
   ```bash
   #!/bin/bash
   # health-check.sh

   FRONTEND_URL="https://umaja.yourdomain.com"
   BACKEND_URL="https://api.umaja.com"

   echo "Checking frontend..."
   FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL)
   if [ $FRONTEND_STATUS -eq 200 ]; then
     echo "✓ Frontend is up (HTTP $FRONTEND_STATUS)"
   else
     echo "✗ Frontend is down (HTTP $FRONTEND_STATUS)"
     exit 1
   fi

   echo "Checking backend..."
   BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BACKEND_URL/health)
   if [ $BACKEND_STATUS -eq 200 ]; then
     echo "✓ Backend is up (HTTP $BACKEND_STATUS)"
   else
     echo "✗ Backend is down (HTTP $BACKEND_STATUS)"
     exit 1
   fi

   echo "All systems operational!"
   ```

2. **End-to-End Testing**
   ```javascript
   // e2e/deployment-test.spec.js
   const { test, expect } = require('@playwright/test');

   test('deployment verification', async ({ page }) => {
     // Test frontend loads
     await page.goto('https://umaja.yourdomain.com');
     await expect(page).toHaveTitle(/UMAJA/);

     // Test API connectivity
     const response = await page.request.get('https://api.umaja.com/health');
     expect(response.status()).toBe(200);

     // Test authentication flow
     await page.goto('https://umaja.yourdomain.com/login');
     await page.fill('[name="email"]', 'test@example.com');
     await page.fill('[name="password"]', 'testpass');
     await page.click('button[type="submit"]');
     
     await expect(page).toHaveURL(/dashboard/);
   });
   ```

### Performance Verification

```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 https://umaja.yourdomain.com/

# Load testing with Artillery
artillery quick --count 100 --num 10 https://api.umaja.com/health

# Stress testing with k6
k6 run --vus 100 --duration 30s load-test.js
```

---

## Cost Breakdown

### Monthly Infrastructure Costs (Estimated)

#### Hosting Costs

| Service | Provider | Tier | Monthly Cost |
|---------|----------|------|--------------|
| Frontend Hosting | GitHub Pages | Free | $0.00 |
| Backend Hosting | AWS EC2 (t3.medium) | 2 vCPU, 4GB RAM | $30.00 |
| Database | AWS RDS (db.t3.small) | PostgreSQL | $25.00 |
| Redis Cache | AWS ElastiCache (cache.t3.micro) | Single node | $12.00 |
| Object Storage | AWS S3 | 100GB + requests | $5.00 |
| Load Balancer | AWS ALB | Standard | $20.00 |

**Subtotal:** $92.00/month

#### CDN & Networking

| Service | Provider | Usage | Monthly Cost |
|---------|----------|-------|--------------|
| CDN | CloudFlare | Pro plan | $20.00 |
| Data Transfer | AWS | 1TB outbound | $90.00 |
| DNS | CloudFlare | Included | $0.00 |

**Subtotal:** $110.00/month

#### Monitoring & Tools

| Service | Provider | Tier | Monthly Cost |
|---------|----------|------|--------------|
| Error Tracking | Sentry | Team plan | $26.00 |
| APM | New Relic | Standard | $49.00 |
| Uptime Monitoring | UptimeRobot | Pro | $7.00 |
| Log Management | Papertrail | 5GB/month | $7.00 |

**Subtotal:** $89.00/month

#### Additional Services

| Service | Description | Monthly Cost |
|---------|-------------|--------------|
| Email Service | SendGrid (50k emails) | $15.00 |
| SSL Certificates | Let's Encrypt | $0.00 |
| Backups | AWS S3 (snapshots) | $10.00 |
| Domain Registration | Amortized annual cost | $1.50 |

**Subtotal:** $26.50/month

### Total Monthly Cost: **$317.50**

### Cost Optimization Tips

1. **Use Reserved Instances:** Save 30-50% on EC2/RDS with 1-year commitment
2. **S3 Lifecycle Policies:** Move old data to Glacier ($0.004/GB)
3. **CloudFront Free Tier:** 1TB data transfer on AWS CloudFront
4. **Spot Instances:** For non-critical workloads (up to 90% savings)
5. **Database Right-Sizing:** Monitor and adjust instance sizes quarterly

### Scaling Cost Projections

| Users | Monthly Cost | Notes |
|-------|--------------|-------|
| 0-10K | $318 | Initial setup |
| 10K-50K | $650 | Add read replica, scale backend |
| 50K-100K | $1,200 | Multi-AZ deployment, CDN premium |
| 100K-500K | $3,500 | Kubernetes cluster, advanced monitoring |
| 500K+ | $10,000+ | Enterprise solutions, dedicated support |

---

## Scaling Considerations

### Horizontal Scaling

#### Auto-Scaling Configuration (AWS)

```yaml
# Auto Scaling Group configuration
ScalingPolicy:
  Type: AWS::AutoScaling::ScalingPolicy
  Properties:
    AutoScalingGroupName: !Ref BackendAutoScalingGroup
    PolicyType: TargetTrackingScaling
    TargetTrackingConfiguration:
      PredefinedMetricSpecification:
        PredefinedMetricType: ASGAverageCPUUtilization
      TargetValue: 70.0

BackendAutoScalingGroup:
  Type: AWS::AutoScaling::AutoScalingGroup
  Properties:
    MinSize: 2
    MaxSize: 10
    DesiredCapacity: 2
    HealthCheckType: ELB
    HealthCheckGracePeriod: 300
```

#### Kubernetes Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: umaja-backend-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: umaja-backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
```

### Vertical Scaling

#### Database Scaling

```sql
-- Monitor database performance
SELECT * FROM pg_stat_database WHERE datname = 'umaja_prod';

-- Check connection usage
SELECT count(*) FROM pg_stat_activity;

-- Analyze slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

**Scaling Steps:**
1. Monitor CPU/Memory usage consistently above 80%
2. Enable read replicas for read-heavy workloads
3. Upgrade instance size during maintenance window
4. Implement connection pooling (PgBouncer)
5. Consider database sharding for massive scale

### Caching Strategy

```javascript
// Redis caching implementation
const redis = require('redis');
const client = redis.createClient({
  url: process.env.REDIS_URL,
  socket: {
    tls: true,
    rejectUnauthorized: true
  }
});

// Cache middleware
async function cacheMiddleware(req, res, next) {
  const key = `cache:${req.originalUrl}`;
  
  try {
    const cached = await client.get(key);
    if (cached) {
      return res.json(JSON.parse(cached));
    }
    
    // Store original res.json
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      // Cache for 5 minutes
      client.setEx(key, 300, JSON.stringify(data));
      return originalJson(data);
    };
    
    next();
  } catch (error) {
    console.error('Cache error:', error);
    next();
  }
}
```

### Database Optimization

1. **Connection Pooling**
   ```javascript
   // PostgreSQL connection pool
   const { Pool } = require('pg');
   
   const pool = new Pool({
     connectionString: process.env.DATABASE_URL,
     min: 5,
     max: 20,
     idleTimeoutMillis: 30000,
     connectionTimeoutMillis: 2000,
   });
   ```

2. **Query Optimization**
   ```sql
   -- Add indexes for frequently queried fields
   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   
   -- Composite indexes
   CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);
   ```

3. **Read Replicas**
   ```javascript
   // Database connection manager
   class DatabaseManager {
     constructor() {
       this.primary = new Pool({ connectionString: process.env.DATABASE_PRIMARY_URL });
       this.replica = new Pool({ connectionString: process.env.DATABASE_REPLICA_URL });
     }
     
     // Write operations
     async write(query, params) {
       return this.primary.query(query, params);
     }
     
     // Read operations
     async read(query, params) {
       return this.replica.query(query, params);
     }
   }
   ```

### Load Balancing Strategy

```nginx
# NGINX load balancing configuration
upstream backend_servers {
    least_conn;
    
    server backend1.umaja.com:3000 max_fails=3 fail_timeout=30s;
    server backend2.umaja.com:3000 max_fails=3 fail_timeout=30s;
    server backend3.umaja.com:3000 max_fails=3 fail_timeout=30s;
    
    # Backup server
    server backup.umaja.com:3000 backup;
    
    keepalive 32;
}

server {
    listen 80;
    server_name api.umaja.com;
    
    location / {
        proxy_pass http://backend_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

---

## Monitoring & Maintenance

### Health Monitoring

1. **Application Health Endpoints**
   ```javascript
   // Health check endpoint
   app.get('/health', async (req, res) => {
     const health = {
       uptime: process.uptime(),
       timestamp: Date.now(),
       status: 'healthy',
       checks: {}
     };
     
     // Database check
     try {
       await db.query('SELECT 1');
       health.checks.database = 'healthy';
     } catch (error) {
       health.checks.database = 'unhealthy';
       health.status = 'degraded';
     }
     
     // Redis check
     try {
       await redis.ping();
       health.checks.redis = 'healthy';
     } catch (error) {
       health.checks.redis = 'unhealthy';
       health.status = 'degraded';
     }
     
     const statusCode = health.status === 'healthy' ? 200 : 503;
     res.status(statusCode).json(health);
   });
   ```

2. **Uptime Monitoring Setup**
   ```bash
   # Configure UptimeRobot monitors
   # Monitor 1: Frontend
   URL: https://umaja.yourdomain.com
   Type: HTTP(s)
   Interval: 5 minutes
   Alert Contacts: [email, SMS, Slack]
   
   # Monitor 2: Backend API
   URL: https://api.umaja.com/health
   Type: HTTP(s) - Keyword
   Keyword: "healthy"
   Interval: 5 minutes
   
   # Monitor 3: Database Connectivity
   URL: https://api.umaja.com/health
   Type: HTTP(s)
   Advanced: Check response time < 1000ms
   ```

### Performance Monitoring

1. **Application Performance Monitoring**
   ```javascript
   // New Relic integration
   require('newrelic');
   
   // Custom instrumentation
   const newrelic = require('newrelic');
   
   app.use((req, res, next) => {
     newrelic.setTransactionName(`${req.method} ${req.route?.path || req.path}`);
     next();
   });
   
   // Custom metrics
   function recordCustomMetric(name, value) {
     newrelic.recordMetric(`Custom/${name}`, value);
   }
   ```

2. **Error Tracking with Sentry**
   ```javascript
   const Sentry = require('@sentry/node');
   
   Sentry.init({
     dsn: process.env.SENTRY_DSN,
     environment: process.env.NODE_ENV,
     tracesSampleRate: 1.0,
     beforeSend(event, hint) {
       // Filter out sensitive data
       if (event.request) {
         delete event.request.cookies;
         delete event.request.headers.authorization;
       }
       return event;
     }
   });
   
   // Error handler
   app.use(Sentry.Handlers.errorHandler());
   ```

### Maintenance Windows

**Scheduled Maintenance:**
- **Time:** Every Sunday 2:00 AM - 4:00 AM UTC
- **Duration:** Maximum 2 hours
- **Notification:** 48 hours advance notice

**Maintenance Checklist:**
- [ ] Database backup verification
- [ ] Security patches applied
- [ ] Log rotation
- [ ] Certificate expiration check
- [ ] Dependency updates
- [ ] Performance metrics review
- [ ] Disk space cleanup
- [ ] Cache clearing

### Backup Strategy

```bash
#!/bin/bash
# backup.sh - Automated backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="umaja_prod"

# Database backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/db_$DATE.sql.gz s3://umaja-backups/database/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

# Verify backup
if [ $? -eq 0 ]; then
  echo "Backup successful: db_$DATE.sql.gz"
else
  echo "Backup failed!" | mail -s "Backup Alert" admin@umaja.com
fi
```

**Backup Schedule:**
- **Full Backups:** Daily at 1:00 AM UTC
- **Incremental:** Every 6 hours
- **Retention:** 30 days online, 1 year in cold storage
- **Testing:** Monthly restore test

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: GitHub Pages Not Updating

**Symptoms:**
- Changes pushed but site not reflecting updates
- Build succeeds but deployment fails

**Diagnosis:**
```bash
# Check GitHub Actions workflow status
gh run list --limit 5

# View specific run details
gh run view [RUN_ID]

# Check GitHub Pages status
curl -I https://harrie19.github.io/UMAJA-Core
```

**Solutions:**
1. Clear CDN cache
2. Force rebuild by pushing empty commit
   ```bash
   git commit --allow-empty -m "Trigger rebuild"
   git push
   ```
3. Check CNAME file exists in output directory
4. Verify custom domain configuration

#### Issue 2: API Connection Timeouts

**Symptoms:**
- Frontend shows connection errors
- API requests hang or timeout

**Diagnosis:**
```bash
# Test API connectivity
curl -v --max-time 10 https://api.umaja.com/health

# Check DNS resolution
dig api.umaja.com

# Test from different locations
curl --connect-timeout 5 https://api.umaja.com/health

# Check backend logs
kubectl logs -f deployment/umaja-backend -n production
```

**Solutions:**
1. Verify backend health: `curl https://api.umaja.com/health`
2. Check load balancer status
3. Verify security group/firewall rules
4. Increase timeout values in frontend
5. Check rate limiting configuration

#### Issue 3: Database Connection Pool Exhausted

**Symptoms:**
- "Connection pool exhausted" errors
- Slow API responses
- Backend crashes

**Diagnosis:**
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Check long-running queries
SELECT pid, now() - query_start as duration, query 
FROM pg_stat_activity 
WHERE state = 'active' AND now() - query_start > interval '5 minutes';

-- Check connection pool stats
SELECT * FROM pg_stat_database WHERE datname = 'umaja_prod';
```

**Solutions:**
1. Increase pool size temporarily
2. Kill long-running queries
   ```sql
   SELECT pg_terminate_backend(pid) 
   FROM pg_stat_activity 
   WHERE pid = [PID];
   ```
3. Implement connection pooling (PgBouncer)
4. Optimize slow queries
5. Scale database instance

#### Issue 4: High Memory Usage

**Symptoms:**
- OOM (Out of Memory) errors
- Container restarts
- Slow performance

**Diagnosis:**
```bash
# Check memory usage
kubectl top pods -n production

# Check resource limits
kubectl describe pod [POD_NAME] -n production

# View application logs
kubectl logs [POD_NAME] -n production --tail=100

# Check for memory leaks (Node.js)
node --expose-gc --inspect app.js
```

**Solutions:**
1. Increase memory limits
   ```yaml
   resources:
     limits:
       memory: "1Gi"
   ```
2. Enable garbage collection logging
3. Profile application for memory leaks
4. Implement proper resource cleanup
5. Add memory monitoring alerts

#### Issue 5: SSL Certificate Issues

**Symptoms:**
- Browser SSL warnings
- Certificate expired errors
- HTTPS not working

**Diagnosis:**
```bash
# Check certificate expiration
openssl s_client -connect umaja.yourdomain.com:443 -servername umaja.yourdomain.com 2>/dev/null | openssl x509 -noout -dates

# Check certificate chain
curl -vI https://umaja.yourdomain.com

# SSL Labs test
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=umaja.yourdomain.com
```

**Solutions:**
1. Renew certificate
   ```bash
   # Let's Encrypt renewal
   certbot renew --force-renewal
   ```
2. Update certificate in GitHub Pages settings
3. Clear browser cache
4. Verify certificate installation
5. Check intermediate certificates

### Debug Mode

```bash
# Enable debug logging
export DEBUG=* NODE_ENV=development

# Run with increased verbosity
node --trace-warnings app.js

# Enable request logging
export LOG_LEVEL=debug

# Profile performance
node --prof app.js
node --prof-process isolate-*.log > profile.txt
```

### Log Analysis

```bash
# Search for errors
kubectl logs -n production deployment/umaja-backend | grep -i error

# Count error types
kubectl logs -n production deployment/umaja-backend | grep -i error | sort | uniq -c

# Filter by time range
kubectl logs -n production deployment/umaja-backend --since=1h

# Follow logs in real-time
kubectl logs -f -n production deployment/umaja-backend
```

---

## Emergency Procedures

### Incident Response Plan

#### Severity Levels

**P0 - Critical (Complete Outage)**
- Complete service unavailability
- Data loss or corruption
- Security breach
- Response Time: Immediate
- Resolution Time: < 1 hour

**P1 - High (Major Impact)**
- Significant functionality degraded
- Performance severely impacted
- Affecting >50% of users
- Response Time: < 15 minutes
- Resolution Time: < 4 hours

**P2 - Medium (Partial Impact)**
- Some features unavailable
- Performance degraded
- Affecting <50% of users
- Response Time: < 1 hour
- Resolution Time: < 24 hours

**P3 - Low (Minor Impact)**
- Minor bugs or issues
- Workaround available
- Minimal user impact
- Response Time: < 4 hours
- Resolution Time: < 1 week

### Emergency Contacts

```
Primary On-Call: +1-XXX-XXX-XXXX (PagerDuty)
Secondary On-Call: +1-XXX-XXX-XXXX
Engineering Lead: engineer@umaja.com
DevOps Lead: devops@umaja.com
Security Team: security@umaja.com
Management: management@umaja.com

External Contacts:
- AWS Support: [Account Number]
- GitHub Support: [Enterprise Support]
- CloudFlare Support: [Account ID]
```

### Incident Response Workflow

```
1. DETECT
   └─> Monitoring alert or user report

2. ACKNOWLEDGE
   └─> On-call engineer acknowledges within SLA

3. ASSESS
   ├─> Determine severity
   ├─> Identify affected components
   └─> Estimate user impact

4. RESPOND
   ├─> Execute appropriate emergency procedure
   ├─> Communicate status to stakeholders
   └─> Document actions taken

5. RESOLVE
   ├─> Implement fix
   ├─> Verify resolution
   └─> Monitor for stability

6. POST-MORTEM
   ├─> Root cause analysis
   ├─> Document lessons learned
   └─> Implement preventive measures
```

### Emergency Procedures

#### Procedure 1: Complete Site Outage

```bash
#!/bin/bash
# emergency-outage.sh

echo "=== EMERGENCY: Complete Site Outage ==="
echo "Starting emergency recovery procedures..."

# 1. Verify outage
echo "Step 1: Verifying outage..."
curl -f https://umaja.yourdomain.com || echo "CONFIRMED: Frontend down"
curl -f https://api.umaja.com/health || echo "CONFIRMED: Backend down"

# 2. Check infrastructure
echo "Step 2: Checking infrastructure..."
kubectl get pods -n production
kubectl get services -n production

# 3. Check recent deployments
echo "Step 3: Checking recent changes..."
kubectl rollout history deployment/umaja-backend -n production

# 4. Enable maintenance mode
echo "Step 4: Enabling maintenance mode..."
kubectl apply -f maintenance-mode.yaml

# 5. Rollback if needed
read -p "Rollback to previous version? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    kubectl rollout undo deployment/umaja-backend -n production
fi

# 6. Notify team
echo "Step 5: Notifying team..."
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"🚨 EMERGENCY: Site outage detected. Recovery procedures initiated."}'

echo "Emergency procedures completed. Monitor status."
```

#### Procedure 2: Database Failure

```bash
#!/bin/bash
# emergency-database.sh

echo "=== EMERGENCY: Database Failure ==="

# 1. Check database status
echo "Checking database status..."
pg_isready -h $DB_HOST -p 5432

# 2. Switch to read replica
echo "Switching to read-only mode..."
kubectl set env deployment/umaja-backend DATABASE_URL=$DATABASE_REPLICA_URL -n production

# 3. Enable read-only mode in application
kubectl set env deployment/umaja-backend READ_ONLY_MODE=true -n production

# 4. Notify users
echo "Notifying users of degraded service..."
# Update status page

# 5. Attempt database recovery
echo "Attempting database recovery..."
# Contact cloud provider support
# Or execute recovery playbook

# 6. Restore from backup if necessary
if [ "$RESTORE_FROM_BACKUP" = "yes" ]; then
    echo "Restoring from most recent backup..."
    ./restore-database.sh --latest
fi
```

#### Procedure 3: Security Breach

```bash
#!/bin/bash
# emergency-security.sh

echo "=== EMERGENCY: Security Breach Detected ==="

# 1. ISOLATE
echo "Step 1: Isolating affected systems..."
# Block suspicious IPs
iptables -A INPUT -s SUSPICIOUS_IP -j DROP

# Disable compromised accounts
psql -U $DB_USER -d $DB_NAME -c "UPDATE users SET active = false WHERE id IN (...);"

# 2. ASSESS
echo "Step 2: Assessing damage..."
# Check access logs
tail -n 1000 /var/log/nginx/access.log | grep "SUSPICIOUS_PATTERN"

# 3. CONTAIN
echo "Step 3: Containing breach..."
# Rotate all secrets
./rotate-secrets.sh

# Force logout all users
redis-cli FLUSHDB

# 4. NOTIFY
echo "Step 4: Notifying stakeholders..."
# Send security alert
mail -s "SECURITY ALERT" security@umaja.com < security-alert.txt

# 5. DOCUMENT
echo "Step 5: Documenting incident..."
echo "Time: $(date)" >> security-incidents.log
echo "Details: Security breach detected" >> security-incidents.log

echo "Security procedures initiated. Escalating to security team."
```

#### Procedure 4: DDoS Attack

```bash
#!/bin/bash
# emergency-ddos.sh

echo "=== EMERGENCY: DDoS Attack Detected ==="

# 1. Enable DDoS protection
echo "Activating DDoS protection..."

# CloudFlare: Enable Under Attack Mode
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value":"under_attack"}'

# 2. Implement rate limiting
echo "Implementing aggressive rate limiting..."
kubectl apply -f rate-limit-strict.yaml

# 3. Block malicious traffic
echo "Analyzing and blocking attack patterns..."
# Get top attacking IPs
tail -n 10000 /var/log/nginx/access.log | \
  awk '{print $1}' | sort | uniq -c | sort -rn | head -20

# 4. Scale up infrastructure
echo "Scaling up to handle load..."
kubectl scale deployment/umaja-backend --replicas=20 -n production

# 5. Monitor situation
echo "Monitoring attack..."
watch -n 5 'curl -s https://api.umaja.com/health | jq .'

echo "DDoS mitigation active. Continue monitoring."
```

### Maintenance Mode

**Enable Maintenance Mode:**
```bash
# Create maintenance page
cat > maintenance.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>UMAJA - Maintenance</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>🔧 Scheduled Maintenance</h1>
    <p>We're currently performing scheduled maintenance.</p>
    <p>We'll be back shortly. Thank you for your patience.</p>
    <p>Estimated completion: [TIME]</p>
</body>
</html>
EOF

# Deploy maintenance page
gh-pages -d . -f maintenance.html

# Or use CDN to serve maintenance page
cloudflare-cli update-page-rule --redirect-to /maintenance.html
```

**Disable Maintenance Mode:**
```bash
# Redeploy normal site
npm run deploy

# Or remove maintenance page rule
cloudflare-cli delete-page-rule --id RULE_ID
```

### Communication Templates

**Outage Notification:**
```
Subject: [INCIDENT] UMAJA Service Disruption

We are currently experiencing a service disruption affecting [COMPONENT].

Status: Investigating
Impact: [DESCRIPTION]
Affected Users: [PERCENTAGE]%
Started: [TIME]
ETA: [TIME]

We are actively working to resolve this issue and will provide updates every 30 minutes.

Updates: https://status.umaja.com
Support: support@umaja.com
```

**Resolution Notification:**
```
Subject: [RESOLVED] UMAJA Service Restored

The service disruption has been resolved.

Duration: [DURATION]
Root Cause: [BRIEF DESCRIPTION]
Resolution: [BRIEF DESCRIPTION]

All systems are now operational. We apologize for any inconvenience.

A detailed post-mortem will be published within 48 hours.
```

---

## Rollback Procedures

### Quick Rollback

```bash
#!/bin/bash
# quick-rollback.sh

echo "=== Initiating Rollback ==="

# Rollback frontend (GitHub Pages)
echo "Rolling back frontend..."
git revert HEAD --no-edit
git push origin main

# Rollback backend (Kubernetes)
echo "Rolling back backend..."
kubectl rollout undo deployment/umaja-backend -n production

# Verify rollback
echo "Verifying rollback..."
kubectl rollout status deployment/umaja-backend -n production

# Run health checks
./health-check.sh

echo "Rollback complete. Monitor for stability."
```

### Database Migration Rollback

```bash
#!/bin/bash
# rollback-migration.sh

echo "=== Rolling back database migration ==="

# Rollback last migration
npm run migrate:rollback

# Or for specific migration
npm run migrate:rollback --to 20260101000000

# Verify database state
psql -U $DB_USER -d $DB_NAME -c "SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1;"

echo "Database migration rolled back."
```

### Version-Specific Rollback

```bash
# Rollback to specific version
kubectl rollout undo deployment/umaja-backend --to-revision=5 -n production

# Check revision history
kubectl rollout history deployment/umaja-backend -n production

# View specific revision
kubectl rollout history deployment/umaja-backend --revision=5 -n production
```

---

## Security Best Practices

### SSL/TLS Configuration

```nginx
# NGINX SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_stapling on;
ssl_stapling_verify on;

# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Content-Security-Policy "default-src 'self'" always;
```

### Secrets Rotation

```bash
#!/bin/bash
# rotate-secrets.sh

echo "=== Rotating Secrets ==="

# Generate new JWT secret
NEW_JWT_SECRET=$(openssl rand -hex 32)

# Update in Kubernetes
kubectl create secret generic umaja-secrets \
  --from-literal=jwt-secret=$NEW_JWT_SECRET \
  --dry-run=client -o yaml | kubectl apply -f -

# Rotate database password
NEW_DB_PASSWORD=$(openssl rand -base64 32)
# Update database password
# Update application config

# Rotate API keys
# ... rotate all third-party API keys

# Force restart to use new secrets
kubectl rollout restart deployment/umaja-backend -n production

echo "Secrets rotation complete."
```

### Security Scanning

```bash
# Scan dependencies for vulnerabilities
npm audit
npm audit fix

# Container security scanning
docker scan umaja-core-backend:latest

# Infrastructure security
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,IpPermissions]'
```

---

## Appendix

### Useful Commands

```bash
# GitHub Pages
gh-pages -d dist                    # Deploy to GitHub Pages
gh run list                         # List workflow runs
gh run view [RUN_ID]               # View specific run

# Kubernetes
kubectl get all -n production       # Get all resources
kubectl describe pod [NAME]         # Describe pod
kubectl logs -f [POD]              # Follow logs
kubectl exec -it [POD] -- /bin/sh  # Shell into pod
kubectl port-forward [POD] 8080:80 # Port forward

# Docker
docker ps                           # List containers
docker logs -f [CONTAINER]         # Follow logs
docker exec -it [CONTAINER] sh     # Shell into container
docker stats                        # Resource usage

# Database
psql -U user -d database           # Connect to PostgreSQL
pg_dump database > backup.sql      # Backup database
psql database < backup.sql         # Restore database

# Redis
redis-cli                          # Connect to Redis
redis-cli KEYS "*"                # List all keys
redis-cli FLUSHALL                # Clear all data
```

### Additional Resources

- **GitHub Pages Documentation:** https://docs.github.com/pages
- **Kubernetes Documentation:** https://kubernetes.io/docs/
- **Docker Documentation:** https://docs.docker.com/
- **AWS Documentation:** https://docs.aws.amazon.com/
- **CloudFlare Documentation:** https://developers.cloudflare.com/

### Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-01 | 1.0 | Initial deployment guide | UMAJA Team |

---

## Support

For deployment support:
- **Email:** devops@umaja.com
- **Slack:** #umaja-deployments
- **Emergency:** +1-XXX-XXX-XXXX (On-call)

---

**Document End**
