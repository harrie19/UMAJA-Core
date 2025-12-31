# 🚀 GitHub Actions Deployment Setup

This repository includes automated deployment via GitHub Actions to Railway or Heroku.

## Quick Start

### Option 1: Manual Trigger (Recommended)

1. Go to **Actions** tab in GitHub
2. Select **Deploy UMAJA WORLDTOUR** workflow
3. Click **Run workflow**
4. Choose platform (Railway or Heroku)
5. Select environment (production or staging)
6. Click **Run workflow** button

### Option 2: Automatic Deployment

Deployment automatically triggers when you push changes to `main` branch in these directories:
- `src/**`
- `api/**`
- `requirements.txt`
- `Procfile`
- `railway.json`

## Setup Instructions

### For Railway Deployment

1. **Get Railway Token:**
   - Go to https://railway.app
   - Navigate to Account Settings → Tokens
   - Create a new token

2. **Add GitHub Secret:**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `RAILWAY_TOKEN`
   - Value: Your Railway token
   - Click "Add secret"

3. **Create Railway Project:**
   ```bash
   railway login
   railway init
   railway link
   ```

4. **Deploy:**
   - Use GitHub Actions (see Quick Start above)
   - Or push to main branch for auto-deploy

### For Heroku Deployment

1. **Get Heroku Credentials:**
   - Get your API key from https://dashboard.heroku.com/account
   - Note your Heroku email
   - Create a Heroku app: `heroku create umaja-worldtour`

2. **Add GitHub Secrets:**
   - `HEROKU_API_KEY`: Your Heroku API key
   - `HEROKU_EMAIL`: Your Heroku account email
   - `HEROKU_APP_NAME`: Your Heroku app name (e.g., umaja-worldtour)

3. **Deploy:**
   - Use GitHub Actions workflow
   - Select "heroku" as platform

## Environment Variables

Set these in your deployment platform (Railway/Heroku):

### Required
```bash
ENVIRONMENT=production
DEBUG=False
PORT=5000
```

### Optional (for full features)
```bash
# Voice Synthesis
ELEVENLABS_API_KEY=your_key
USE_OFFLINE_TTS=true

# Image Generation
USE_LOCAL_STABLE_DIFFUSION=false

# Worldtour
WORLDTOUR_MODE=true
SALES_ENABLED=true
```

## Monitoring Deployment

### Check Deployment Status
1. Go to **Actions** tab
2. Click on the running workflow
3. Watch the logs in real-time

### View Deployment Logs
- **Railway**: `railway logs`
- **Heroku**: `heroku logs --tail`

### Verify Deployment
After deployment, test the endpoints:

```bash
# Health check
curl https://your-app.railway.app/health

# Generate content
curl -X POST https://your-app.railway.app/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{"topic":"test","personality":"john_cleese","length":"short"}'
```

## Rollback

If deployment fails or you need to rollback:

### Railway
```bash
railway rollback
```

### Heroku
```bash
heroku rollback
```

### Via GitHub Actions
- Go to successful previous deployment
- Click "Re-run jobs"

## Troubleshooting

### Deployment fails with "Railway token invalid"
- Regenerate token in Railway dashboard
- Update `RAILWAY_TOKEN` secret in GitHub

### Deployment fails with "Heroku authentication failed"
- Verify `HEROKU_API_KEY` is correct
- Check `HEROKU_EMAIL` matches your account

### Tests fail before deployment
- Check the test logs in GitHub Actions
- Fix the failing tests and push again

### App doesn't start after deployment
- Check platform logs for errors
- Verify all required dependencies are in `requirements.txt`
- Ensure `Procfile` is correct

## Manual Deployment (Fallback)

If GitHub Actions deployment fails, use manual deployment:

### Railway
```bash
railway login
railway link
railway up
```

### Heroku
```bash
heroku login
git push heroku main
```

## Security Notes

- Never commit API keys or secrets
- Always use GitHub Secrets for sensitive data
- Review deployment logs for exposed credentials
- Enable branch protection on `main`

## Support

- Deployment issues: Check GitHub Actions logs
- Platform issues: Consult Railway/Heroku documentation
- Code issues: Review [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)
