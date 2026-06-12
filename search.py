from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(1000), unique=True, nullable=False)
    author = db.Column(db.String(200), nullable=True)
    published_date = db.Column(db.DateTime, nullable=True)
    scraped_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Authenticity scoring fields
    authenticity_score = db.Column(db.Float, default=0.0)
    ai_generated_probability = db.Column(db.Float, default=0.0)
    vocabulary_richness = db.Column(db.Float, default=0.0)
    sentence_complexity = db.Column(db.Float, default=0.0)
    
    # Blog metadata
    blog_domain = db.Column(db.String(200), nullable=True)
    blog_name = db.Column(db.String(200), nullable=True)
    is_personal_blog = db.Column(db.Boolean, default=True)
    
    # Search optimization
    keywords = db.Column(db.Text, nullable=True)  # Comma-separated keywords
    summary = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<BlogPost {self.title[:50]}...>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content[:500] + '...' if len(self.content) > 500 else self.content,
            'url': self.url,
            'author': self.author,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'scraped_date': self.scraped_date.isoformat() if self.scraped_date else None,
            'authenticity_score': self.authenticity_score,
            'ai_generated_probability': self.ai_generated_probability,
            'vocabulary_richness': self.vocabulary_richness,
            'sentence_complexity': self.sentence_complexity,
            'blog_domain': self.blog_domain,
            'blog_name': self.blog_name,
            'is_personal_blog': self.is_personal_blog,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'summary': self.summary
        }

    def to_search_result(self):
        """Simplified representation for search results"""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'author': self.author,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'authenticity_score': self.authenticity_score,
            'blog_domain': self.blog_domain,
            'blog_name': self.blog_name,
            'summary': self.summary,
            'keywords': self.keywords.split(',') if self.keywords else []
        }

