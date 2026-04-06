import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { getAnalytics } from '../services/api';

const Analytics = () => {
    const [analyticsData, setAnalyticsData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                const response = await getAnalytics();
                if (response.success) {
                    setAnalyticsData(response);
                } else {
                    setError(response.error || 'Failed to fetch analytics');
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAnalytics();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                    <strong className="font-bold">Error! </strong>
                    <span className="block sm:inline">{error}</span>
                </div>
            </div>
        );
    }

    const { charts, patterns, recommendations, weaknesses } = analyticsData;

    return (
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-6">Analytics Dashboard</h1>

            {/* Summary Stats */}
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">Avg. WPM</dt>
                                    <dd className="flex items-baseline">
                                        <div className="text-2xl font-semibold text-gray-900">{patterns.average_wpm}</div>
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">Avg. Accuracy</dt>
                                    <dd className="flex items-baseline">
                                        <div className="text-2xl font-semibold text-gray-900">{patterns.average_accuracy}%</div>
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">Avg. Errors</dt>
                                    <dd className="flex items-baseline">
                                        <div className="text-2xl font-semibold text-gray-900">{patterns.average_errors}</div>
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">Total Tests</dt>
                                    <dd className="flex items-baseline">
                                        <div className="text-2xl font-semibold text-gray-900">{patterns.total_tests}</div>
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-8">
                {charts && charts.wpm_trend ? (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">WPM Over Time</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <img src={charts.wpm_trend} alt="WPM Trend" className="w-full" onError={(e) => { e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iMzIiIHk9IjMyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5DaGFydCBOb3QgQXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg=='; }} />
                        </div>
                    </div>
                ) : (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">WPM Over Time</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <div className="text-center py-8 text-gray-500">
                                Not enough data to generate chart
                            </div>
                        </div>
                    </div>
                )}

                {charts && charts.accuracy_trend ? (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Accuracy Over Time</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <img src={charts.accuracy_trend} alt="Accuracy Trend" className="w-full" onError={(e) => { e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iMzIiIHk9IjMyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5DaGFydCBOb3QgQXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg=='; }} />
                        </div>
                    </div>
                ) : (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Accuracy Over Time</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <div className="text-center py-8 text-gray-500">
                                Not enough data to generate chart
                            </div>
                        </div>
                    </div>
                )}

                {charts && charts.difficulty_comparison ? (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Performance by Difficulty</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <img src={charts.difficulty_comparison} alt="Difficulty Comparison" className="w-full" onError={(e) => { e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iMzIiIHk9IjMyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5DaGFydCBOb3QgQXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg=='; }} />
                        </div>
                    </div>
                ) : (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Performance by Difficulty</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <div className="text-center py-8 text-gray-500">
                                Not enough data to generate chart
                            </div>
                        </div>
                    </div>
                )}

                {charts && charts.error_distribution ? (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Error Distribution</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <img src={charts.error_distribution} alt="Error Distribution" className="w-full" onError={(e) => { e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iMzIiIHk9IjMyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5DaGFydCBOb3QgQXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg=='; }} />
                        </div>
                    </div>
                ) : (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Error Distribution</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <div className="text-center py-8 text-gray-500">
                                Not enough data to generate chart
                            </div>
                        </div>
                    </div>
                )}

                {charts && charts.wpm_vs_accuracy ? (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">WPM vs Accuracy</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <img src={charts.wpm_vs_accuracy} alt="WPM vs Accuracy" className="w-full" onError={(e) => { e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iMzIiIHk9IjMyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5DaGFydCBOb3QgQXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg=='; }} />
                        </div>
                    </div>
                ) : (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">WPM vs Accuracy</h3>
                        </div>
                        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                            <div className="text-center py-8 text-gray-500">
                                Not enough data to generate chart
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Insights Section */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-8">
                {/* Weaknesses Analysis */}
                <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                    <div className="px-4 py-5 sm:px-6">
                        <h3 className="text-lg leading-6 font-medium text-gray-900">Weakness Analysis</h3>
                    </div>
                    <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                        {weaknesses.needs_more_data ? (
                            <div className="text-center py-4">
                                <p className="text-gray-500">{weaknesses.message}</p>
                            </div>
                        ) : (
                            <div>
                                {weaknesses.common_issues.length > 0 && (
                                    <div className="mb-4">
                                        <h4 className="text-md font-medium text-gray-900 mb-2">Common Issues</h4>
                                        <ul className="list-disc pl-5 space-y-1">
                                            {weaknesses.common_issues.map((issue, index) => (
                                                <li key={index} className="text-gray-700">{issue}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {weaknesses.strengths.length > 0 && (
                                    <div className="mb-4">
                                        <h4 className="text-md font-medium text-gray-900 mb-2">Strengths</h4>
                                        <ul className="list-disc pl-5 space-y-1">
                                            {weaknesses.strengths.map((strength, index) => (
                                                <li key={index} className="text-green-700">{strength}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {weaknesses.areas_for_improvement.length > 0 && (
                                    <div>
                                        <h4 className="text-md font-medium text-gray-900 mb-2">Areas for Improvement</h4>
                                        <ul className="list-disc pl-5 space-y-1">
                                            {weaknesses.areas_for_improvement.map((area, index) => (
                                                <li key={index} className="text-yellow-700">{area}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>

                {/* Recommendations */}
                <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                    <div className="px-4 py-5 sm:px-6">
                        <h3 className="text-lg leading-6 font-medium text-gray-900">Personalized Recommendations</h3>
                    </div>
                    <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
                        {recommendations.length > 0 ? (
                            <ul className="list-disc pl-5 space-y-2">
                                {recommendations.map((recommendation, index) => (
                                    <li key={index} className="text-gray-700">{recommendation}</li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-gray-500">No recommendations available at this time.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Analytics;