from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
from datetime import datetime, timezone
import logging

from .models import Article, Insights
from .news_sources import fetch_all_feeds
from .insights import generate_insights, classify_threat_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Threat Intelligence Platform API",
    description="Real-time threat intelligence news aggregation and analysis",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://sh-dott.github.io",  # GitHub Pages
        "https://*.herokuapp.com",  # Heroku backend
        "https://*.vercel.app",  # Vercel deployments
        "https://threat-intelligence-platform.vercel.app",  # Vercel frontend
        "https://threat-intel-api.vercel.app"  # Vercel backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache
articles_cache: List[Article] = []
insights_cache: Insights = None
last_fetch_time: datetime = None
FETCH_INTERVAL = 1800  # 30 minutes in seconds (real-time updates every 30 min)
MAX_ARTICLES = 5000  # Keep last 5000 articles to prevent unlimited growth


async def update_news_cache():
    """Background task to periodically fetch news and accumulate articles"""
    global articles_cache, insights_cache, last_fetch_time

    while True:
        try:
            logger.info("Starting news fetch cycle...")

            # Fetch all feeds
            new_articles = fetch_all_feeds()

            # Merge new articles with existing ones
            # Create a dictionary of existing articles by ID
            existing_ids = {article.id for article in articles_cache}

            # Add only new articles (not already in cache)
            added_count = 0
            for article in new_articles:
                if article.id not in existing_ids:
                    articles_cache.append(article)
                    added_count += 1

            # Sort by published date (newest first)
            articles_cache.sort(key=lambda x: x.published_at, reverse=True)

            # Keep only the most recent MAX_ARTICLES
            if len(articles_cache) > MAX_ARTICLES:
                articles_cache = articles_cache[:MAX_ARTICLES]

            logger.info(f"Added {added_count} new articles. Total articles: {len(articles_cache)}")

            # Re-classify all articles (in case classification rules were updated)
            if articles_cache:
                for article in articles_cache:
                    article.threat_type = classify_threat_type(article)

            # Generate insights on all accumulated articles
            if articles_cache:
                insights_cache = generate_insights(articles_cache)

            last_fetch_time = datetime.now(timezone.utc)

        except Exception as e:
            logger.error(f"Error updating news cache: {e}")

        # Wait for next fetch cycle
        await asyncio.sleep(FETCH_INTERVAL)


@app.on_event("startup")
async def startup_event():
    """Initialize cache on startup"""
    logger.info("Starting Threat Intelligence Platform API...")

    # Do initial fetch synchronously to have data ready
    try:
        logger.info("Performing initial news fetch...")
        global articles_cache, insights_cache, last_fetch_time

        articles = fetch_all_feeds()
        articles_cache = articles

        # Re-classify all articles with improved classification system
        if articles:
            logger.info("Re-classifying all articles with improved threat detection...")
            reclassified_count = 0
            for article in articles_cache:
                old_type = article.threat_type
                article.threat_type = classify_threat_type(article)
                if old_type != article.threat_type:
                    reclassified_count += 1
            logger.info(f"Re-classified {reclassified_count} articles with new categories")

            insights_cache = generate_insights(articles)

        last_fetch_time = datetime.now(timezone.utc)
        logger.info(f"Initial fetch complete. Total articles: {len(articles_cache)}")

    except Exception as e:
        logger.error(f"Error during initial fetch: {e}")

    # Start background task
    asyncio.create_task(update_news_cache())


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "name": "Threat Intelligence Platform API",
        "version": "1.0.0",
        "status": "operational",
        "last_update": last_fetch_time.isoformat() if last_fetch_time else None,
        "total_articles": len(articles_cache)
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "articles_count": len(articles_cache),
        "last_fetch": last_fetch_time.isoformat() if last_fetch_time else None
    }


@app.get("/api/news", response_model=List[Article])
def get_news(
    limit: int = 10000,
    threat_type: str = None,
    search: str = None
):
    """
    Get normalized news articles

    Parameters:
    - limit: Maximum number of articles to return (default: 10000, effectively unlimited)
    - threat_type: Filter by threat type (optional)
    - search: Search in title and summary (optional)
    """
    try:
        articles = articles_cache.copy()

        # Apply filters
        if threat_type:
            articles = [a for a in articles if a.threat_type == threat_type]

        if search:
            search_lower = search.lower()
            articles = [
                a for a in articles
                if search_lower in a.title.lower() or search_lower in a.summary.lower()
            ]

        # Apply limit
        articles = articles[:limit]

        return articles

    except Exception as e:
        logger.error(f"Error getting news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/insights", response_model=Insights)
def get_insights():
    """
    Get intelligence insights and trends

    Returns computed statistics about threat types, entities, and geographies
    """
    try:
        if insights_cache is None:
            raise HTTPException(
                status_code=503,
                detail="Insights not yet available. Please try again in a moment."
            )

        return insights_cache

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/refresh")
async def refresh_data():
    """
    Manually trigger a data refresh

    Useful for testing or forcing an immediate update
    """
    try:
        global articles_cache, insights_cache, last_fetch_time

        logger.info("Manual refresh triggered")

        # Fetch new articles
        new_articles = fetch_all_feeds()

        # Merge with existing articles (same logic as background task)
        existing_ids = {article.id for article in articles_cache}
        added_count = 0
        for article in new_articles:
            if article.id not in existing_ids:
                articles_cache.append(article)
                added_count += 1

        # Sort by published date (newest first)
        articles_cache.sort(key=lambda x: x.published_at, reverse=True)

        # Keep only the most recent MAX_ARTICLES
        if len(articles_cache) > MAX_ARTICLES:
            articles_cache = articles_cache[:MAX_ARTICLES]

        # Generate insights
        if articles_cache:
            insights_cache = generate_insights(articles_cache)

        last_fetch_time = datetime.now(timezone.utc)

        return {
            "status": "success",
            "new_articles_added": added_count,
            "total_articles": len(articles_cache),
            "timestamp": last_fetch_time.isoformat()
        }

    except Exception as e:
        logger.error(f"Error during manual refresh: {e}")
        raise HTTPException(status_code=500, detail=str(e))
