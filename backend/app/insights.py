from datetime import datetime, timedelta, timezone
from typing import List, Dict
from collections import Counter
import re
from .models import Article, Insights, ThreatTypeStat, EntityMention, GeoStat

# Comprehensive threat type classification rules
THREAT_KEYWORDS = {
    "ransomware": [
        "ransomware", "ransom", "lockbit", "blackcat", "royal", "conti", "revil", "darkside",
        "ryuk", "sodinokibi", "maze", "ragnar", "hive", "alphv", "akira", "play ransomware",
        "encryption attack", "double extortion", "ransom payment", "ransom demand"
    ],
    "phishing": [
        "phishing", "spear phishing", "whaling", "spoofing", "credential harvesting",
        "fake login", "phishing campaign", "phishing email", "email scam", "business email compromise",
        "bec attack", "invoice fraud", "ceo fraud", "smishing", "vishing", "quishing",
        "credential theft", "fake website", "lookalike domain", "typosquatting"
    ],
    "data_breach": [
        "data breach", "database leak", "leak of", "records exposed", "data stolen", "breach of",
        "data exfiltration", "stolen credentials", "exposed database", "leaked data",
        "customer data breach", "pii exposed", "personally identifiable", "data dump",
        "hacked database", "compromised data", "unauthorized access to data", "data theft"
    ],
    "malware": [
        "malware", "trojan", "backdoor", "botnet", "spyware", "keylogger", "rat",
        "remote access trojan", "infostealer", "stealer", "loader", "dropper",
        "rootkit", "wiper", "virus", "worm", "banking trojan", "emotet", "qakbot",
        "trickbot", "dridex", "icedid", "cobalt strike", "mimikatz", "redline stealer"
    ],
    "vulnerability": [
        "vulnerability", "zero-day", "cve-", "exploit", "patch", "security flaw",
        "security update", "bug fix", "critical vulnerability", "remote code execution",
        "rce", "privilege escalation", "sql injection", "xss", "cross-site scripting",
        "code injection", "buffer overflow", "authentication bypass", "security patch",
        "proof of concept", "poc exploit", "unpatched", "security advisory"
    ],
    "ddos": [
        "ddos", "denial of service", "dos attack", "distributed denial", "ddos attack",
        "amplification attack", "reflection attack", "botnet attack", "flooding attack",
        "service disruption", "availability attack", "ddos mitigation"
    ],
    "apt": [
        "apt", "advanced persistent threat", "nation-state", "state-sponsored",
        "apt group", "apt attack", "targeted attack", "espionage", "cyber espionage",
        "lazarus", "fancy bear", "apt28", "apt29", "cozy bear", "kimsuky", "apt41",
        "chinese hackers", "russian hackers", "north korean", "iranian hackers",
        "state actor", "government-backed"
    ],
    "supply_chain": [
        "supply chain", "third-party", "vendor compromise", "software supply chain",
        "dependency attack", "compromised library", "npm attack", "pypi attack",
        "supply chain attack", "third-party breach", "vendor security", "sbom",
        "solarwinds", "codecov", "3cx", "msp attack", "managed service provider"
    ],
    "crypto": [
        "cryptocurrency", "crypto fraud", "bitcoin", "crypto scam", "wallet",
        "blockchain", "ethereum", "nft", "defi", "crypto theft", "crypto hack",
        "exchange hack", "wallet drain", "rug pull", "crypto phishing",
        "mining malware", "cryptojacking", "coinbase", "binance"
    ],
    "iot": [
        "iot", "internet of things", "smart device", "router exploit", "router vulnerability",
        "firmware vulnerability", "iot botnet", "mirai", "smart home", "connected device",
        "industrial iot", "scada", "ics", "operational technology", "ot security",
        "smart camera", "ip camera", "nvr", "dvr exploit"
    ],
    "cloud_security": [
        "cloud security", "aws", "azure", "gcp", "google cloud", "cloud misconfiguration",
        "s3 bucket", "exposed bucket", "cloud breach", "serverless", "lambda",
        "kubernetes", "k8s", "docker", "container security", "cloud storage",
        "saas security", "cloud access", "cloud vulnerability", "terraform"
    ],
    "social_engineering": [
        "social engineering", "pretexting", "baiting", "tailgating", "quid pro quo",
        "manipulation attack", "human error", "trust exploitation", "psychological manipulation",
        "se attack", "vishing", "voice phishing", "phone scam", "impersonation"
    ],
    "insider_threat": [
        "insider threat", "rogue employee", "insider attack", "employee theft",
        "data exfiltration by employee", "privileged user", "insider risk",
        "malicious insider", "negligent insider", "former employee", "contractor breach"
    ],
    "mobile_security": [
        "mobile malware", "android malware", "ios malware", "mobile app",
        "app vulnerability", "mobile banking trojan", "mobile phishing",
        "app store", "google play", "mobile device", "smartphone attack",
        "tablet security", "mobile threat", "pegasus", "spyware on phone"
    ],
    "ai_ml_security": [
        "ai security", "machine learning", "deepfake", "synthetic media", "chatgpt",
        "llm", "large language model", "prompt injection", "model poisoning",
        "adversarial attack", "ai vulnerability", "automated attack", "ai-powered",
        "chatbot security", "generative ai", "ai threat"
    ],
    "web_security": [
        "xss", "cross-site scripting", "sql injection", "sqli", "csrf",
        "cross-site request forgery", "web application", "webapp vulnerability",
        "web exploit", "web shell", "file upload", "path traversal",
        "directory traversal", "xxe", "xml external entity", "deserialization",
        "web attack", "http vulnerability", "web server"
    ],
    "authentication": [
        "authentication", "credential stuffing", "brute force", "password spray",
        "password attack", "mfa bypass", "2fa bypass", "authentication bypass",
        "session hijacking", "token theft", "oauth", "saml", "sso",
        "password manager", "weak password", "default credentials", "credential access"
    ],
    "network_security": [
        "network intrusion", "lateral movement", "network attack", "man in the middle",
        "mitm", "arp spoofing", "dns hijacking", "network segmentation",
        "vpn vulnerability", "firewall bypass", "network scanning", "port scan",
        "network traffic", "packet sniffing", "network breach", "perimeter security"
    ],
    "privacy": [
        "gdpr", "privacy violation", "data privacy", "personal data", "pii",
        "ccpa", "privacy breach", "surveillance", "tracking", "data collection",
        "consent violation", "privacy law", "data protection", "right to be forgotten",
        "privacy policy", "user privacy", "metadata", "fingerprinting"
    ],
    "incident_response": [
        "incident response", "breach response", "forensics", "digital forensics",
        "incident handling", "cyber incident", "security incident", "breach notification",
        "post-mortem", "root cause analysis", "containment", "eradication",
        "recovery", "incident report", "breach investigation"
    ],
    "email_security": [
        "email security", "spam", "email attack", "email spoofing", "dmarc",
        "spf", "dkim", "email authentication", "malicious email", "email threat",
        "email gateway", "email filter", "email phishing", "email compromise",
        "email forwarding", "email exfiltration"
    ],
    "compliance": [
        "compliance", "regulatory", "audit", "pci dss", "hipaa", "sox",
        "iso 27001", "nist", "cis controls", "compliance violation",
        "regulatory fine", "non-compliant", "security standard", "certification",
        "framework", "baseline", "security control"
    ]
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

    # Note: Articles are now pre-classified when fetched, no need to re-classify here

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
