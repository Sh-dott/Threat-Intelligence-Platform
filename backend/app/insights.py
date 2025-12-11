from datetime import datetime, timedelta, timezone
from typing import List, Dict
from collections import Counter
import re
from .models import Article, Insights, ThreatTypeStat, EntityMention, GeoStat

# Threat type classification rules
THREAT_KEYWORDS = {
    "ransomware": ["ransomware", "ransom", "lockbit", "blackcat", "royal"],
    "phishing": ["phishing", "spoofing", "credential harvesting", "fake login", "spear phishing"],
    "data_breach": ["data breach", "database leak", "leak of", "records exposed", "data stolen", "breach of"],
    "malware": ["malware", "trojan", "backdoor", "botnet", "spyware", "keylogger", "rat"],
    "vulnerability": ["vulnerability", "zero-day", "cve-", "exploit", "patch", "security flaw"],
    "ddos": ["ddos", "denial of service", "dos attack"],
    "apt": ["apt", "advanced persistent threat", "nation-state", "state-sponsored"],
    "supply_chain": ["supply chain", "third-party", "vendor compromise"],
    "crypto": ["cryptocurrency", "crypto fraud", "bitcoin", "crypto scam", "wallet"],
    "iot": ["iot", "internet of things", "smart device", "router exploit"]
}

# Known entities (companies, products, etc.)
KNOWN_ENTITIES = [
    "Microsoft", "Google", "Apple", "Amazon", "Meta", "Facebook",
    "Cisco", "Fortinet", "Palo Alto", "SonicWall", "VMware",
    "Oracle", "SAP", "Adobe", "Citrix", "Linux", "Windows",
    "Android", "iOS", "Chrome", "Firefox", "Safari",
    "Okta", "Cloudflare", "Akamai", "GitHub", "GitLab",
    "MOVEit", "Ivanti", "JetBrains", "Atlassian", "WordPress"
]

# Countries and regions
COUNTRIES = [
    "US", "USA", "United States", "UK", "Britain", "China", "Russia",
    "Israel", "Iran", "North Korea", "Ukraine", "France", "Germany",
    "India", "Brazil", "Japan", "South Korea", "Australia", "Canada",
    "Italy", "Spain", "Netherlands", "Sweden", "Norway", "Denmark"
]


def classify_threat_type(article: Article) -> str:
    """Classify article into threat type based on keywords"""
    text = (article.title + " " + article.summary).lower()

    # Count matches for each threat type
    matches = {}
    for threat_type, keywords in THREAT_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text)
        if count > 0:
            matches[threat_type] = count

    # Return the threat type with most matches
    if matches:
        return max(matches, key=matches.get)

    return "other"


def extract_entities(articles: List[Article]) -> List[EntityMention]:
    """Extract and count mentioned entities"""
    entity_counter = Counter()

    for article in articles:
        text = article.title + " " + article.summary

        # Look for known entities
        for entity in KNOWN_ENTITIES:
            # Case-insensitive word boundary search
            pattern = r'\b' + re.escape(entity) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                entity_counter[entity] += 1

        # Also look for capitalized words (potential entities)
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        for word in words:
            if len(word) > 3 and word not in ['The', 'This', 'That', 'What', 'When', 'Where', 'Who', 'Why', 'How']:
                entity_counter[word] += 1

    # Get top 10 entities
    top_entities = [
        EntityMention(name=name, count=count)
        for name, count in entity_counter.most_common(10)
    ]

    return top_entities


def extract_geographies(articles: List[Article]) -> List[GeoStat]:
    """Extract and count geographic mentions"""
    geo_counter = Counter()

    for article in articles:
        text = article.title + " " + article.summary

        for country in COUNTRIES:
            pattern = r'\b' + re.escape(country) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                # Normalize country name
                normalized = country
                if country in ["USA", "United States"]:
                    normalized = "US"
                elif country == "Britain":
                    normalized = "UK"
                geo_counter[normalized] += 1

    # Get stats
    geo_stats = [
        GeoStat(country=country, count_last_7d=count)
        for country, count in geo_counter.most_common(15)
    ]

    return geo_stats


def compute_threat_stats(articles: List[Article]) -> List[ThreatTypeStat]:
    """Compute statistics by threat type"""
    now = datetime.now(timezone.utc)
    cutoff_24h = now - timedelta(hours=24)
    cutoff_7d = now - timedelta(days=7)

    # Group articles by threat type
    threat_groups = {}
    for article in articles:
        threat_type = article.threat_type or "other"
        if threat_type not in threat_groups:
            threat_groups[threat_type] = []
        threat_groups[threat_type].append(article)

    # Compute stats
    stats = []
    for threat_type, type_articles in threat_groups.items():
        count_24h = sum(1 for a in type_articles if a.published_at >= cutoff_24h)
        count_7d = sum(1 for a in type_articles if a.published_at >= cutoff_7d)

        if count_7d > 0:  # Only include types with recent activity
            stats.append(ThreatTypeStat(
                threat_type=threat_type,
                last_24h=count_24h,
                last_7d=count_7d
            ))

    # Sort by 7-day count (descending)
    stats.sort(key=lambda x: x.last_7d, reverse=True)

    return stats


def generate_insights(articles: List[Article]) -> Insights:
    """Generate intelligence insights from articles"""

    # Classify all articles
    for article in articles:
        article.threat_type = classify_threat_type(article)

    # Filter to last 7 days for insights
    now = datetime.now(timezone.utc)
    cutoff_7d = now - timedelta(days=7)
    recent_articles = [a for a in articles if a.published_at >= cutoff_7d]

    # Compute statistics
    threat_stats = compute_threat_stats(recent_articles)
    top_entities = extract_entities(recent_articles)
    geo_stats = extract_geographies(recent_articles)

    # Generate summary
    summary = "No significant threats detected."
    if threat_stats:
        top_threat = threat_stats[0]
        summary = f"{top_threat.threat_type.replace('_', ' ').title()} is the most reported threat type in the last 7 days with {top_threat.last_7d} articles."

    insights = Insights(
        generated_at=now,
        threat_type_stats=threat_stats,
        top_entities=top_entities,
        geo_stats=geo_stats,
        summary=summary
    )

    return insights
