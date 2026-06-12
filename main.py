import re
import nltk
import spacy
from textstat import flesch_reading_ease, flesch_kincaid_grade, automated_readability_index
from collections import Counter
from urllib.parse import urlparse
import math

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model (using small English model)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

class ContentAnalyzer:
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        
    def analyze_content(self, title, content, url, author=None):
        """
        Analyze content and return authenticity scores
        """
        analysis = {
            'authenticity_score': 0.0,
            'ai_generated_probability': 0.0,
            'vocabulary_richness': 0.0,
            'sentence_complexity': 0.0,
            'is_personal_blog': False,
            'blog_domain': self._extract_domain(url),
            'keywords': self._extract_keywords(title + " " + content),
            'summary': self._generate_summary(content)
        }
        
        # Calculate individual metrics
        analysis['vocabulary_richness'] = self._calculate_vocabulary_richness(content)
        analysis['sentence_complexity'] = self._calculate_sentence_complexity(content)
        analysis['ai_generated_probability'] = self._estimate_ai_probability(content)
        analysis['is_personal_blog'] = self._is_personal_blog(url, author, content)
        
        # Calculate overall authenticity score
        analysis['authenticity_score'] = self._calculate_authenticity_score(
            analysis['vocabulary_richness'],
            analysis['sentence_complexity'],
            analysis['ai_generated_probability'],
            analysis['is_personal_blog'],
            content,
            url
        )
        
        return analysis
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        try:
            return urlparse(url).netloc.lower()
        except:
            return ""
    
    def _calculate_vocabulary_richness(self, text):
        """Calculate vocabulary richness using Type-Token Ratio"""
        if not text:
            return 0.0
            
        words = re.findall(r'\b\w+\b', text.lower())
        if len(words) < 10:
            return 0.0
            
        unique_words = set(words)
        # Filter out stop words for better measure
        content_words = [w for w in unique_words if w not in self.stop_words and len(w) > 2]
        
        if len(words) == 0:
            return 0.0
            
        # Modified TTR to account for text length
        ttr = len(content_words) / len(words)
        # Normalize to 0-1 scale
        return min(ttr * 2, 1.0)
    
    def _calculate_sentence_complexity(self, text):
        """Calculate sentence complexity using readability metrics"""
        if not text or len(text) < 50:
            return 0.0
            
        try:
            # Use multiple readability metrics
            flesch_score = flesch_reading_ease(text)
            fk_grade = flesch_kincaid_grade(text)
            ari_score = automated_readability_index(text)
            
            # Normalize scores (higher complexity = higher score)
            # Flesch: 0-100 (higher = easier), we want inverse
            flesch_complexity = max(0, (100 - flesch_score) / 100)
            
            # FK Grade: typically 1-18+ (higher = more complex)
            fk_complexity = min(fk_grade / 18, 1.0)
            
            # ARI: similar to FK Grade
            ari_complexity = min(ari_score / 18, 1.0)
            
            # Average the metrics
            complexity = (flesch_complexity + fk_complexity + ari_complexity) / 3
            return min(max(complexity, 0.0), 1.0)
            
        except:
            return 0.5  # Default moderate complexity
    
    def _estimate_ai_probability(self, text):
        """Estimate probability that text is AI-generated"""
        if not text:
            return 0.0
            
        ai_indicators = 0
        total_checks = 0
        
        # Check for repetitive patterns
        sentences = nltk.sent_tokenize(text)
        if len(sentences) > 3:
            total_checks += 1
            sentence_starts = [s.split()[:3] for s in sentences if len(s.split()) >= 3]
            start_counter = Counter([' '.join(start) for start in sentence_starts])
            if max(start_counter.values()) > len(sentences) * 0.3:
                ai_indicators += 1
        
        # Check for overly formal language patterns
        total_checks += 1
        formal_phrases = [
            "it is important to note", "furthermore", "moreover", "in conclusion",
            "it should be noted", "as previously mentioned", "in summary"
        ]
        formal_count = sum(1 for phrase in formal_phrases if phrase in text.lower())
        if formal_count > len(sentences) * 0.1:
            ai_indicators += 1
        
        # Check for lack of personal pronouns (in personal blogs)
        total_checks += 1
        personal_pronouns = len(re.findall(r'\b(I|me|my|mine|myself)\b', text, re.IGNORECASE))
        word_count = len(text.split())
        if word_count > 100 and personal_pronouns / word_count < 0.01:
            ai_indicators += 1
        
        # Check for perfect grammar (unusual in personal blogs)
        total_checks += 1
        # Simple heuristic: look for contractions and informal language
        contractions = len(re.findall(r"\w+'[a-z]", text))
        if word_count > 100 and contractions / word_count < 0.005:
            ai_indicators += 1
        
        return ai_indicators / total_checks if total_checks > 0 else 0.0
    
    def _is_personal_blog(self, url, author, content):
        """Determine if this is likely a personal blog"""
        domain = self._extract_domain(url)
        
        # Check domain patterns
        personal_indicators = 0
        total_checks = 0
        
        # Domain-based checks
        total_checks += 1
        if any(pattern in domain for pattern in ['.com', '.net', '.org']) and not any(corp in domain for corp in ['corp', 'inc', 'company', 'business']):
            personal_indicators += 1
        
        # Author name in domain
        if author:
            total_checks += 1
            author_parts = author.lower().split()
            if any(part in domain for part in author_parts if len(part) > 2):
                personal_indicators += 1
        
        # Content-based checks
        total_checks += 1
        personal_pronouns = len(re.findall(r'\b(I|me|my|mine|myself|we|us|our)\b', content, re.IGNORECASE))
        word_count = len(content.split())
        if word_count > 50 and personal_pronouns / word_count > 0.02:
            personal_indicators += 1
        
        # Check for personal story indicators
        total_checks += 1
        story_indicators = ['my experience', 'my journey', 'I learned', 'I discovered', 'my story', 'personal']
        if any(indicator in content.lower() for indicator in story_indicators):
            personal_indicators += 1
        
        return personal_indicators / total_checks > 0.5
    
    def _calculate_authenticity_score(self, vocab_richness, sentence_complexity, ai_probability, is_personal, content, url):
        """Calculate overall authenticity score"""
        score = 0.0
        
        # Vocabulary richness (25% weight)
        score += vocab_richness * 0.25
        
        # Sentence complexity - moderate complexity is good (25% weight)
        # Peak at 0.6 complexity, decline after
        complexity_score = 1.0 - abs(sentence_complexity - 0.6) / 0.6
        score += complexity_score * 0.25
        
        # AI probability - lower is better (30% weight)
        score += (1.0 - ai_probability) * 0.30
        
        # Personal blog bonus (20% weight)
        if is_personal:
            score += 0.20
        
        # Content length bonus/penalty
        word_count = len(content.split())
        if word_count > 300:  # Substantial content
            score += 0.1
        elif word_count < 100:  # Too short
            score -= 0.1
        
        # Domain reputation (simple heuristic)
        domain = self._extract_domain(url)
        if any(corp in domain for corp in ['medium.com', 'substack.com', 'wordpress.com', 'blogspot.com']):
            score += 0.05  # Slight bonus for known blogging platforms
        
        return min(max(score, 0.0), 1.0)
    
    def _extract_keywords(self, text, max_keywords=10):
        """Extract keywords from text"""
        if not text:
            return ""
            
        # Simple keyword extraction using word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 3]
        
        word_freq = Counter(words)
        keywords = [word for word, freq in word_freq.most_common(max_keywords)]
        
        return ','.join(keywords)
    
    def _generate_summary(self, content, max_length=200):
        """Generate a simple summary of the content"""
        if not content:
            return ""
            
        sentences = nltk.sent_tokenize(content)
        if len(sentences) <= 2:
            return content[:max_length]
        
        # Take first two sentences as summary
        summary = '. '.join(sentences[:2])
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
            
        return summary

