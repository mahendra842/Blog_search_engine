import requests
from bs4 import BeautifulSoup
import feedparser
import time
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import logging

class BlogScraper:
    def __init__(self, delay=1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay  # Delay between requests to be respectful
        
    def scrape_blog_directory(self, directory_url, max_blogs=50):
        """
        Scrape a blog directory to get list of personal blogs
        """
        try:
            response = self.session.get(directory_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            blog_urls = []
            
            # Generic link extraction - look for links that might be blogs
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if self._is_likely_blog_url(href):
                    full_url = urljoin(directory_url, href)
                    if full_url not in blog_urls:
                        blog_urls.append(full_url)
                        
                if len(blog_urls) >= max_blogs:
                    break
                    
            return blog_urls
            
        except Exception as e:
            logging.error(f"Error scraping directory {directory_url}: {e}")
            return []
    
    def scrape_blog_post(self, url):
        """
        Scrape a single blog post and extract content
        """
        try:
            time.sleep(self.delay)  # Be respectful
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract content
            content = self._extract_content(soup)
            
            # Extract author
            author = self._extract_author(soup)
            
            # Extract published date
            published_date = self._extract_published_date(soup)
            
            # Extract blog name
            blog_name = self._extract_blog_name(soup)
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'author': author,
                'published_date': published_date,
                'blog_name': blog_name,
                'blog_domain': urlparse(url).netloc
            }
            
        except Exception as e:
            logging.error(f"Error scraping blog post {url}: {e}")
            return None
    
    def scrape_rss_feed(self, feed_url, max_posts=10):
        """
        Scrape RSS feed to get recent blog posts
        """
        try:
            feed = feedparser.parse(feed_url)
            posts = []
            
            for entry in feed.entries[:max_posts]:
                post_data = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'author': entry.get('author', ''),
                    'published_date': self._parse_feed_date(entry.get('published', '')),
                    'summary': entry.get('summary', ''),
                    'blog_name': feed.feed.get('title', ''),
                    'blog_domain': urlparse(entry.get('link', '')).netloc
                }
                
                # Get full content by scraping the post URL
                if post_data['url']:
                    full_post = self.scrape_blog_post(post_data['url'])
                    if full_post:
                        post_data['content'] = full_post['content']
                        posts.append(post_data)
                        
            return posts
            
        except Exception as e:
            logging.error(f"Error scraping RSS feed {feed_url}: {e}")
            return []
    
    def discover_rss_feeds(self, blog_url):
        """
        Try to discover RSS feeds for a blog
        """
        try:
            response = self.session.get(blog_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            feeds = []
            
            # Look for RSS/Atom feed links in HTML head
            feed_links = soup.find_all('link', {'type': ['application/rss+xml', 'application/atom+xml']})
            for link in feed_links:
                href = link.get('href')
                if href:
                    feed_url = urljoin(blog_url, href)
                    feeds.append(feed_url)
            
            # Common RSS feed paths
            common_paths = ['/feed', '/rss', '/feed.xml', '/rss.xml', '/atom.xml', '/index.xml']
            base_url = f"{urlparse(blog_url).scheme}://{urlparse(blog_url).netloc}"
            
            for path in common_paths:
                potential_feed = base_url + path
                if potential_feed not in feeds:
                    # Quick check if feed exists
                    try:
                        feed_response = self.session.head(potential_feed, timeout=5)
                        if feed_response.status_code == 200:
                            feeds.append(potential_feed)
                    except:
                        pass
            
            return feeds
            
        except Exception as e:
            logging.error(f"Error discovering RSS feeds for {blog_url}: {e}")
            return []
    
    def _is_likely_blog_url(self, url):
        """
        Heuristic to determine if a URL is likely a blog
        """
        if not url:
            return False
            
        # Skip obvious non-blog URLs
        skip_patterns = [
            'javascript:', 'mailto:', '#', 'tel:',
            '.pdf', '.jpg', '.png', '.gif', '.css', '.js',
            'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com'
        ]
        
        for pattern in skip_patterns:
            if pattern in url.lower():
                return False
        
        # Look for blog-like patterns
        blog_patterns = [
            'blog', 'post', 'article', 'diary', 'journal',
            '.com', '.net', '.org', '.io'
        ]
        
        return any(pattern in url.lower() for pattern in blog_patterns)
    
    def _extract_title(self, soup):
        """Extract title from HTML"""
        # Try multiple selectors
        selectors = [
            'h1.entry-title',
            'h1.post-title',
            'h1.article-title',
            'h1',
            '.entry-title',
            '.post-title',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "Untitled"
    
    def _extract_content(self, soup):
        """Extract main content from HTML"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.decompose()
        
        # Try multiple content selectors
        content_selectors = [
            '.entry-content',
            '.post-content',
            '.article-content',
            '.content',
            'article',
            '.post',
            '.entry',
            'main'
        ]
        
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                # Get text and clean it up
                text = content_element.get_text()
                # Clean up whitespace
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 100:  # Ensure we have substantial content
                    return text
        
        # Fallback: get all paragraph text
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return re.sub(r'\s+', ' ', content).strip()
    
    def _extract_author(self, soup):
        """Extract author from HTML"""
        author_selectors = [
            '.author',
            '.by-author',
            '.post-author',
            '.entry-author',
            '[rel="author"]',
            '.byline'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        # Look in meta tags
        meta_author = soup.find('meta', {'name': 'author'})
        if meta_author:
            return meta_author.get('content', '').strip()
        
        return ""
    
    def _extract_published_date(self, soup):
        """Extract published date from HTML"""
        # Look for time elements
        time_element = soup.find('time')
        if time_element:
            datetime_attr = time_element.get('datetime')
            if datetime_attr:
                try:
                    return datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                except:
                    pass
        
        # Look in meta tags
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="date"]',
            'meta[name="publish_date"]'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get('content')
                if content:
                    try:
                        return datetime.fromisoformat(content.replace('Z', '+00:00'))
                    except:
                        pass
        
        return None
    
    def _extract_blog_name(self, soup):
        """Extract blog name from HTML"""
        # Try site title
        title_element = soup.find('title')
        if title_element:
            title = title_element.get_text()
            # Often blog name is after a separator
            if ' | ' in title:
                return title.split(' | ')[-1].strip()
            elif ' - ' in title:
                return title.split(' - ')[-1].strip()
        
        # Look for site name in header
        site_selectors = [
            '.site-title',
            '.blog-title',
            '.site-name',
            'h1 a[rel="home"]'
        ]
        
        for selector in site_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return ""
    
    def _parse_feed_date(self, date_string):
        """Parse date from RSS feed"""
        if not date_string:
            return None
            
        try:
            # feedparser usually handles this, but let's be safe
            import email.utils
            timestamp = email.utils.parsedate_to_datetime(date_string)
            return timestamp
        except:
            return None

