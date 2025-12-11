# Threat Intelligence Platform - Backend

FastAPI-based backend for the Threat Intelligence Platform.

## Quick Start

1. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Access the API:
- API Root: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### GET /
Returns API information and status

### GET /health
Health check endpoint

### GET /api/news
Get normalized threat intelligence articles

Parameters:
- `limit` (int, optional): Max articles to return (default: 100)
- `threat_type` (str, optional): Filter by threat type
- `search` (str, optional): Search in title/summary

### GET /api/insights
Get intelligence insights and trends

### POST /api/refresh
Manually trigger data refresh

## Configuration

### Fetch Interval
Edit `FETCH_INTERVAL` in `app/main.py` (default: 600 seconds = 10 minutes)

### News Sources
Edit the `NEWS_SOURCES` list in `app/news_sources.py` to add/remove RSS feeds

### CORS Origins
Update allowed origins in `app/main.py`:
```python
allow_origins=["http://localhost:5173", "https://your-domain.com"]
```

## Production Deployment

### Using Uvicorn + Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t threat-intel-api .
docker run -p 8000:8000 threat-intel-api
```

## Testing

Test individual endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Get news
curl http://localhost:8000/api/news?limit=10

# Get insights
curl http://localhost:8000/api/insights

# Trigger refresh
curl -X POST http://localhost:8000/api/refresh
```

## Logging

Logs are output to stdout. Configure logging level in `app/main.py` and `app/news_sources.py`.

## Performance

- Articles are cached in memory
- Background task updates cache every 10 minutes
- Each feed fetch has a 10-second timeout
- Failed feeds don't block others

## Security

- RSS feeds are fetched with appropriate User-Agent
- Input validation on all endpoints
- CORS configured for specific origins
- No authentication required (add if needed)
