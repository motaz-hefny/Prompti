# Prompti - Quick Start Guide

## 🚀 Get Your App Live in 10 Minutes

### What You Have
✅ Fully functional prompt generator with AI enhancement
✅ Google Gemini API key already configured
✅ Production-ready code with no errors
✅ Complete documentation

---

## Option 1: Deploy to Vercel (Easiest - Recommended)

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Sign up with GitHub (recommended) or email

### Step 2: Import Your Project
1. Click "Add New Project"
2. Import your Git repository
   - If not on Git yet, push your code to GitHub first
3. Vercel will auto-detect it's a Vite project

### Step 3: Configure Environment Variable
1. In the deployment settings, find "Environment Variables"
2. Add:
   - **Name**: `VITE_GEMINI_API_KEY`
   - **Value**: `AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE`
3. Click "Add"

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for build to complete
3. Your app is live! 🎉

**Your URL**: `https://your-project-name.vercel.app`

---

## Option 2: Deploy to Netlify

### Step 1: Create Netlify Account
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub or email

### Step 2: Deploy
1. Click "Add new site" → "Import an existing project"
2. Connect your Git repository
3. Build settings (auto-detected):
   - Build command: `npm run build`
   - Publish directory: `dist`
4. Add environment variable:
   - **Key**: `VITE_GEMINI_API_KEY`
   - **Value**: `AIzaSyDZBbO8P4MEZ5lUhade1G8JJVJL_GKdDKE`
5. Click "Deploy site"

**Your URL**: `https://your-site-name.netlify.app`

---

## Option 3: Test Locally First

### Run Development Server
```bash
cd /workspace/app-855yksanby0x
npm run dev
```

Open browser to `http://localhost:5173`

### Test Features:
1. ✅ Switch languages (English, Arabic, Egyptian)
2. ✅ Select different frameworks
3. ✅ Fill in form fields
4. ✅ Click "Generate Prompt" (instant)
5. ✅ Click "✨ Generate with AI" (uses your API key)
6. ✅ Compare both outputs
7. ✅ Copy to clipboard
8. ✅ Download as .txt file

---

## 🎯 What to Test After Deployment

### Basic Functionality:
- [ ] Page loads without errors
- [ ] Language switching works
- [ ] Framework selection works
- [ ] Form inputs work
- [ ] Live preview updates

### AI Features:
- [ ] Manual generation works
- [ ] AI generation works (check API key)
- [ ] Loading spinner shows during AI generation
- [ ] Both prompts display correctly

### Export:
- [ ] Copy to clipboard works
- [ ] Download creates .txt file
- [ ] Filenames are correct

### Responsive:
- [ ] Desktop layout looks good
- [ ] Mobile layout works
- [ ] RTL works for Arabic

---

## 🔧 Troubleshooting

### "AI generation failed"
- Check that environment variable is set correctly
- Verify API key at [Google AI Studio](https://makersuite.google.com/)
- Check browser console for detailed error

### Build fails on deployment
- Ensure Node.js version is 18+
- Check that all dependencies are in package.json
- Review build logs for specific errors

### Environment variable not working
- Make sure it starts with `VITE_`
- Redeploy after adding the variable
- Check platform-specific documentation

---

## 📱 Share Your App

Once deployed, share your URL:
- `https://your-project.vercel.app`
- `https://your-site.netlify.app`

### Add Custom Domain (Optional):
1. Go to project settings
2. Add custom domain
3. Update DNS records
4. Wait for SSL certificate (automatic)

---

## 🎉 You're Done!

Your Prompti app is now live and ready to use!

### What You Can Do Now:
1. ✅ Generate structured prompts
2. ✅ Use AI to enhance prompts
3. ✅ Switch between 3 languages
4. ✅ Export and share prompts
5. ✅ Access from any device

### Next Steps:
- Share with friends and colleagues
- Get feedback
- Monitor API usage at Google AI Studio
- Consider adding custom domain
- Explore future enhancements

---

## 📚 Need More Help?

- **Full Documentation**: See `PROMPTI_README.md`
- **Deployment Options**: See `DEPLOYMENT_GUIDE.md`
- **AI Setup**: See `AI_SETUP_GUIDE.md`
- **Google Sign-In**: See `GOOGLE_SIGNIN_INFO.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`

---

**Estimated Time**: 10 minutes
**Difficulty**: Easy
**Cost**: Free

🚀 **Happy Prompting!**
