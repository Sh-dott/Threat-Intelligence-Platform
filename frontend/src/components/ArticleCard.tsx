import { Article } from '../types';
import { ExternalLink, Calendar, Tag } from 'lucide-react';

interface ArticleCardProps {
  article: Article;
}

const THREAT_TYPE_COLORS: Record<string, string> = {
  ransomware: 'bg-red-500/20 text-red-300 border-red-500/30',
  phishing: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
  data_breach: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
  malware: 'bg-pink-500/20 text-pink-300 border-pink-500/30',
  vulnerability: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
  ddos: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  apt: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30',
  supply_chain: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
  crypto: 'bg-green-500/20 text-green-300 border-green-500/30',
  iot: 'bg-teal-500/20 text-teal-300 border-teal-500/30',
  other: 'bg-gray-500/20 text-gray-300 border-gray-500/30',
};

function formatTimeAgo(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 60) {
    return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
  } else if (diffHours < 24) {
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
  } else if (diffDays < 7) {
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  } else {
    return date.toLocaleDateString();
  }
}

export function ArticleCard({ article }: ArticleCardProps) {
  const threatTypeClass = THREAT_TYPE_COLORS[article.threat_type] || THREAT_TYPE_COLORS.other;

  return (
    <article className="bg-dark-700 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border border-dark-600">
      {/* Image */}
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block"
      >
        <div className="aspect-video bg-dark-600 overflow-hidden">
          {article.image_url ? (
            <img
              src={article.image_url}
              alt={article.title}
              className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
                target.parentElement!.classList.add('flex', 'items-center', 'justify-center');
                target.parentElement!.innerHTML = '<div class="text-gray-500 text-4xl">📰</div>';
              }}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-500 text-6xl">
              📰
            </div>
          )}
        </div>
      </a>

      {/* Content */}
      <div className="p-5">
        {/* Threat Type Tag */}
        <div className="mb-3">
          <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium border ${threatTypeClass}`}>
            <Tag size={12} />
            {article.threat_type.replace(/_/g, ' ').toUpperCase()}
          </span>
        </div>

        {/* Title */}
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block group"
        >
          <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-blue-400 transition-colors line-clamp-2">
            {article.title}
          </h3>
        </a>

        {/* Metadata */}
        <div className="flex items-center gap-3 text-sm text-gray-400 mb-3">
          <span className="font-medium text-blue-400">{article.source}</span>
          <span className="flex items-center gap-1">
            <Calendar size={14} />
            {formatTimeAgo(article.published_at)}
          </span>
        </div>

        {/* Summary */}
        <p className="text-gray-300 text-sm leading-relaxed line-clamp-3 mb-4">
          {article.summary}
        </p>

        {/* Read More Link */}
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-sm text-blue-400 hover:text-blue-300 font-medium transition-colors"
        >
          Read Full Article
          <ExternalLink size={14} />
        </a>
      </div>
    </article>
  );
}
