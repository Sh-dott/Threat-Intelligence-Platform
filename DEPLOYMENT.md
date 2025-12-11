# Deployment Guide

This guide provides detailed instructions for deploying the Threat Intelligence Platform to production.

## Table of Contents
1. [Local Development](#local-development)
2. [Production Build](#production-build)
3. [Deployment Options](#deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Local Development

### Quick Start (Windows)

1. **Start Backend:**
   ```cmd
   start-backend.bat
   ```
   - Creates virtual environment if needed
   - Installs dependencies
   - Starts FastAPI on http://localhost:8000

2. **Start Frontend** (in a new terminal):
   ```cmd
   start-frontend.bat
   ```
   - Installs dependencies if needed
   - Starts Vite dev server on http://localhost:5173

### Quick Start (macOS/Linux)

1. **Make scripts executable:**
   ```bash
   chmod +x start-backend.sh start-frontend.sh
   ```

2. **Start Backend:**
   ```bash
   ./start-backend.sh
   ```

3. **Start Frontend** (in a new terminal):
   ```bash
   ./start-frontend.sh
   ```

### Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Production Build

### Backend Production Setup

1. **Install production server:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn app.main:app \
     -w 4 \
     -k uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:8000 \
     --access-logfile - \
     --error-logfile -
   ```

   **Options explained:**
   - `-w 4`: 4 worker processes (adjust based on CPU cores)
   - `-k uvicorn.workers.UvicornWorker`: Use Uvicorn worker class
   - `--bind 0.0.0.0:8000`: Listen on all interfaces, port 8000
   - `--access-logfile -`: Log access to stdout
   - `--error-logfile -`: Log errors to stdout

### Frontend Production Build

1. **Build for production:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Output:**
   - Production-ready files in `dist/` directory
   - Optimized, minified, and tree-shaken
   - Ready for static hosting

3. **Preview build locally:**
   ```bash
   npm run preview
   ```

---

## Deployment Options

### Option 1: Render (Backend) + Netlify (Frontend) ⭐ RECOMMENDED

**Backend on Render:**

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `threat-intel-api`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables (optional):
   - `PYTHON_VERSION`: `3.11.0`
6. Click "Create Web Service"
7. Copy your service URL (e.g., `https://threat-intel-api.onrender.com`)

**Frontend on Netlify:**

1. Build your frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Create account at https://netlify.com
3. Click "Add new site" → "Deploy manually"
4. Drag and drop the `frontend/dist` folder
5. After deployment, configure:
   - Go to "Site settings" → "Environment variables"
   - Add `VITE_API_URL` with your Render backend URL
6. Rebuild:
   ```bash
   npm run build
   ```
   Then re-upload the `dist/` folder

**Alternative: Netlify with Git:**
1. Push to GitHub
2. "Add new site" → "Import from Git"
3. Select repository
4. Configure:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
5. Add environment variable: `VITE_API_URL`

---

### Option 2: Railway (Full Stack)

Railway provides an excellent all-in-one solution.

**Setup:**

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository

**Backend Service:**
1. Click "Add Service" → "GitHub Repo"
2. Configure:
   - **Root Directory:** `/backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add custom domain or use Railway-provided URL

**Frontend Service:**
1. Click "Add Service" → "GitHub Repo"
2. Configure:
   - **Root Directory:** `/frontend`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm run preview` or use a static server
3. Add environment variable:
   - `VITE_API_URL`: Your backend Railway URL

**Bonus:** Railway auto-deploys on git push!

---

### Option 3: Vercel (Frontend) + Any Backend Host

**Frontend on Vercel:**

1. Push to GitHub
2. Go to https://vercel.com
3. Click "Add New..." → "Project"
4. Import your repository
5. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
6. Add environment variable:
   - `VITE_API_URL`: Your backend URL
7. Deploy

**Backend Options:**
- Render (see Option 1)
- Railway (see Option 2)
- DigitalOcean App Platform
- AWS Elastic Beanstalk
- Heroku

---

### Option 4: Docker Deployment

**Create Dockerfiles:**

`backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

`frontend/nginx.conf`:
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**Run:**
```bash
docker-compose up -d
```

**Deploy to:**
- AWS ECS
- Google Cloud Run
- DigitalOcean Container Registry
- Any Docker host

---

### Option 5: AWS (S3 + CloudFront + Lambda)

**Frontend on S3 + CloudFront:**

1. Build frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Create S3 bucket:
   ```bash
   aws s3 mb s3://threat-intel-frontend
   ```

3. Upload files:
   ```bash
   aws s3 sync dist/ s3://threat-intel-frontend --acl public-read
   ```

4. Configure S3 for static hosting
5. Create CloudFront distribution
6. Point custom domain

**Backend on Lambda + API Gateway:**
- Use Mangum to wrap FastAPI for Lambda
- Or use AWS Elastic Beanstalk for easier deployment

---

## Environment Configuration

### Backend Environment Variables

Create `backend/.env` (for local development):
```env
# Optional: Configure fetch interval (seconds)
FETCH_INTERVAL=600

# Optional: Configure CORS origins
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Frontend Environment Variables

Create `frontend/.env.production`:
```env
VITE_API_URL=https://your-api-domain.com
```

Different environments:
- `.env` - All environments
- `.env.local` - Local overrides (not committed)
- `.env.production` - Production builds
- `.env.development` - Development builds

---

## Monitoring and Maintenance

### Backend Monitoring

**Health Check Endpoint:**
```bash
curl https://your-api.com/health
```

**Logs:**
- Render: Dashboard → "Logs"
- Railway: Service → "Deployments" → "View Logs"
- Docker: `docker logs <container-id>`

**Performance:**
- Monitor response times
- Check memory usage
- Watch for failed RSS feed fetches

### Frontend Monitoring

**Netlify:**
- Dashboard shows deploy status
- Analytics available

**Vercel:**
- Built-in analytics
- Performance insights

### Maintenance Tasks

**Update Dependencies:**

Backend:
```bash
pip list --outdated
pip install --upgrade package-name
```

Frontend:
```bash
npm outdated
npm update
```

**Monitor RSS Feeds:**
- Some feeds may become unavailable
- Update feed URLs in `backend/app/news_sources.py`
- Add new sources as needed

**Data Refresh:**
- Backend auto-refreshes every 10 minutes
- Manual refresh via `/api/refresh` endpoint:
  ```bash
  curl -X POST https://your-api.com/api/refresh
  ```

---

## Security Checklist

- [ ] Update CORS origins for production
- [ ] Use HTTPS for both frontend and backend
- [ ] Set appropriate rate limits
- [ ] Monitor for API abuse
- [ ] Keep dependencies updated
- [ ] Review logs regularly
- [ ] Set up error tracking (Sentry, etc.)

---

## Troubleshooting

**Backend won't start:**
- Check Python version (3.8+)
- Verify all dependencies installed
- Check port 8000 is available
- Review error logs

**Frontend can't connect to backend:**
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in backend
- Ensure backend is running and accessible
- Check browser console for errors

**No articles loading:**
- Check internet connectivity
- Some RSS feeds may be down temporarily
- Review backend logs for feed errors
- Trigger manual refresh

---

## Performance Optimization

**Backend:**
- Increase worker processes for high traffic
- Consider adding Redis for caching
- Implement rate limiting
- Add database for persistent storage

**Frontend:**
- Images are lazy-loaded by default
- Consider adding CDN for static assets
- Enable compression (Gzip/Brotli)
- Add service worker for offline support

---

## Scaling Considerations

**When traffic grows:**

1. **Backend:**
   - Add more worker processes
   - Use Redis for shared cache
   - Implement database (PostgreSQL)
   - Add load balancer

2. **Frontend:**
   - Use CDN (Cloudflare, AWS CloudFront)
   - Enable caching headers
   - Optimize images

3. **Monitoring:**
   - Set up uptime monitoring (UptimeRobot, Pingdom)
   - Add APM (New Relic, DataDog)
   - Configure alerts

---

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review backend logs
- Check browser console for frontend errors
- File an issue on GitHub

---

**Congratulations!** Your Threat Intelligence Platform is ready for production! 🚀
