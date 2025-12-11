import { Insights } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, Globe, Users, AlertTriangle } from 'lucide-react';

interface InsightsDashboardProps {
  insights: Insights | null;
  isLoading: boolean;
}

const THREAT_TYPE_COLORS: Record<string, string> = {
  ransomware: '#ef4444',
  phishing: '#f97316',
  data_breach: '#a855f7',
  malware: '#ec4899',
  vulnerability: '#eab308',
  ddos: '#3b82f6',
  apt: '#6366f1',
  supply_chain: '#06b6d4',
  crypto: '#10b981',
  iot: '#14b8a6',
  other: '#6b7280',
};

export function InsightsDashboard({ insights, isLoading }: InsightsDashboardProps) {
  if (isLoading) {
    return (
      <section className="mt-12 mb-8">
        <div className="bg-dark-700 rounded-lg p-8 border border-dark-600">
          <div className="animate-pulse">
            <div className="h-8 bg-dark-600 rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-dark-600 rounded w-2/3 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="h-64 bg-dark-600 rounded"></div>
              <div className="h-64 bg-dark-600 rounded"></div>
              <div className="h-64 bg-dark-600 rounded"></div>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (!insights) {
    return null;
  }

  // Prepare chart data
  const chartData = insights.threat_type_stats.map(stat => ({
    name: stat.threat_type.replace(/_/g, ' ').toUpperCase(),
    value: stat.last_7d,
    last_24h: stat.last_24h,
    color: THREAT_TYPE_COLORS[stat.threat_type] || THREAT_TYPE_COLORS.other
  }));

  return (
    <section className="mt-12 mb-8">
      <div className="bg-dark-700 rounded-lg p-8 border border-dark-600 shadow-xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <TrendingUp className="text-blue-400" size={32} />
            <h2 className="text-3xl font-bold text-white">Live Intelligence Insights</h2>
          </div>
          <p className="text-gray-400 text-lg">
            Real-time analysis and trends across threat intelligence sources
          </p>
        </div>

        {/* Summary Banner */}
        {insights.summary && (
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mb-8">
            <div className="flex items-start gap-3">
              <AlertTriangle className="text-blue-400 flex-shrink-0 mt-1" size={20} />
              <p className="text-blue-200 font-medium">{insights.summary}</p>
            </div>
          </div>
        )}

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Threat Type Distribution */}
          <div className="lg:col-span-2 bg-dark-800 rounded-lg p-6 border border-dark-600">
            <h3 className="text-xl font-semibold text-white mb-4">Threat Type Distribution (Last 7 Days)</h3>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis type="number" stroke="#9ca3af" />
                  <YAxis dataKey="name" type="category" stroke="#9ca3af" width={90} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '0.5rem',
                      color: '#fff'
                    }}
                    formatter={(value: number, name: string) => {
                      if (name === 'value') return [value, 'Articles (7d)'];
                      return [value, name];
                    }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                No threat data available
              </div>
            )}

            {/* 24h vs 7d Comparison */}
            <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-4">
              {insights.threat_type_stats.slice(0, 6).map((stat) => (
                <div key={stat.threat_type} className="bg-dark-700 rounded-lg p-3 border border-dark-600">
                  <div className="text-xs text-gray-400 mb-1">
                    {stat.threat_type.replace(/_/g, ' ').toUpperCase()}
                  </div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-lg font-bold text-white">{stat.last_24h}</span>
                    <span className="text-xs text-gray-500">/ 24h</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Side Panel */}
          <div className="space-y-6">
            {/* Top Entities */}
            <div className="bg-dark-800 rounded-lg p-6 border border-dark-600">
              <div className="flex items-center gap-2 mb-4">
                <Users className="text-purple-400" size={20} />
                <h3 className="text-lg font-semibold text-white">Top Mentioned Entities</h3>
              </div>
              <div className="space-y-3">
                {insights.top_entities.slice(0, 8).map((entity, index) => (
                  <div key={entity.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-gray-500 w-6">#{index + 1}</span>
                      <span className="text-sm text-gray-300">{entity.name}</span>
                    </div>
                    <span className="text-sm font-semibold text-purple-400">{entity.count}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Geographic Stats */}
            <div className="bg-dark-800 rounded-lg p-6 border border-dark-600">
              <div className="flex items-center gap-2 mb-4">
                <Globe className="text-cyan-400" size={20} />
                <h3 className="text-lg font-semibold text-white">Geographic Mentions</h3>
              </div>
              <div className="space-y-3">
                {insights.geo_stats.slice(0, 8).map((geo) => (
                  <div key={geo.country} className="flex items-center justify-between">
                    <span className="text-sm text-gray-300">{geo.country}</span>
                    <div className="flex items-center gap-2">
                      <div className="bg-cyan-500/20 rounded-full h-2 w-16 overflow-hidden">
                        <div
                          className="bg-cyan-500 h-full"
                          style={{
                            width: `${Math.min(100, (geo.count_last_7d / Math.max(...insights.geo_stats.map(g => g.count_last_7d))) * 100)}%`
                          }}
                        ></div>
                      </div>
                      <span className="text-sm font-semibold text-cyan-400 w-8 text-right">{geo.count_last_7d}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 pt-6 border-t border-dark-600">
          <p className="text-xs text-gray-500 text-center">
            Last updated: {new Date(insights.generated_at).toLocaleString()}
          </p>
        </div>
      </div>
    </section>
  );
}
