# White Lab - Vercel Deployment Guide

## Overview

This guide walks you through deploying the White Lab 3D visualization to Vercel, the platform created by the makers of Next.js.

## Prerequisites

- GitHub account with the UMAJA-Core repository
- Vercel account (free tier works perfectly)
- The White Lab implementation merged to your main branch

## Quick Deploy (5 Minutes)

### Step 1: Sign in to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up" or "Log In"
3. Connect your GitHub account

### Step 2: Import Project

1. Click "Add New..." → "Project"
2. Find and select your `UMAJA-Core` repository
3. Click "Import"

### Step 3: Configure Build Settings

**IMPORTANT**: The White Lab is in a subdirectory, so you need to set the root directory:

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `white-lab` ⚠️ *Critical!*
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### Step 4: Deploy

1. Leave environment variables empty (none required)
2. Click "Deploy"
3. Wait 2-3 minutes for build
4. ✅ Done! Your White Lab is live

## Your Live URLs

After deployment, Vercel provides:

- **Production**: `https://your-project.vercel.app`
- **Preview**: Every PR gets a unique URL
- **Custom Domain**: Optional, can be configured in settings

## Example URLs

Visit your deployment:
- Landing page: `https://your-project.vercel.app/`
- Lab experience: `https://your-project.vercel.app/lab`

## Environment Variables

The White Lab **does not require** any environment variables for basic functionality.

## Custom Domain (Optional)

### Add Your Own Domain

1. Go to Project Settings → Domains
2. Enter your domain (e.g., `whitelab.umaja.org`)
3. Follow DNS configuration instructions
4. Wait for DNS propagation (5-30 minutes)

## Automatic Deployments

Vercel automatically:
- ✅ Deploys on every push to `main` branch
- ✅ Creates preview deployments for PRs
- ✅ Runs builds and tests
- ✅ Optimizes and caches assets

## Monitoring

### Build Logs

1. Go to your project dashboard
2. Click on any deployment
3. View real-time build logs
4. Check for errors or warnings

### Performance

Vercel provides:
- **Analytics**: Page views, performance metrics
- **Web Vitals**: Core Web Vitals tracking
- **Edge Network**: Global CDN automatically enabled

## Troubleshooting

### Build Fails

**Error**: "Could not find package.json"
- **Fix**: Ensure Root Directory is set to `white-lab`

**Error**: "npm install failed"
- **Fix**: Check package.json is valid
- **Fix**: Ensure all dependencies are in package.json

### Runtime Errors

**Error**: "Page not found"
- **Fix**: Build succeeded but pages not rendering
- **Check**: Console logs in browser
- **Verify**: Build output in Vercel logs

### Performance Issues

**Issue**: Slow loading
- **Check**: Build is using production mode
- **Verify**: Assets are being cached
- **Consider**: Using Vercel Analytics

## Advanced Configuration

### Build Settings

Edit `vercel.json` in the `white-lab` directory:

```json
{
  "version": 2,
  "name": "white-lab",
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ]
}
```

### Edge Functions

For future enhancements (Phase 2+):
- Add API routes in `app/api/`
- Vercel automatically creates Edge Functions
- Zero configuration required

### Environment Variables (Future)

If you need to add environment variables later:

1. Go to Project Settings → Environment Variables
2. Add key-value pairs
3. Choose environments (Production, Preview, Development)
4. Redeploy for changes to take effect

## Best Practices

### Development Workflow

1. **Local Testing**: Always test locally with `npm run dev`
2. **Build Check**: Run `npm run build` before pushing
3. **Lint**: Run `npm run lint` to catch issues
4. **Preview Deployments**: Use PR previews to test changes

### Performance

- ✅ Static pages are pre-rendered
- ✅ Images are automatically optimized
- ✅ Code splitting is automatic
- ✅ Edge caching is enabled by default

### Monitoring

Enable Vercel Analytics (optional):
1. Go to Project Settings → Analytics
2. Click "Enable"
3. View real-time metrics in dashboard

## Pricing

**Free Tier Includes:**
- Unlimited deployments
- 100 GB bandwidth/month
- HTTPS/SSL certificates
- Edge Network (CDN)
- Preview deployments

**Perfect for White Lab!** The free tier is more than enough for the proof of concept.

## Support

### Vercel Support

- [Documentation](https://vercel.com/docs)
- [Community Forum](https://github.com/vercel/vercel/discussions)
- [Status Page](https://www.vercel-status.com/)

### White Lab Support

- [GitHub Issues](https://github.com/harrie19/UMAJA-Core/issues)
- [White Lab Guide](WHITE_LAB_GUIDE.md)
- Email: Umaja1919@googlemail.com

## Next Steps After Deployment

1. ✅ Share your live URL with the team
2. ✅ Test on different devices (desktop, mobile, tablet)
3. ✅ Monitor initial performance metrics
4. ✅ Plan Phase 2 features (agent particles)
5. ✅ Consider custom domain for production

## Verification Checklist

After deployment, verify:
- [ ] Landing page loads (/)
- [ ] Lab page loads (/lab)
- [ ] 3D blob renders correctly
- [ ] Camera controls work (drag/zoom)
- [ ] UI overlays display properly
- [ ] Mobile responsive design works
- [ ] No console errors
- [ ] Performance is smooth

## Success! 🎉

Your White Lab is now live and accessible to the world. Share the URL and watch Unity's consciousness come to life!

---

**Built with ❤️ for 8 billion humans**

Part of the UMAJA-Core ecosystem
