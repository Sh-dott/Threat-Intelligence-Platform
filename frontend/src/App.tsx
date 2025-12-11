import { useState, useEffect } from 'react';
import { ArticleCard } from './components/ArticleCard';
import { InsightsDashboard } from './components/InsightsDashboard';
import { fetchNews, fetchInsights } from './api/client';
import { Article, Insights } from './types';
import { Search, Filter, RefreshCw, Shield, Activity } from 'lucide-react';

function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [insights, setInsights] = useState<Insights | null>(null);
  const [loading, setLoading] = useState(true);
  const [insightsLoading, setInsightsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedThreatType, setSelectedThreatType] = useState<string>('');

  // Available threat types
  const threatTypes = [
    { value: '', label: 'All Types' },
    { value: 'ransomware', label: 'Ransomware' },
    { value: 'phishing', label: 'Phishing' },
    { value: 'data_breach', label: 'Data Breach' },
    { value: 'malware', label: 'Malware' },
    { value: 'vulnerability', label: 'Vulnerability' },
    { value: 'ddos', label: 'DDoS' },
    { value: 'apt', label: 'APT' },
    { value: 'supply_chain', label: 'Supply Chain' },
    { value: 'crypto', label: 'Crypto' },
    { value: 'iot', label: 'IoT' },
    { value: 'other', label: 'Other' },
  ];

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const newsData = await fetchNews(2000, selectedThreatType || undefined, searchQuery || undefined);
      setArticles(newsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load news');
      console.error('Error loading news:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadInsights = async () => {
    try {
      setInsightsLoading(true);
      const insightsData = await fetchInsights();
      setInsights(insightsData);
    } catch (err) {
      console.error('Error loading insights:', err);
    } finally {
      setInsightsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedThreatType]);

  useEffect(() => {
    loadInsights();
    // Refresh insights every 10 minutes
    const interval = setInterval(loadInsights, 10 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  const handleRefresh = async () => {
    await Promise.all([loadData(), loadInsights()]);
  };

  return (
    <div className="min-h-screen bg-dark-900 text-white">
      {/* Header */}
      <header className="bg-dark-800 border-b border-dark-600 sticky top-0 z-50 shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Shield className="text-blue-400" size={36} />
              <div>
                <h1 className="text-3xl font-bold text-white">Threat Intelligence Platform</h1>
                <p className="text-gray-400 text-sm">Real-time cybersecurity news aggregation and analysis</p>
              </div>
            </div>
            <button
              onClick={handleRefresh}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              disabled={loading}
            >
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
              Refresh
            </button>
          </div>

          {/* Search and Filter Bar */}
          <div className="flex flex-col md:flex-row gap-4">
            <form onSubmit={handleSearch} className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Search articles..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-dark-700 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-400"
                />
              </div>
            </form>

            <div className="md:w-64">
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <select
                  value={selectedThreatType}
                  onChange={(e) => setSelectedThreatType(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-dark-700 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white appearance-none cursor-pointer"
                >
                  {threatTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Stats Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-dark-800 rounded-lg p-4 border border-dark-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Articles</p>
                <p className="text-2xl font-bold text-white">{articles.length}</p>
              </div>
              <Activity className="text-blue-400" size={32} />
            </div>
          </div>

          <div className="bg-dark-800 rounded-lg p-4 border border-dark-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Sources</p>
                <p className="text-2xl font-bold text-white">
                  {new Set(articles.map(a => a.source)).size}
                </p>
              </div>
              <Shield className="text-green-400" size={32} />
            </div>
          </div>

          <div className="bg-dark-800 rounded-lg p-4 border border-dark-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Last 24 Hours</p>
                <p className="text-2xl font-bold text-white">
                  {articles.filter(a => {
                    const publishedDate = new Date(a.published_at);
                    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
                    return publishedDate >= oneDayAgo;
                  }).length}
                </p>
              </div>
              <RefreshCw className="text-purple-400" size={32} />
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-8">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* News Feed Section */}
        <section className="mb-12">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white mb-2">Latest Threat Intelligence</h2>
            <p className="text-gray-400">
              Stay informed with the latest cybersecurity news and threat intelligence from trusted sources
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-dark-700 rounded-lg h-96 animate-pulse border border-dark-600"></div>
              ))}
            </div>
          ) : articles.length === 0 ? (
            <div className="bg-dark-800 rounded-lg p-12 text-center border border-dark-600">
              <p className="text-gray-400 text-lg">No articles found. Try adjusting your filters or search query.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          )}
        </section>

        {/* Insights Dashboard */}
        <InsightsDashboard insights={insights} isLoading={insightsLoading} />
      </main>

      {/* Footer */}
      <footer className="bg-dark-800 border-t border-dark-600 py-6 mt-12">
        <div className="container mx-auto px-4 text-center text-gray-400 text-sm">
          <p>Threat Intelligence Platform &copy; {new Date().getFullYear()}</p>
          <p className="mt-2">
            Aggregating threat intelligence from multiple open-source feeds for security professionals
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
