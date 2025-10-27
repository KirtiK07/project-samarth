# 🌐 Deployment Guide - Get Your Public Link!

This guide will help you deploy Samarth and get a public shareable link.

## Prerequisites

✅ GitHub account (free)
✅ Groq API key (free from [console.groq.com](https://console.groq.com))
✅ Render account (free)
✅ Vercel account (free)

---

## Part 1: Push Code to GitHub

### Step 1: Initialize Git Repository

```bash
# Navigate to project root
cd samarth

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Samarth Q&A System"
```

### Step 2: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `samarth` (or any name you prefer)
3. Make it **Public** (required for free tier)
4. **Don't** initialize with README (we already have one)
5. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/samarth.git

# Push code
git branch -M main
git push -u origin main
```

Your code is now on GitHub! ✅

---

## Part 2: Deploy Backend to Render

### Step 1: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub account

### Step 2: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect account" and authorize Render to access GitHub
4. Find and select your `samarth` repository

### Step 3: Configure Web Service

Fill in the following:

**Basic Settings:**
- **Name**: `samarth-backend` (or any name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `backend`

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --chdir src app:app`

**Advanced Settings:**

Click "Advanced" and add environment variables:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | Your Groq API key |
| `FLASK_ENV` | `production` |
| `PORT` | `5000` |

**Plan:**
- Select **Free** (up to 750 hours/month)

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait 2-5 minutes for deployment
3. You'll see logs - wait for "Running on http://0.0.0.0:5000"

### Step 5: Get Backend URL

Once deployed, you'll see your URL at the top:
```
https://samarth-backend-xxxx.onrender.com
```

**Copy this URL** - you'll need it for frontend! 📋

### Step 6: Test Backend

Open in browser:
```
https://your-backend-url.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "message": "Samarth API is running"
}
```

Backend deployed! ✅

---

## Part 3: Deploy Frontend to Vercel

### Step 1: Update Frontend with Backend URL

**Important:** Before deploying frontend, update the API URL!

Edit `frontend/script.js` (line 2-4):

```javascript
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://your-backend-url.onrender.com';  // ← Replace this!
```

Replace with your Render backend URL from Part 2, Step 5.

**Commit the change:**
```bash
git add frontend/script.js
git commit -m "Update backend URL for production"
git push
```

### Step 2: Sign Up for Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Start Deploying"
3. Sign up with GitHub account

### Step 3: Deploy Frontend

1. Click "Add New..." → "Project"
2. Import your `samarth` repository
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

4. Click "Deploy"
5. Wait 1-2 minutes

### Step 4: Get Your Public Link

Once deployed, Vercel shows your URL:
```
https://samarth-xxxx.vercel.app
```

**This is your public shareable link!** 🎉

### Step 5: Test Your Public Link

1. Open your Vercel URL in browser
2. Try example queries:
   - "Which district has highest crop production?"
   - "Compare rainfall in Chennai vs Coimbatore"

If queries work, you're done! ✅

---

## 🎉 You're Live!

Your Samarth Q&A system is now publicly accessible!

**Share these links:**
- 🌐 **Frontend**: `https://your-project.vercel.app`
- 🔧 **Backend API**: `https://your-backend.onrender.com`

---

## Troubleshooting

### Backend Issues

**Problem: "Application failed to respond"**
- Check Render logs for errors
- Verify GROQ_API_KEY is set correctly
- Make sure all files pushed to GitHub

**Problem: "GROQ_API_KEY not found"**
- Go to Render dashboard → your service → Environment
- Add the GROQ_API_KEY variable
- Click "Save Changes"
- Render will auto-redeploy

### Frontend Issues

**Problem: "Cannot connect to backend"**
- Verify backend URL in `script.js` is correct
- Make sure backend is deployed and running
- Check browser console for CORS errors

**Problem: Queries not working**
- Open browser developer console (F12)
- Check for errors
- Verify backend URL is accessible

### Free Tier Limitations

**Render Free Tier:**
- Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free

**Groq Free Tier:**
- 14,400 requests per day
- 50 requests per minute
- More than enough for demo!

**Vercel Free Tier:**
- 100 GB bandwidth/month
- Unlimited projects
- Perfect for frontend!

---

## Keeping Your Deployment Updated

When you make code changes:

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push

# Both Render and Vercel will auto-deploy!
```

---

## Custom Domain (Optional)

### Vercel:
1. Go to your project settings
2. Domains → Add custom domain
3. Follow Vercel's instructions

### Render:
1. Go to your service settings
2. Custom Domains → Add custom domain
3. Follow Render's instructions

---

## Monitoring Your App

### Render Dashboard
- View logs in real-time
- Check deployment status
- Monitor resource usage

### Vercel Dashboard
- View deployment history
- Check analytics
- Monitor performance

---

## Need Help?

1. Check logs in Render/Vercel dashboard
2. Review README.md for detailed docs
3. Test locally first with QUICKSTART.md
4. Check environment variables are set correctly

---

**Congratulations! Your AI-powered Q&A system is live! 🚀**

Share your link and showcase your project!

For Loom video:
1. Record your screen
2. Show the public link
3. Demonstrate 2-3 queries
4. Show the answers with citations
5. Upload to Loom and share the link!
