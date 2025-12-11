# Project Structure

Complete overview of the Threat Intelligence Platform codebase.

```
threat-intel-platform/
│
├── 📁 backend/                    # FastAPI Backend Application
│   ├── 📁 app/
│   │   ├── __init__.py           # Package initializer
│   │   ├── main.py               # FastAPI app, endpoints, startup logic
│   │   ├── models.py             # Pydantic data models
│   │   ├── news_sources.py       # RSS feed aggregation logic
│   │   └── insights.py           # Threat analysis & classification
│   │
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend-specific documentation
│
├── 📁 frontend/                   # React Frontend Application
│   ├── 📁 public/                # Static assets (auto-generated)
│   │
│   ├── 📁 src/
│   │   ├── 📁 api/
│   │   │   └── client.ts         # API client functions
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── ArticleCard.tsx   # Individual article card component
│   │   │   └── InsightsDashboard.tsx  # Analytics dashboard
│   │   │
│   │   ├── 📁 types/
│   │   │   └── index.ts          # TypeScript type definitions
│   │   │
│   │   ├── App.tsx               # Main application component
│   │   ├── main.tsx              # React entry point
│   │   └── index.css             # Global styles with Tailwind
│   │
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies & scripts
│   ├── tsconfig.json             # TypeScript configuration
│   ├── vite.config.ts            # Vite build configuration
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   ├── postcss.config.js         # PostCSS configuration
│   └── .env.example              # Environment variables template
│
├── 📄 README.md                  # Main project documentation
├── 📄 QUICK_START.md             # Fast setup guide
├── 📄 DEPLOYMENT.md              # Production deployment guide
├── 📄 PROJECT_STRUCTURE.md       # This file
├── 📄 .gitignore                 # Git ignore rules
│
├── 🚀 start-backend.bat          # Windows backend launcher
├── 🚀 start-backend.sh           # Unix backend launcher
├── 🚀 start-frontend.bat         # Windows frontend launcher
└── 🚀 start-frontend.sh          # Unix frontend launcher
```

## File Descriptions

### Backend Files

**`backend/app/main.py`** (200 lines)
- FastAPI application setup
- API endpoints: `/`, `/health`, `/api/news`, `/api/insights`, `/api/refresh`
- CORS configuration
- Background task for periodic news fetching
- In-memory caching system

**`backend/app/models.py`** (45 lines)
- `Article` - Normalized news article model
- `ThreatTypeStat` - Statistics per threat type
- `EntityMention` - Mentioned companies/products
- `GeoStat` - Geographic statistics
- `Insights` - Complete insights response

**`backend/app/news_sources.py`** (200 lines)
- RSS feed configuration (10+ sources)
- Feed fetching and parsing logic
- HTML cleaning and text extraction
- Image URL extraction
- Deduplication logic

**`backend/app/insights.py`** (150 lines)
- Threat type classification rules
- Entity extraction (companies, products)
- Geographic mention detection
- Statistics computation (24h, 7d)
- Trend summary generation

### Frontend Files

**`frontend/src/App.tsx`** (250 lines)
- Main application component
- Search and filter functionality
- State management for articles & insights
- Statistics cards
- Layout and routing

**`frontend/src/components/ArticleCard.tsx`** (120 lines)
- Individual article display
- Threat type badge with color coding
- Image handling with fallback
- Time formatting (e.g., "2 hours ago")
- External link handling

**`frontend/src/components/InsightsDashboard.tsx`** (200 lines)
- Horizontal bar chart (Recharts)
- Threat type distribution visualization
- Top entities list
- Geographic mentions with progress bars
- 24h vs 7d comparison cards

**`frontend/src/api/client.ts`** (40 lines)
- `fetchNews()` - Get articles with filters
- `fetchInsights()` - Get analytics data
- `refreshData()` - Trigger manual refresh
- Environment-based API URL configuration

**`frontend/src/types/index.ts`** (30 lines)
- TypeScript interfaces matching backend models
- Type safety across the application

## Data Flow

```
┌─────────────────┐
│   RSS Feeds     │ (External Sources)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ news_sources.py │ Fetch & Parse
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   insights.py   │ Analyze & Classify
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    main.py      │ Cache & Serve via API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   client.ts     │ Fetch from API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     App.tsx     │ State Management
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  ArticleCard + InsightsDashboard │ Display
└──────────────────────────────────┘
```

## Key Features Location

| Feature | Backend File | Frontend File |
|---------|-------------|---------------|
| News Aggregation | `news_sources.py` | - |
| Threat Classification | `insights.py` | - |
| API Endpoints | `main.py` | - |
| Article Display | - | `ArticleCard.tsx` |
| Search & Filter | - | `App.tsx` |
| Analytics Charts | - | `InsightsDashboard.tsx` |
| API Calls | - | `client.ts` |

## Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `package.json` | Node.js dependencies & scripts |
| `vite.config.ts` | Vite bundler config, proxy setup |
| `tailwind.config.js` | Custom colors, dark theme |
| `tsconfig.json` | TypeScript compiler options |
| `.gitignore` | Files to exclude from git |

## Environment Variables

**Backend:**
- `FETCH_INTERVAL` - Seconds between updates (default: 600)
- `CORS_ORIGINS` - Allowed frontend origins

**Frontend:**
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Extending the Platform

**Add New RSS Feed:**
1. Edit `backend/app/news_sources.py`
2. Add to `NEWS_SOURCES` list

**Add New Threat Type:**
1. Edit `backend/app/insights.py`
2. Add to `THREAT_KEYWORDS` dict
3. Update `frontend/src/components/ArticleCard.tsx` color mapping

**Add New UI Component:**
1. Create in `frontend/src/components/`
2. Import in `App.tsx`

**Add New API Endpoint:**
1. Add function in `backend/app/main.py`
2. Create client function in `frontend/src/api/client.ts`
3. Use in components

## Build Outputs

**Backend:**
- No build step required
- Python bytecode in `__pycache__/`

**Frontend:**
- `npm run build` → `dist/` directory
- Optimized HTML, CSS, JS
- Ready for static hosting

## Dependencies Count

**Backend:** 7 main packages
- FastAPI, Uvicorn, Feedparser, Requests, BeautifulSoup4, python-dateutil, Pydantic

**Frontend:** 6 main packages
- React, React-DOM, Recharts, Lucide-React, TypeScript, Vite

**DevTools:** 5 packages
- Tailwind CSS, PostCSS, Autoprefixer, Vite plugins, TypeScript types

---

**Total Lines of Code:** ~1,500 lines
**Total Files:** 30+ files
**Languages:** Python, TypeScript, CSS
