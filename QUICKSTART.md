# 🚀 Quick Start Guide

Get Samarth running in 5 minutes!

## Step 1: Get Groq API Key (FREE)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (free, no credit card)
3. Go to "API Keys" → Create new key
4. Copy the API key

## Step 2: Set Up Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and paste your Groq API key
# GROQ_API_KEY=your_key_here
```

## Step 3: Run Backend

```bash
cd src
python app.py
```

You should see:
```
Initializing Samarth Q&A System...
Loaded crop data: 32 rows
Loaded rainfall data: 34 rows
System initialized successfully!
Running on http://0.0.0.0:5000
```

## Step 4: Open Frontend

Simply open `frontend/index.html` in your browser!

Or run a local server:
```bash
cd frontend
python -m http.server 8000
```

Then visit: `http://localhost:8000`

## Step 5: Try Example Queries

Click on the example buttons or try:
- "Which district has the highest crop production in Karnataka?"
- "Compare rainfall in Chennai vs Coimbatore"
- "Top 5 districts by rainfall"

## 🎉 That's it!

Your system is running locally!

## Next: Deploy for Public Link

Follow the deployment guide in README.md to:
1. Deploy backend to Render (free)
2. Deploy frontend to Vercel (free)
3. Get your public shareable link!

### Quick Deploy Commands

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin YOUR_GITHUB_URL
git push -u origin main

# Then follow deployment steps in README.md
```

---

**Need help?** Check README.md for detailed instructions!
