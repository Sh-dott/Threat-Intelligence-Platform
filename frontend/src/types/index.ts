export interface Article {
  id: string;
  title: string;
  source: string;
  published_at: string;
  url: string;
  summary: string;
  image_url: string | null;
  threat_type: string;
}

export interface ThreatTypeStat {
  threat_type: string;
  last_24h: number;
  last_7d: number;
}

export interface EntityMention {
  name: string;
  count: number;
}

export interface GeoStat {
  country: string;
  count_last_7d: number;
}

export interface Insights {
  generated_at: string;
  threat_type_stats: ThreatTypeStat[];
  top_entities: EntityMention[];
  geo_stats: GeoStat[];
  summary: string;
}
