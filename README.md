# Personal Blog Search Engine

## Project Overview

A custom search engine that surfaces deep-dive personal blogs and insightful articles, filtering out generic SEO-filled content to provide authentic voices and meaningful content.

## Problem Statement

Most search results today are dominated by corporate websites and SEO-optimized content that lacks authenticity and personal insight. This search engine addresses that by:

- Prioritizing personal blogs and authentic voices
- Using AI-powered authenticity scoring to filter content
- Providing a clean, modern interface focused on discovery
- Surfacing high-quality, thoughtful content over generic advice

## Features

### Core Functionality
- **Smart Search**: Semantic search across curated personal blog content
- **Authenticity Scoring**: AI-powered scoring system (0.0-1.0) that evaluates:
  - Content originality and depth
  - Personal voice and authenticity
  - Vocabulary richness and complexity
  - AI-generated content detection
- **Advanced Filtering**: Sort by relevance, authenticity score, or publication date
- **Quality Threshold**: Configurable minimum authenticity score filtering

### User Interface
- **Modern Design**: Clean, responsive interface with smooth animations
- **Search Results**: Rich cards showing title, summary, author, domain, and authenticity score
- **Statistics Dashboard**: Platform overview with total posts, average authenticity, and top domains
- **External Links**: Direct links to original blog posts
- **Mobile Responsive**: Optimized for both desktop and mobile devices

### Technical Features
- **Web Scraping**: Automated content discovery from RSS feeds and blog directories
- **Content Analysis**: NLP-powered analysis using spaCy and NLTK
- **RESTful API**: Clean API endpoints for search, statistics, and content management
- **Database**: SQLite database with efficient indexing and search capabilities

## Architecture

### Backend (Flask)
- **API Server**: Flask-based REST API with CORS support
- **Database**: SQLAlchemy ORM with SQLite database
- **Content Analysis**: spaCy and NLTK for natural language processing
- **Web Scraping**: BeautifulSoup and feedparser for content extraction

### Frontend (React)
- **UI Framework**: React with Vite build system
- **Styling**: Tailwind CSS with shadcn/ui components
- **Animations**: Framer Motion for smooth interactions
- **Icons**: Lucide React icon library

### Content Sources
Currently indexed sources:
- **manassaloi.com**: Personal blog by Manas Saloi (Product Management insights)
- **waitbutwhy.com**: Tim Urban's deep-dive articles on various topics

## Deployment URLs

### Production Deployment
- **Frontend**: https://searchenginegdsc-1.onrender.com/
- **Backend API**: https://searchenginegdsc.onrender.com/

### API Endpoints
- `GET /api/search?q={query}&sort={sort}&min_authenticity={score}` - Search for content
- `GET /api/stats` - Get platform statistics
- `POST /api/posts` - Add new blog post to index
- `GET /api/posts/{id}` - Get specific post details




## Project Structure

```
personal-blog-search-engine/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── models/
│   │   ├── blog_post.py       # Blog post database model
│   │   └── user.py            # User model (template)
│   ├── routes/
│   │   ├── search.py          # Search API endpoints
│   │   └── user.py            # User routes (template)
│   ├── content_analyzer.py    # Content authenticity analysis
│   ├── blog_scraper.py        # Web scraping functionality
│   └── indexer.py             # Automated content indexing
├── requirements.txt           # Python dependencies
└── database.db              # SQLite database

personal-blog-search-frontend/
├── src/
│   ├── App.jsx               # Main React application
│   ├── App.css               # Application styles
│   └── components/ui/        # UI components (shadcn/ui)
├── dist/                     # Production build output
├── package.json              # Node.js dependencies
└── index.html               # HTML entry point
```

## Content Analysis Metrics

### Authenticity Score Components
1. **Vocabulary Richness** (0.0-1.0): Unique word ratio and lexical diversity
2. **Sentence Complexity** (0.0-1.0): Average sentence length and structure variety
3. **Personal Voice Detection** (0.0-1.0): First-person pronouns and personal experiences
4. **Content Depth** (0.0-1.0): Article length and substantive content ratio
5. **AI Detection** (0.0-1.0): Probability of AI-generated content (inverted)


### Search Performance
- Fast semantic search with SQLite FTS
- Real-time filtering and sorting
- Efficient pagination for large result sets
- Responsive UI with smooth animations


## Contributing

To add new blog sources:
1. Update `blog_scraper.py` with new RSS feeds or scraping logic
2. Run the indexer to process new content
3. Test search functionality with new content

To improve authenticity scoring:
1. Modify `content_analyzer.py` algorithms
2. Adjust scoring weights and thresholds
3. Re-run analysis on existing content


