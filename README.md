# 🌾 Samarth - Intelligent Q&A System for Agricultural & Climate Data

An AI-powered system that answers natural language questions about agricultural and climate data from India's government data sources, specifically focusing on Karnataka's crop production and Tamil Nadu's rainfall data.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Llama 3](https://img.shields.io/badge/Llama_3-70B-orange)
![Groq](https://img.shields.io/badge/Groq-API-purple)

## 🎯 Features

- **Natural Language Processing**: Ask questions in plain English
- **Intelligent Query Analysis**: Powered by Llama 3 70B via Groq API
- **Multi-Source Data**: Crop production (Karnataka) and Rainfall (Tamil Nadu)
- **Comprehensive Analysis**: Comparisons, rankings, trends, and correlations
- **Source Citations**: Every answer includes data source references
- **Beautiful UI**: Modern, responsive web interface
- **Free to Deploy**: No cost for Groq API (free tier)

## 📊 Available Data

### Crop Production Data (Karnataka)
- **Districts**: 30 districts across Karnataka
- **Seasons**: Kharif, Rabi, Summer
- **Metrics**: Area (hectares), Yield (kg/hectare), Production (tonnes)
- **Source**: `data/crop_production.csv`

### Rainfall Data (Tamil Nadu)
- **Districts**: 32 districts across Tamil Nadu
- **Period**: June 2017 - May 2018
- **Seasons**: South West Monsoon, North East Monsoon, Winter, Hot Weather
- **Metrics**: Actual vs Normal rainfall (mm)
- **Source**: `data/rainfall_data.csv.csv`

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Groq API key (free - get it from [https://console.groq.com](https://console.groq.com))

### Local Setup

1. **Clone the repository**
   ```bash
   cd samarth
   ```

2. **Set up backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy example env file
   cp .env.example .env

   # Edit .env and add your Groq API key
   # GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Start the backend server**
   ```bash
   cd src
   python app.py
   ```
   Backend will run on `http://localhost:5000`

5. **Open the frontend**
   - Open `frontend/index.html` in your browser
   - Or use a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Frontend will be available at `http://localhost:8000`

## 📝 Example Queries

Try asking these questions:

### Comparison Queries
- "Compare rainfall in Chennai vs Coimbatore"
- "Compare crop production between Raichur and Belagavi districts"
- "Which district has more rainfall: Nagapattinam or Kanniyakumari?"

### Ranking Queries
- "Which district has the highest crop production in Karnataka?"
- "Top 5 districts by rainfall in Tamil Nadu"
- "Districts with lowest crop yield"
- "Rank districts by total crop area"

### Analysis Queries
- "What is the average rainfall across Tamil Nadu?"
- "Total crop production in Karnataka"
- "Which season contributes most to crop production?"
- "Seasonal rainfall patterns in Tamil Nadu"

### Specific Data Queries
- "Crop production data for Mysuru district"
- "Rainfall data for Salem district"
- "How much area is under cultivation in Ballari?"
- "What is the yield in Hassan district?"

## 🌐 Deployment Guide

### Deploy Backend to Render (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [https://render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` folder
   - Render will auto-detect settings from `render.yaml`
   - Add environment variable:
     - Key: `GROQ_API_KEY`
     - Value: Your Groq API key
   - Click "Create Web Service"

3. **Get your backend URL**
   - After deployment, copy your backend URL (e.g., `https://samarth-backend.onrender.com`)

### Deploy Frontend to Vercel

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Update frontend API URL**
   - Edit `frontend/script.js`
   - Replace `YOUR_BACKEND_URL_HERE` with your Render backend URL:
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost'
       ? 'http://localhost:5000'
       : 'https://your-backend-url.onrender.com';
   ```

3. **Deploy to Vercel**
   - Go to [https://vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Click "Deploy"

4. **Get your public link**
   - After deployment, Vercel will provide your public URL
   - Share this link with anyone!

### Alternative: Deploy to Railway

1. **Deploy Backend**
   - Go to [https://railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variable: `GROQ_API_KEY`
   - Railway will auto-deploy

2. **Get public URL**
   - Railway provides a public URL for your backend
   - Update frontend with this URL

## 🛠️ API Documentation

### Base URL
- Local: `http://localhost:5000`
- Production: Your deployed URL

### Endpoints

#### GET `/`
Welcome message and API information

#### GET `/health`
Health check endpoint

#### GET `/data-summary`
Get summary of available datasets

**Response:**
```json
{
  "success": true,
  "data": {
    "crop_data": {
      "rows": 32,
      "columns": [...],
      "districts": [...]
    },
    "rainfall_data": {
      "rows": 34,
      "columns": [...],
      "districts": [...]
    }
  }
}
```

#### POST `/query`
Submit a natural language query

**Request:**
```json
{
  "query": "Which district has the highest crop production?"
}
```

**Response:**
```json
{
  "success": true,
  "query": "Which district has the highest crop production?",
  "answer": "Based on the crop production data...",
  "raw_data": { ... },
  "sources": [ ... ]
}
```

#### GET `/example-queries`
Get example queries you can try

## 🏗️ Project Structure

```
samarth/
├── backend/
│   ├── src/
│   │   ├── app.py                  # Flask application
│   │   ├── data_loader.py          # CSV data loader
│   │   ├── query_analyzer.py       # NLP query analysis
│   │   ├── query_processor.py      # Data processing
│   │   └── answer_generator.py     # Answer generation
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example               # Environment variables template
│   ├── Procfile                   # Deployment config
│   ├── render.yaml                # Render config
│   └── runtime.txt                # Python version
├── frontend/
│   ├── index.html                 # Main HTML
│   ├── style.css                  # Styles
│   ├── script.js                  # Frontend logic
│   └── vercel.json                # Vercel config
├── data/
│   ├── crop_production.csv        # Karnataka crop data
│   └── rainfall_data.csv.csv      # Tamil Nadu rainfall data
└── README.md                       # This file
```

## 🧪 Testing Locally

1. **Start backend**
   ```bash
   cd backend/src
   python app.py
   ```

2. **Test API with curl**
   ```bash
   # Health check
   curl http://localhost:5000/health

   # Submit query
   curl -X POST http://localhost:5000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Which district has highest crop production?"}'
   ```

3. **Open frontend**
   - Open `frontend/index.html` in browser
   - Try example queries

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
FLASK_ENV=development
PORT=5000
```

### Get Groq API Key (FREE)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (free - no credit card required)
3. Go to "API Keys" section
4. Create new API key
5. Copy and add to `.env` file

## 📈 System Architecture

```
User Query → Frontend (HTML/JS)
              ↓
          Flask API Backend
              ↓
      1. Query Analyzer (Llama 3 via Groq)
         - Extracts intent, entities, metrics
              ↓
      2. Query Processor (Pandas)
         - Retrieves and analyzes data
              ↓
      3. Answer Generator (Llama 3 via Groq)
         - Generates natural language answer
              ↓
          Response with Citations
```

## 🎨 Key Technologies

- **Backend**: Python 3.11, Flask
- **Data Processing**: Pandas
- **AI/NLP**: Llama 3 70B via Groq API
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Deployment**: Render (backend), Vercel (frontend)

## 📚 Future Enhancements

- [ ] Add more states and datasets
- [ ] Multi-year trend analysis
- [ ] Correlation analysis between crop and rainfall
- [ ] Export data to PDF/Excel
- [ ] User authentication
- [ ] Query history
- [ ] Advanced visualizations (charts, maps)
- [ ] Mobile app
- [ ] Real-time data updates from data.gov.in API

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more datasets
- Improve query processing
- Enhance UI/UX
- Add visualizations
- Optimize performance

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- Data sources: India's data.gov.in portal
- AI Model: Llama 3 by Meta
- Inference API: Groq (free tier)

## 📧 Support

For issues or questions:
- Check existing issues in the repository
- Create a new issue with details
- Include error messages and logs

---

**Built with ❤️ for agricultural data analysis and climate insights**

### 🎉 Ready to Deploy!

Follow the deployment guide above to get your public link and share it with the world!

**Important**: After deployment, your public link will be:
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-backend.onrender.com`

Share the frontend URL for others to use the system!
