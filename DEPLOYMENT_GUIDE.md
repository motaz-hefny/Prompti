# Prompti Deployment Guide

This guide covers how to deploy your Prompti application to various hosting platforms.

## Important Notes

### Google Sign-In Status
⚠️ **The Google Sign-In button is currently a MOCK/PLACEHOLDER**
- It's a visual element only - clicking it does nothing
- No actual Google OAuth authentication is implemented
- This is intentional as per the original requirements
- To implement real Google Sign-In, you would need to:
  1. Set up Google OAuth 2.0 credentials in Google Cloud Console
  2. Install a library like `@react-oauth/google`
  3. Implement authentication flow and user session management
  4. Add backend support for token verification

### Current Authentication
- The app works without any authentication
- All data is stored locally in browser sessionStorage
- No user accounts or cloud storage
- Perfect for personal use and testing

---

## Deployment Options

### Option 1: Vercel (Recommended - Easiest)

Vercel is the easiest way to deploy React applications with automatic builds and HTTPS.

#### Steps:

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Vercel Website**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your Git repository (GitHub, GitLab, or Bitbucket)
   - Vercel will auto-detect it's a Vite project
   - Add environment variable:
     - Key: `VITE_GEMINI_API_KEY`
     - Value: `AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE`
   - Click "Deploy"

3. **Deploy via CLI** (alternative):
   ```bash
   cd /workspace/app-855yksanby0x
   vercel
   ```
   - Follow the prompts
   - Add environment variables when asked

4. **Configure Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add: `VITE_GEMINI_API_KEY` = `AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE`
   - Redeploy if needed

**Pros:**
- Free tier available
- Automatic HTTPS
- Global CDN
- Automatic deployments from Git
- Easy environment variable management

**Your app will be live at**: `https://your-project-name.vercel.app`

---

### Option 2: Netlify

Another excellent option for static sites and React apps.

#### Steps:

1. **Deploy via Netlify Website**:
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your Git repository
   - Build settings:
     - Build command: `npm run build`
     - Publish directory: `dist`
   - Add environment variable:
     - Key: `VITE_GEMINI_API_KEY`
     - Value: `AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE`
   - Click "Deploy"

2. **Deploy via Netlify CLI** (alternative):
   ```bash
   npm install -g netlify-cli
   cd /workspace/app-855yksanby0x
   npm run build
   netlify deploy --prod
   ```

**Pros:**
- Free tier available
- Automatic HTTPS
- Form handling (if needed later)
- Serverless functions support

**Your app will be live at**: `https://your-site-name.netlify.app`

---

### Option 3: GitHub Pages

Free hosting directly from your GitHub repository.

#### Steps:

1. **Install gh-pages**:
   ```bash
   npm install --save-dev gh-pages
   ```

2. **Update package.json**:
   Add these scripts:
   ```json
   {
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d dist"
     },
     "homepage": "https://yourusername.github.io/prompti"
   }
   ```

3. **Update vite.config.ts**:
   Add base path:
   ```typescript
   export default defineConfig({
     base: '/prompti/',
     // ... rest of config
   })
   ```

4. **Deploy**:
   ```bash
   npm run deploy
   ```

5. **Configure GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from branch `gh-pages`
   - Save

**Note**: Environment variables need to be built into the app or use a different approach for GitHub Pages.

**Your app will be live at**: `https://yourusername.github.io/prompti`

---

### Option 4: Cloudflare Pages

Fast, global deployment with excellent performance.

#### Steps:

1. **Deploy via Cloudflare Dashboard**:
   - Go to [pages.cloudflare.com](https://pages.cloudflare.com)
   - Click "Create a project"
   - Connect your Git repository
   - Build settings:
     - Build command: `npm run build`
     - Build output directory: `dist`
   - Add environment variable:
     - Variable name: `VITE_GEMINI_API_KEY`
     - Value: `AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE`
   - Click "Save and Deploy"

**Pros:**
- Free tier available
- Excellent performance
- Global CDN
- DDoS protection

**Your app will be live at**: `https://prompti.pages.dev`

---

### Option 5: Self-Hosted (VPS/Server)

For complete control, deploy to your own server.

#### Requirements:
- A server (DigitalOcean, AWS, Linode, etc.)
- Node.js installed
- Nginx or Apache web server

#### Steps:

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Upload the `dist` folder** to your server:
   ```bash
   scp -r dist/* user@your-server:/var/www/prompti
   ```

3. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /var/www/prompti;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

4. **Set up HTTPS** with Let's Encrypt:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

---

## Environment Variables for Production

### Important: Securing Your API Key

⚠️ **Security Warning**: Your Gemini API key is exposed in the client-side code. This is acceptable for:
- Personal projects
- Internal tools
- Low-traffic applications

For production applications with many users, consider:
1. Setting up API key restrictions in Google Cloud Console
2. Limiting requests per day
3. Monitoring usage
4. Using a backend proxy to hide the key

### Setting Environment Variables

Different platforms handle environment variables differently:

**Vercel/Netlify/Cloudflare**:
- Add via dashboard: `VITE_GEMINI_API_KEY`
- Variables are injected at build time

**GitHub Pages**:
- Use GitHub Secrets for Actions
- Build with secrets in CI/CD pipeline

**Self-Hosted**:
- Create `.env` file on server
- Ensure it's not publicly accessible

---

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] API key is configured in environment variables
- [ ] Application builds successfully: `npm run build`
- [ ] No console errors in production build
- [ ] All features tested locally
- [ ] Environment variables are set correctly
- [ ] `.env` file is in `.gitignore` (already done)
- [ ] Custom domain configured (optional)
- [ ] HTTPS is enabled (automatic on most platforms)

---

## Post-Deployment Testing

After deployment, test:

1. **Basic Functionality**:
   - [ ] Page loads correctly
   - [ ] Language switching works
   - [ ] Framework selection works
   - [ ] Form inputs work

2. **AI Features**:
   - [ ] Manual prompt generation works
   - [ ] AI prompt generation works
   - [ ] Loading states display correctly
   - [ ] Error messages show properly

3. **Export Features**:
   - [ ] Copy to clipboard works
   - [ ] Download works
   - [ ] Filenames are correct

4. **Multilingual**:
   - [ ] English UI works
   - [ ] Arabic UI works with RTL
   - [ ] Egyptian Arabic works

5. **Responsive Design**:
   - [ ] Desktop layout works
   - [ ] Mobile layout works
   - [ ] Tablet layout works

---

## Custom Domain Setup

### Vercel:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Netlify:
1. Go to Site Settings → Domain Management
2. Add custom domain
3. Configure DNS

### Cloudflare Pages:
1. Go to Custom Domains
2. Add your domain
3. DNS is automatically configured if using Cloudflare DNS

---

## Monitoring and Analytics

Consider adding:

1. **Google Analytics**: Track usage and user behavior
2. **Sentry**: Error tracking and monitoring
3. **Vercel Analytics**: Built-in analytics (if using Vercel)

---

## Updating Your Deployment

### Automatic Deployments (Recommended):
- Connect your Git repository
- Push changes to main branch
- Platform automatically rebuilds and deploys

### Manual Deployments:
```bash
npm run build
# Then upload dist folder or use CLI
```

---

## Troubleshooting

### Build Fails:
- Check Node.js version (should be 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check for TypeScript errors: `npm run lint`

### Environment Variables Not Working:
- Ensure they start with `VITE_`
- Rebuild after adding variables
- Check platform-specific documentation

### AI Generation Not Working:
- Verify API key is set correctly
- Check browser console for errors
- Test API key at Google AI Studio
- Check API quota and rate limits

### 404 Errors on Refresh:
- Configure platform for SPA routing
- Vercel/Netlify handle this automatically
- For others, ensure server redirects to index.html

---

## Cost Considerations

### Free Tiers:

**Vercel**:
- 100 GB bandwidth/month
- Unlimited personal projects
- Automatic HTTPS

**Netlify**:
- 100 GB bandwidth/month
- 300 build minutes/month
- Automatic HTTPS

**Cloudflare Pages**:
- Unlimited bandwidth
- 500 builds/month
- Automatic HTTPS

**GitHub Pages**:
- 100 GB bandwidth/month
- 100 GB storage
- Free for public repositories

**Google Gemini API**:
- 60 requests/minute (free tier)
- 1,500 requests/day (free tier)
- Monitor usage at [Google AI Studio](https://makersuite.google.com/)

---

## Recommended Deployment Path

For your Prompti app, I recommend:

1. **Start with Vercel** (easiest, best DX)
2. Connect your GitHub repository
3. Add environment variable for Gemini API key
4. Deploy with one click
5. Get a free `.vercel.app` domain
6. Add custom domain later if needed

**Total time**: 5-10 minutes
**Cost**: Free

---

## Support and Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Netlify Documentation](https://docs.netlify.com)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Google Gemini API Docs](https://ai.google.dev/docs)

---

## Next Steps

1. Choose a deployment platform
2. Create an account
3. Connect your repository
4. Add environment variables
5. Deploy!
6. Share your app URL

Your Prompti app is ready to go live! 🚀
