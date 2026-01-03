# UMAJA Core - Deployment Instructions

Complete step-by-step guide for deploying the UMAJA Core application to production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Railway)](#backend-deployment-railway)
3. [Frontend Deployment (GitHub Pages)](#frontend-deployment-github-pages)
4. [Configuration](#configuration)
5. [Verification Checklist](#verification-checklist)
6. [Troubleshooting](#troubleshooting)
7. [Expected URLs and Endpoints](#expected-urls-and-endpoints)

---

## Prerequisites

Before starting the deployment process, ensure you have:

- [ ] GitHub account with repository access
- [ ] Railway account (sign up at https://railway.app)
- [ ] Git installed locally
- [ ] Node.js and npm installed (for local testing)
- [ ] Repository cloned locally

---

## Backend Deployment (Railway)

### Step 1: Create Railway Account and Project

1. **Sign up/Login to Railway**
   - Visit https://railway.app
   - Sign in with your GitHub account
   - Authorize Railway to access your repositories

   ![Screenshot: Railway Login](_placeholder_railway_login.png)

2. **Create New Project**
   - Click "New Project" button
   - Select "Deploy from GitHub repo"
   - Choose the `harrie19/UMAJA-core` repository

   ![Screenshot: New Project Creation](_placeholder_railway_new_project.png)

### Step 2: Configure Backend Service

1. **Select Backend Directory**
   - Railway will auto-detect your application
   - If needed, set the root directory to `/backend` in project settings
   - Go to Settings → Service Settings

   ![Screenshot: Service Configuration](_placeholder_railway_service_config.png)

2. **Set Environment Variables**
   - Navigate to the "Variables" tab
   - Add the following required environment variables:

   ```env
   NODE_ENV=production
   PORT=8080
   DATABASE_URL=<your_database_connection_string>
   JWT_SECRET=<generate_secure_random_string>
   CORS_ORIGIN=https://<your-github-username>.github.io
   ```

   ![Screenshot: Environment Variables](_placeholder_railway_env_vars.png)

3. **Additional Configuration Variables** (if applicable)
   ```env
   API_VERSION=v1
   SESSION_SECRET=<generate_secure_random_string>
   MAX_REQUEST_SIZE=10mb
   RATE_LIMIT_WINDOW=15m
   RATE_LIMIT_MAX_REQUESTS=100
   ```

### Step 3: Database Setup (if required)

1. **Add Database Service**
   - Click "New" → "Database"
   - Choose your database (PostgreSQL, MySQL, MongoDB, etc.)
   - Railway will automatically provision the database

   ![Screenshot: Database Setup](_placeholder_railway_database.png)

2. **Link Database to Backend**
   - The `DATABASE_URL` will be automatically added to environment variables
   - Verify the connection string in the Variables tab

### Step 4: Deploy Backend

1. **Trigger Deployment**
   - Railway will automatically deploy when you push to your main branch
   - Or manually trigger deployment from the Railway dashboard
   - Monitor deployment logs in real-time

   ![Screenshot: Deployment Logs](_placeholder_railway_deploy_logs.png)

2. **Get Backend URL**
   - Once deployed, navigate to Settings → Domains
   - Click "Generate Domain" to get your Railway subdomain
   - Copy the URL (e.g., `https://umaja-core-production.up.railway.app`)

   ![Screenshot: Generated Domain](_placeholder_railway_domain.png)

---

## Frontend Deployment (GitHub Pages)

### Step 1: Configure Backend URL

1. **Update Frontend Configuration**
   - Open `frontend/src/config/api.js` (or equivalent config file)
   - Update the API base URL with your Railway backend URL:

   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_URL || 
                        'https://umaja-core-production.up.railway.app/api';
   
   export default API_BASE_URL;
   ```

2. **Update Environment Variables**
   - Create/update `.env.production` in the frontend directory:

   ```env
   REACT_APP_API_URL=https://umaja-core-production.up.railway.app/api
   REACT_APP_ENV=production
   ```

### Step 2: Build Frontend

1. **Local Build**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Verify Build**
   - Check that the `build` or `dist` folder is created
   - Verify the contents include `index.html`, assets, etc.

### Step 3: Enable GitHub Pages

1. **Access Repository Settings**
   - Go to https://github.com/harrie19/UMAJA-core
   - Click "Settings" tab
   - Scroll to "Pages" in the left sidebar

   ![Screenshot: GitHub Settings](_placeholder_github_settings.png)

2. **Configure GitHub Pages**
   - **Source**: Select "GitHub Actions" (recommended) or "Deploy from a branch"
   
   **Option A: Using GitHub Actions (Recommended)**
   - The repository already has `.github/workflows/pages-deploy.yml` configured for automatic GitHub Pages deployment when changes are made to the `docs/**` directory.
   
   **For Railway Deployment:**
   - Use `.github/workflows/railway-deploy.yml` which handles automatic Railway deployments.

   **Option B: Deploy from Branch**
   - Source: Select branch (e.g., `gh-pages`)
   - Folder: `/ (root)` or `/docs` depending on your setup
   - Click "Save"

   ![Screenshot: GitHub Pages Configuration](_placeholder_github_pages_config.png)

3. **Deploy**
   - If using GitHub Actions: Push your workflow file to trigger deployment
   - If using branch: Push your built files to the `gh-pages` branch
   
   ```bash
   # For manual branch deployment
   npm install -g gh-pages
   cd frontend
   npm run build
   gh-pages -d build
   ```

4. **Verify Deployment**
   - GitHub will show the deployment status
   - Your site will be available at: `https://harrie19.github.io/UMAJA-core/`

   ![Screenshot: Deployment Success](_placeholder_github_pages_success.png)

---

## Configuration

### Backend CORS Configuration

Ensure your backend allows requests from your GitHub Pages domain:

**In `backend/server.js` or middleware:**

```javascript
const cors = require('cors');

const corsOptions = {
  origin: [
    'https://harrie19.github.io',
    'http://localhost:3000' // for local development
  ],
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

### API Configuration

**Update all API endpoints in frontend:**

```javascript
// frontend/src/services/api.js
const API_URL = process.env.REACT_APP_API_URL || 
                'https://umaja-core-production.up.railway.app/api';

export const fetchData = async (endpoint) => {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include'
  });
  return response.json();
};
```

### Environment-Specific Settings

**Railway (Backend):**
- Set `NODE_ENV=production`
- Configure appropriate logging levels
- Enable security headers
- Set up monitoring and alerts

**GitHub Pages (Frontend):**
- Configure proper base URL in `package.json`:
  ```json
  {
    "homepage": "https://harrie19.github.io/UMAJA-core"
  }
  ```

---

## Verification Checklist

### Pre-Deployment Checklist

- [ ] All environment variables configured correctly
- [ ] Database connection tested
- [ ] CORS settings properly configured
- [ ] API endpoints updated with production URLs
- [ ] Security configurations reviewed
- [ ] SSL/HTTPS enabled for both frontend and backend

### Post-Deployment Backend Verification

1. **Health Check**
   ```bash
   curl https://umaja-core-production.up.railway.app/health
   ```
   Expected response: `{ "status": "ok", "timestamp": "..." }`

2. **API Endpoints**
   - [ ] Test GET endpoints
   - [ ] Test POST endpoints (with authentication)
   - [ ] Verify database connections
   - [ ] Check error handling

3. **Logs and Monitoring**
   - [ ] Check Railway logs for errors
   - [ ] Verify no critical warnings
   - [ ] Monitor initial traffic

### Post-Deployment Frontend Verification

1. **Site Accessibility**
   - [ ] Visit https://harrie19.github.io/UMAJA-core/
   - [ ] Verify homepage loads correctly
   - [ ] Check all navigation links
   - [ ] Test responsive design on mobile

2. **Functionality Testing**
   - [ ] Test API calls from frontend
   - [ ] Verify authentication flow
   - [ ] Check data fetching and display
   - [ ] Test form submissions
   - [ ] Verify error handling

3. **Performance**
   - [ ] Run Lighthouse audit (target 90+ performance score)
   - [ ] Check page load times
   - [ ] Verify asset optimization
   - [ ] Test caching behavior

4. **Browser Compatibility**
   - [ ] Chrome/Edge
   - [ ] Firefox
   - [ ] Safari
   - [ ] Mobile browsers

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: CORS Errors

**Symptom:**
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Solution:**
1. Verify CORS origin in Railway environment variables:
   ```
   CORS_ORIGIN=https://harrie19.github.io
   ```
2. Update backend CORS middleware to include your GitHub Pages domain
3. Ensure credentials are handled correctly
4. Redeploy backend after changes

#### Issue 2: 404 Errors on GitHub Pages

**Symptom:**
- Routes work on root but return 404 on refresh

**Solution:**
1. Add a `404.html` file that redirects to `index.html`:
   ```html
   <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>UMAJA Core</title>
       <script>
         sessionStorage.redirect = location.href;
       </script>
       <meta http-equiv="refresh" content="0;URL='/'">
     </head>
   </html>
   ```

2. Update your router to use HashRouter instead of BrowserRouter:
   ```javascript
   import { HashRouter } from 'react-router-dom';
   ```

#### Issue 3: Environment Variables Not Loading

**Symptom:**
- API calls fail with undefined URLs
- Configuration values are missing

**Solution:**
1. Verify `.env.production` exists and contains correct values
2. Ensure variables start with `REACT_APP_` prefix
3. Rebuild the frontend after adding environment variables
4. Check that build process includes environment variables

#### Issue 4: Railway Deployment Fails

**Symptom:**
- Build errors in Railway logs
- Deployment status shows "Failed"

**Solution:**
1. Check Railway logs for specific error messages
2. Verify `package.json` scripts are correct:
   ```json
   {
     "scripts": {
       "start": "node server.js",
       "build": "npm install"
     }
   }
   ```
3. Ensure all dependencies are in `package.json`
4. Verify Node.js version compatibility
5. Check Railway start command in Settings

#### Issue 5: Database Connection Issues

**Symptom:**
```
Error: connect ETIMEDOUT
```

**Solution:**
1. Verify DATABASE_URL environment variable
2. Check database service is running in Railway
3. Ensure backend and database are in the same Railway project
4. Test connection string locally
5. Check database firewall rules

#### Issue 6: Assets Not Loading (404 for CSS/JS)

**Symptom:**
- Page loads but styling is broken
- Console shows 404 errors for assets

**Solution:**
1. Verify `homepage` in `package.json` matches your GitHub Pages URL
2. Use relative paths for assets
3. Check build output paths
4. Ensure all assets are included in the build

#### Issue 7: API Calls Return 500 Errors

**Symptom:**
- Backend returns Internal Server Error

**Solution:**
1. Check Railway logs for detailed error messages
2. Verify all environment variables are set
3. Check database migrations are up to date
4. Review error handling in backend code
5. Test endpoints with tools like Postman

### Debug Mode

Enable detailed logging for troubleshooting:

**Backend (Railway):**
```env
DEBUG=true
LOG_LEVEL=debug
```

**Frontend (Local):**
```env
REACT_APP_DEBUG=true
```

### Getting Help

If issues persist:

1. **Check Railway Logs**: Settings → Deployments → Click on latest deployment
2. **GitHub Actions Logs**: Actions tab → Click on workflow run
3. **Browser Console**: F12 → Console tab for frontend errors
4. **Network Tab**: F12 → Network tab to inspect API calls

---

## Expected URLs and Endpoints

### Production URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | https://harrie19.github.io/UMAJA-core/ | Main application interface |
| Backend API | https://umaja-core-production.up.railway.app | API server |
| Backend Health | https://umaja-core-production.up.railway.app/health | Health check endpoint |

### API Endpoints

#### Public Endpoints

```
GET  /api/health              - Health check
GET  /api/v1/status           - API status
GET  /api/v1/info             - Application info
```

#### Authentication Endpoints

```
POST /api/v1/auth/register    - User registration
POST /api/v1/auth/login       - User login
POST /api/v1/auth/logout      - User logout
GET  /api/v1/auth/verify      - Verify token
```

#### Protected Endpoints (Require Authentication)

```
GET    /api/v1/users          - List users
GET    /api/v1/users/:id      - Get user details
PUT    /api/v1/users/:id      - Update user
DELETE /api/v1/users/:id      - Delete user

GET    /api/v1/data           - Fetch application data
POST   /api/v1/data           - Create new data entry
PUT    /api/v1/data/:id       - Update data entry
DELETE /api/v1/data/:id       - Delete data entry
```

### Testing Endpoints

You can test your deployed API using curl:

```bash
# Test health endpoint
curl https://umaja-core-production.up.railway.app/health

# Test API with authentication (example)
curl -X POST https://umaja-core-production.up.railway.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Test protected endpoint (with token)
curl https://umaja-core-production.up.railway.app/api/v1/users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Expected Response Formats

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

---

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [React Deployment Guide](https://create-react-app.dev/docs/deployment/)
- [CORS Troubleshooting](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

## Maintenance and Updates

### Updating the Application

**Backend Updates:**
1. Push changes to main branch
2. Railway will auto-deploy
3. Monitor logs for any issues
4. Run database migrations if needed

**Frontend Updates:**
1. Make changes to frontend code
2. Push to main branch
3. GitHub Actions will rebuild and deploy
4. Clear browser cache to see changes

### Rollback Procedure

**Railway:**
1. Go to Deployments tab
2. Find previous successful deployment
3. Click "Redeploy"

**GitHub Pages:**
1. Revert commit in GitHub
2. Wait for automatic redeployment
3. Or manually deploy previous version

---

## Security Considerations

- [ ] Use HTTPS for all communications
- [ ] Keep secrets in environment variables (never commit)
- [ ] Implement rate limiting on API endpoints
- [ ] Use secure JWT secrets (minimum 32 characters)
- [ ] Enable CORS only for trusted domains
- [ ] Regular security updates for dependencies
- [ ] Monitor Railway logs for suspicious activity
- [ ] Implement proper authentication and authorization
- [ ] Use prepared statements for database queries
- [ ] Sanitize user inputs

---

## Support

For issues specific to UMAJA Core:
- Open an issue on GitHub: https://github.com/harrie19/UMAJA-core/issues
- Check existing issues for solutions
- Provide detailed error messages and logs

---

**Last Updated:** 2026-01-03  
**Version:** 1.0.0  
**Maintained by:** harrie19
