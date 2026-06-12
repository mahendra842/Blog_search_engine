import { useState, useEffect } from 'react'
import { Search, Filter, TrendingUp, BookOpen, Star, ExternalLink, Calendar, User } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Slider } from '@/components/ui/slider.jsx'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

const API_BASE_URL = 'https://searchenginegdsc.onrender.com'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [sortBy, setSortBy] = useState('relevance')
  const [minAuthenticity, setMinAuthenticity] = useState([0])
  const [showFilters, setShowFilters] = useState(false)
  const [totalResults, setTotalResults] = useState(0)

  // Fetch stats on component mount
  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`)
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setIsLoading(true)
    try {
      const params = new URLSearchParams({
        q: searchQuery,
        sort: sortBy,
        min_authenticity: minAuthenticity[0],
        limit: 20
      })
      
      const response = await fetch(`${API_BASE_URL}/search?${params}`)
      const data = await response.json()
      
      setSearchResults(data.results || [])
      setTotalResults(data.total_results || 0)
    } catch (error) {
      console.error('Error searching:', error)
      setSearchResults([])
    } finally {
      setIsLoading(false)
    }
  }

  const getAuthenticityColor = (score) => {
    if (score >= 0.8) return 'text-green-600 bg-green-50'
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const formatDate = (dateString) => {
    if (!dateString) return null
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <BookOpen className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Personal Blog Search
                </h1>
                <p className="text-sm text-gray-600">Discover authentic voices and insightful articles</p>
              </div>
            </div>
            
            {stats && (
              <div className="hidden md:flex items-center space-x-6 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <BookOpen className="h-4 w-4" />
                  <span>{stats.total_posts} posts</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4" />
                  <span>{stats.average_authenticity_score} avg score</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center mb-8"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Find Authentic Personal Stories
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Search through curated personal blogs and insightful articles, 
              filtered for authenticity and depth.
            </p>
          </motion.div>

          <motion.form
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            onSubmit={handleSearch}
            className="max-w-4xl mx-auto"
          >
            <div className="relative">
              <div className="flex space-x-2">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <Input
                    type="text"
                    placeholder="Search for personal stories, experiences, insights..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 pr-4 py-3 text-lg border-2 border-gray-200 focus:border-blue-500 rounded-xl"
                  />
                </div>
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl"
                >
                  {isLoading ? 'Searching...' : 'Search'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowFilters(!showFilters)}
                  className="px-4 py-3 rounded-xl"
                >
                  <Filter className="h-5 w-5" />
                </Button>
              </div>
            </div>

            {/* Filters */}
            <AnimatePresence>
              {showFilters && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-4 p-4 bg-white rounded-xl border border-gray-200 shadow-sm"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Sort by
                      </label>
                      <Select value={sortBy} onValueChange={setSortBy}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="relevance">Relevance</SelectItem>
                          <SelectItem value="authenticity">Authenticity Score</SelectItem>
                          <SelectItem value="date">Publication Date</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Minimum Authenticity Score: {minAuthenticity[0].toFixed(1)}
                      </label>
                      <Slider
                        value={minAuthenticity}
                        onValueChange={setMinAuthenticity}
                        max={1}
                        min={0}
                        step={0.1}
                        className="w-full"
                      />
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.form>
        </div>

        {/* Results Section */}
        {searchResults.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-semibold text-gray-900">
                Search Results
              </h3>
              <p className="text-gray-600">
                {totalResults} result{totalResults !== 1 ? 's' : ''} found
              </p>
            </div>

            <div className="space-y-6">
              {searchResults.map((result, index) => (
                <motion.div
                  key={result.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card className="hover:shadow-lg transition-shadow duration-300 border-l-4 border-l-blue-500">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <CardTitle className="text-xl mb-2 hover:text-blue-600 transition-colors">
                            <a
                              href={result.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center space-x-2"
                            >
                              <span>{result.title}</span>
                              <ExternalLink className="h-4 w-4" />
                            </a>
                          </CardTitle>
                          <CardDescription className="text-base">
                            {result.summary}
                          </CardDescription>
                        </div>
                        <Badge className={`ml-4 ${getAuthenticityColor(result.authenticity_score)}`}>
                          <Star className="h-3 w-3 mr-1" />
                          {result.authenticity_score.toFixed(2)}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                        {result.author && (
                          <div className="flex items-center space-x-1">
                            <User className="h-4 w-4" />
                            <span>{result.author}</span>
                          </div>
                        )}
                        {result.published_date && (
                          <div className="flex items-center space-x-1">
                            <Calendar className="h-4 w-4" />
                            <span>{formatDate(result.published_date)}</span>
                          </div>
                        )}
                        <div className="flex items-center space-x-1">
                          <TrendingUp className="h-4 w-4" />
                          <span>{result.blog_domain}</span>
                        </div>
                      </div>
                      
                      {result.keywords && result.keywords.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {result.keywords.slice(0, 5).map((keyword, idx) => (
                            <Badge key={idx} variant="secondary" className="text-xs">
                              {keyword}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Empty State */}
        {searchResults.length === 0 && searchQuery && !isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No results found</h3>
            <p className="text-gray-600">
              Try adjusting your search terms or filters to find more content.
            </p>
          </motion.div>
        )}

        {/* Stats Section */}
        {stats && !searchQuery && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-12"
          >
            <h3 className="text-2xl font-semibold text-gray-900 mb-6">Platform Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BookOpen className="h-5 w-5 text-blue-600" />
                    <span>Total Posts</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-blue-600">{stats.total_posts}</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Star className="h-5 w-5 text-yellow-600" />
                    <span>Avg. Authenticity</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-yellow-600">{stats.average_authenticity_score}</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    <span>Personal Blogs</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-green-600">{stats.personal_blogs}</p>
                </CardContent>
              </Card>
            </div>

            {stats.top_domains && stats.top_domains.length > 0 && (
              <div className="mt-8">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Top Domains</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {stats.top_domains.map((domain, index) => (
                    <Card key={index}>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <span className="font-medium">{domain.domain}</span>
                          <Badge variant="secondary">{domain.count} posts</Badge>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </main>
    </div>
  )
}

export default App

