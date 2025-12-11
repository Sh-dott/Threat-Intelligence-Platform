# Threat Intelligence Platform

A professional, real-time threat intelligence news aggregation and analysis platform built with FastAPI and React.

![Platform Preview](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-18.3-blue)

## Features

### News Aggregation
- **Multi-source RSS feeds**: Aggregates from 10+ leading cybersecurity sources including:
  - BleepingComputer
  - KrebsOnSecurity
  - The Hacker News
  - Dark Reading
  - CISA Alerts
  - And more...
- **Automatic updates**: Fetches new articles every 10 minutes
- **Smart deduplication**: Removes duplicate articles across sources
- **Rich metadata**: Includes titles, summaries, images, and publish dates

### Intelligence Analysis
- **Threat type classification**: Rule-based classification into 10+ threat categories
  - Ransomware, Phishing, Data Breach, Malware, Vulnerability, DDoS, APT, Supply Chain, Crypto, IoT
- **Entity extraction**: Identifies and ranks mentioned companies, products, and technologies
- **Geographic analysis**: Tracks country/region mentions in threat reports
- **Trend analysis**: 24-hour and 7-day statistics for each threat type

### User Interface
- **Modern dark theme**: Optimized for security analysts
- **Real-time search**: Filter articles by keywords
- **Threat type filtering**: Quick access to specific threat categories
- **Visual analytics**: Interactive charts and statistics
- **Responsive design**: Works on desktop, tablet, and mobile

## Architecture

```
threat-intel-platform/
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── main.py       # API endpoints
│   │   ├── models.py     # Pydantic data models
│   │   ├── news_sources.py  # RSS feed aggregator
│   │   └── insights.py   # Intelligence analysis engine
│   └── requirements.txt
│
└── frontend/             # React application
    ├── src/
    │   ├── api/          # API client
    │   ├── components/   # React components
    │   ├── types/        # TypeScript types
    │   ├── App.tsx       # Main application
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Feedparser**: RSS/Atom feed parsing
- **BeautifulSoup4**: HTML content cleaning
- **Requests**: HTTP client for feed fetching
- **Pydantic**: Data validation and serialization

### Frontend
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **TailwindCSS**: Utility-first CSS framework
- **Recharts**: Charting library
- **Lucide React**: Icon library

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file (optional):
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## API Endpoints

### `GET /`
Health check and API information

### `GET /health`
Detailed health status

### `GET /api/news`
Get normalized news articles

Query parameters:
- `limit` (int, default: 100): Maximum number of articles
- `threat_type` (string): Filter by threat type
- `search` (string): Search in title and summary

### `GET /api/insights`
Get intelligence insights and trends

Returns statistics about:
- Threat type distribution
- Top mentioned entities
- Geographic mentions
- Trend analysis

### `POST /api/refresh`
Manually trigger a data refresh

## Building for Production

### Backend
The FastAPI application can be deployed using:
- **Uvicorn** with Gunicorn for production
- **Docker** container
- **Cloud platforms**: Render, Railway, AWS, etc.

Example production command:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
Build the optimized production bundle:
```bash
cd frontend
npm run build
```

The `dist/` directory contains static files ready for deployment to:
- **Netlify**
- **Vercel**
- **GitHub Pages**
- **AWS S3 + CloudFront**
- Any static hosting service

Configure the production API URL:
```env
VITE_API_URL=https://your-api-domain.com
```

## Deployment Guide

### Option 1: Render (Backend) + Netlify (Frontend)

**Backend on Render:**
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy

**Frontend on Netlify:**
1. Build your frontend: `npm run build`
2. Create a new site on Netlify
3. Upload the `dist/` folder
4. Add environment variable: `VITE_API_URL` with your Render backend URL
5. Deploy

### Option 2: Railway (Full Stack)

1. Create a new project on Railway
2. Add two services:
   - Backend: Python service running FastAPI
   - Frontend: Static site from `dist/` folder
3. Configure environment variables
4. Deploy both services

### Option 3: Docker Deployment

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t threat-intel-api .
docker run -p 8000:8000 threat-intel-api
```

## Customization

### Adding New RSS Feeds
Edit `backend/app/news_sources.py` and add to the `NEWS_SOURCES` list:
```python
{
    "name": "Your Source Name",
    "url": "https://example.com/feed.xml",
    "type": "rss"
}
```

### Adding Threat Types
Edit `backend/app/insights.py` and update `THREAT_KEYWORDS`:
```python
THREAT_KEYWORDS = {
    "your_threat_type": ["keyword1", "keyword2", "keyword3"],
    # ... existing types
}
```

### Customizing Fetch Interval
Edit `backend/app/main.py` and change `FETCH_INTERVAL`:
```python
FETCH_INTERVAL = 900  # 15 minutes in seconds
```

## Performance Considerations

- **In-memory caching**: Articles are cached in memory for fast access
- **Background updates**: News fetching runs in background without blocking requests
- **Rate limiting**: Respects RSS feed rate limits with reasonable intervals
- **Efficient parsing**: Uses streaming and iterative parsing for large feeds

## Security Notes

- All external article links open in new tabs with `noopener noreferrer`
- No sensitive data is stored or transmitted
- CORS is configured for specific origins (update in production)
- RSS feeds are fetched with appropriate user agents
- Input validation on all API endpoints

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Problem**: Feeds not loading
- Check internet connectivity
- Some feeds may have rate limits or be temporarily unavailable
- Check logs for specific error messages

### Frontend Issues

**Problem**: API connection refused
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify proxy configuration in `vite.config.ts`

**Problem**: Build fails
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

## License

MIT License - Feel free to use this project for your own threat intelligence needs!

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- All the amazing open-source cybersecurity news sources
- The FastAPI and React communities
- Security researchers and analysts who keep us informed

---

Built with ❤️ for the security community
