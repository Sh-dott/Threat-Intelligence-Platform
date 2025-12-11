# Quick Start Guide

Get the Threat Intelligence Platform running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Terminal/Command Prompt

## Step 1: Start the Backend

### Windows
```cmd
start-backend.bat
```

### macOS/Linux
```bash
chmod +x start-backend.sh
./start-backend.sh
```

### Manual (all platforms)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend is ready when you see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:** Open http://localhost:8000/docs

## Step 2: Start the Frontend

**Open a NEW terminal window**

### Windows
```cmd
start-frontend.bat
```

### macOS/Linux
```bash
chmod +x start-frontend.sh
./start-frontend.sh
```

### Manual (all platforms)
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend is ready when you see:
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

## Step 3: Use the Platform

Open your browser to: **http://localhost:5173**

You should see:
- Latest threat intelligence articles
- Search and filter functionality
- Live insights dashboard with charts

## What's Next?

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- ⚙️ Customize RSS feeds in `backend/app/news_sources.py`
- 🎨 Modify the UI in `frontend/src/`

## Common Issues

**Backend Error: "python: command not found"**
- Try `python3` or `py` instead

**Backend Error: "Address already in use"**
- Port 8000 is taken. Stop other services or change the port

**Frontend Error: "Cannot GET /api/news"**
- Make sure the backend is running on port 8000
- Check the Vite proxy configuration in `vite.config.ts`

**No articles showing:**
- Wait a moment for the initial fetch to complete
- Check the backend terminal for any errors
- Some RSS feeds may be temporarily unavailable

## Stopping the Servers

Press **Ctrl+C** in each terminal window to stop the servers.

---

**Enjoy your Threat Intelligence Platform!** 🛡️
