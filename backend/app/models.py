from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Article(BaseModel):
    """Normalized article model"""
    id: str
    title: str
    source: str
    published_at: datetime
    url: str
    summary: str
    image_url: Optional[str] = None
    threat_type: Optional[str] = "other"


class ThreatTypeStat(BaseModel):
    """Statistics for a specific threat type"""
    threat_type: str
    last_24h: int
    last_7d: int


class EntityMention(BaseModel):
    """Top mentioned entity"""
    name: str
    count: int


class GeoStat(BaseModel):
    """Geographic statistics"""
    country: str
    count_last_7d: int


class Insights(BaseModel):
    """Intelligence insights computed over articles"""
    generated_at: datetime
    threat_type_stats: List[ThreatTypeStat]
    top_entities: List[EntityMention]
    geo_stats: List[GeoStat]
    summary: str = ""
