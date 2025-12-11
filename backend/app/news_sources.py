import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil import parser as date_parser
import hashlib
import logging
from typing import List, Dict, Optional
from .models import Article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comprehensive list of Threat Intelligence RSS feeds - VERIFIED WORKING
NEWS_SOURCES = [
    # Major Security News Sites & Magazines
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "type": "rss"
    },
    {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews",
        "type": "rss"
    },
    {
        "name": "SecurityWeek",
        "url": "https://www.securityweek.com/feed/",
        "type": "rss"
    },
    {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com/rss/all.xml",
        "type": "rss"
    },
    {
        "name": "InfoSecurity Magazine",
        "url": "https://www.infosecurity-magazine.com/rss/news/",
        "type": "rss"
    },
    {
        "name": "SC Magazine",
        "url": "https://www.scmagazine.com/feed",
        "type": "rss"
    },
    {
        "name": "Schneier on Security",
        "url": "https://www.schneier.com/blog/atom.xml",
        "type": "rss"
    },
    {
        "name": "Graham Cluley",
        "url": "https://grahamcluley.com/feed/",
        "type": "rss"
    },

    # Government & CERT Feeds
    {
        "name": "CISA Alerts",
        "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "type": "rss"
    },
    {
        "name": "US-CERT Current Activity",
        "url": "https://us-cert.cisa.gov/ncas/current-activity.xml",
        "type": "rss"
    },
    {
        "name": "US-CERT Alerts",
        "url": "https://us-cert.cisa.gov/ncas/alerts.xml",
        "type": "rss"
    },
    {
        "name": "NIST Cybersecurity Insights",
        "url": "https://www.nist.gov/blogs/cybersecurity-insights/rss.xml",
        "type": "rss"
    },

    # Threat Intelligence Focused Sources
    {
        "name": "Recorded Future - The Record",
        "url": "https://therecord.media/feed",
        "type": "rss"
    },
    {
        "name": "Palo Alto Unit 42",
        "url": "http://researchcenter.paloaltonetworks.com/unit42/feed/",
        "type": "rss"
    },
    {
        "name": "CrowdStrike Blog",
        "url": "https://www.crowdstrike.com/blog/feed/",
        "type": "rss"
    },
    {
        "name": "Mandiant",
        "url": "https://www.mandiant.com/resources/blog/rss.xml",
        "type": "rss"
    },
    {
        "name": "Secureworks CTU",
        "url": "https://www.secureworks.com/blog/rss",
        "type": "rss"
    },
    {
        "name": "Kaspersky Securelist",
        "url": "https://securelist.com/feed/",
        "type": "rss"
    },
    {
        "name": "Cisco Talos",
        "url": "http://feeds.feedburner.com/feedburner/Talos",
        "type": "rss"
    },
    {
        "name": "SentinelOne Labs",
        "url": "https://www.sentinelone.com/labs/feed/",
        "type": "rss"
    },
    {
        "name": "Checkpoint Research",
        "url": "https://research.checkpoint.com/feed/",
        "type": "rss"
    },

    # Vendor Security Blogs
    {
        "name": "Microsoft Security",
        "url": "https://www.microsoft.com/security/blog/feed/",
        "type": "rss"
    },
    {
        "name": "Microsoft Security Response Center",
        "url": "https://msrc-blog.microsoft.com/feed/",
        "type": "rss"
    },
    {
        "name": "Google Security Blog",
        "url": "https://googleonlinesecurity.blogspot.com/atom.xml",
        "type": "rss"
    },
    {
        "name": "Google Project Zero",
        "url": "https://googleprojectzero.blogspot.com/feeds/posts/default",
        "type": "rss"
    },
    {
        "name": "Malwarebytes Labs",
        "url": "https://blog.malwarebytes.com/feed/",
        "type": "rss"
    },
    {
        "name": "Sophos Naked Security",
        "url": "https://nakedsecurity.sophos.com/feed/",
        "type": "rss"
    },
    {
        "name": "Bitdefender Labs",
        "url": "https://www.bitdefender.com/blog/api/rss/labs/",
        "type": "rss"
    },
    {
        "name": "Trend Micro Security",
        "url": "http://feeds.trendmicro.com/TrendMicroSimplySecurity",
        "type": "rss"
    },
    {
        "name": "Cloudflare Security",
        "url": "https://blog.cloudflare.com/tag/security/rss",
        "type": "rss"
    },
    {
        "name": "IBM Security Intelligence",
        "url": "https://securityintelligence.com/feed/",
        "type": "rss"
    },

    # Newsletters & Daily Briefings
    {
        "name": "KrebsOnSecurity",
        "url": "https://krebsonsecurity.com/feed/",
        "type": "rss"
    },
    {
        "name": "The CyberWire",
        "url": "https://thecyberwire.com/feeds/rss.xml",
        "type": "rss"
    },
    {
        "name": "Risky Business",
        "url": "https://risky.biz/feeds/risky-business/",
        "type": "rss"
    },

    # Community & Research Sources
    {
        "name": "SANS ISC",
        "url": "https://isc.sans.edu/rssfeed_full.xml",
        "type": "rss"
    },
    {
        "name": "Troy Hunt",
        "url": "https://www.troyhunt.com/rss/",
        "type": "rss"
    },
    {
        "name": "Google TAG",
        "url": "https://blog.google/threat-analysis-group/rss/",
        "type": "rss"
    },

    # Additional Quality Sources
    {
        "name": "Security Affairs",
        "url": "http://securityaffairs.co/wordpress/feed",
        "type": "rss"
    },
    {
        "name": "HackRead",
        "url": "https://www.hackread.com/feed/",
        "type": "rss"
    },
    {
        "name": "Help Net Security",
        "url": "https://www.helpnetsecurity.com/feed/",
        "type": "rss"
    },
    {
        "name": "Ars Technica Security",
        "url": "https://feeds.arstechnica.com/arstechnica/security",
        "type": "rss"
    },
    {
        "name": "CSO Online",
        "url": "https://www.csoonline.com/feed/",
        "type": "rss"
    },
    {
        "name": "Reddit r/netsec",
        "url": "https://www.reddit.com/r/netsec/.rss",
        "type": "rss"
    }
]


def clean_html(text: str) -> str:
    """Remove HTML tags and clean text"""
    if not text:
        return ""
    soup = BeautifulSoup(text, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


def truncate_text(text: str, max_length: int = 300) -> str:
    """Truncate text to max_length"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."


def parse_date(date_str: str) -> datetime:
    """Parse various date formats to datetime"""
    try:
        dt = date_parser.parse(date_str)
        # Ensure timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now(timezone.utc)


def extract_image_from_entry(entry: Dict) -> Optional[str]:
    """Extract image URL from feed entry"""
    # Try media:content
    if hasattr(entry, 'media_content') and entry.media_content:
        return entry.media_content[0].get('url')

    # Try media:thumbnail
    if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
        return entry.media_thumbnail[0].get('url')

    # Try enclosures
    if hasattr(entry, 'enclosures') and entry.enclosures:
        for enclosure in entry.enclosures:
            if enclosure.get('type', '').startswith('image/'):
                return enclosure.get('href')

    # Try to find image in content
    if hasattr(entry, 'content') and entry.content:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')

    # Try summary
    if hasattr(entry, 'summary'):
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')

    return None


def fetch_feed(source: Dict) -> List[Article]:
    """Fetch and parse a single RSS feed"""
    articles = []

    try:
        logger.info(f"Fetching feed from {source['name']}...")

        # Set a reasonable timeout and user agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(source['url'], headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()

        # Parse the feed
        feed = feedparser.parse(response.content)

        if feed.bozo and feed.bozo_exception:
            logger.warning(f"Feed parsing warning for {source['name']}: {feed.bozo_exception}")

        if not feed.entries:
            logger.warning(f"No entries found in feed for {source['name']}")

        for entry in feed.entries:
            try:
                # Generate unique ID from URL
                url = entry.get('link', entry.get('id', ''))
                article_id = hashlib.md5(url.encode()).hexdigest()

                # Extract title
                title = entry.get('title', 'No Title')

                # Extract and clean summary
                summary = entry.get('summary', entry.get('description', ''))
                summary = clean_html(summary)
                summary = truncate_text(summary)

                # Parse published date
                published_str = entry.get('published', entry.get('updated', ''))
                published_at = parse_date(published_str) if published_str else datetime.now(timezone.utc)

                # Extract image
                image_url = extract_image_from_entry(entry)

                article = Article(
                    id=article_id,
                    title=title,
                    source=source['name'],
                    published_at=published_at,
                    url=url,
                    summary=summary,
                    image_url=image_url
                )

                articles.append(article)

            except Exception as e:
                logger.error(f"Error parsing entry from {source['name']}: {e}")
                continue

        if articles:
            logger.info(f"✅ Successfully fetched {len(articles)} articles from {source['name']}")
        else:
            logger.warning(f"⚠️  {source['name']} returned 0 articles")

    except requests.exceptions.Timeout:
        logger.error(f"❌ Timeout fetching {source['name']} (URL: {source['url']})")
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ HTTP {e.response.status_code} error fetching {source['name']} (URL: {source['url']})")
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error fetching {source['name']}: {e} (URL: {source['url']})")
    except Exception as e:
        logger.error(f"❌ Unexpected error fetching {source['name']}: {e} (URL: {source['url']})")

    return articles


def fetch_all_feeds() -> List[Article]:
    """Fetch all configured news feeds"""
    all_articles = []

    for source in NEWS_SOURCES:
        articles = fetch_feed(source)
        all_articles.extend(articles)

    # Sort by published date (newest first)
    all_articles.sort(key=lambda x: x.published_at, reverse=True)

    # Remove duplicates based on ID
    seen_ids = set()
    unique_articles = []
    for article in all_articles:
        if article.id not in seen_ids:
            seen_ids.add(article.id)
            unique_articles.append(article)

    logger.info(f"Total unique articles fetched: {len(unique_articles)}")

    return unique_articles
