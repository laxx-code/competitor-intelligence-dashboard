from textblob import TextBlob
from typing import Dict, List
import re
from datetime import datetime

class SentimentAnalyzer:
    """Analyzes sentiment of text data"""
    
    def __init__(self):
        self.sentiment_history = []
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        if not text:
            return {
                "text": "",
                "polarity": 0,
                "subjectivity": 0,
                "sentiment": "neutral",
                "score": 0
            }
        
        blob = TextBlob(text)
        
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.3:
            sentiment = "positive"
        elif polarity < -0.3:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "text": text[:200],
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment,
            "score": polarity
        }
    
    def analyze_competitor_sentiment(self, competitor_data: Dict) -> Dict:
        """Analyze sentiment from competitor data"""
        sentiments = []
        
        # Analyze about text
        about = competitor_data.get('about', '')
        if about:
            sentiments.append(self.analyze_text(about))
        
        # Analyze services
        for service in competitor_data.get('services', [])[:5]:
            if service:
                sentiments.append(self.analyze_text(service))
        
        # Analyze company name for sentiment
        name = competitor_data.get('company_name', '')
        if name:
            sentiments.append(self.analyze_text(f"{name} is a great company"))
        
        # Calculate overall sentiment
        if sentiments:
            avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
            positive = sum(1 for s in sentiments if s['sentiment'] == 'positive')
            negative = sum(1 for s in sentiments if s['sentiment'] == 'negative')
            neutral = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
            
            return {
                "company": competitor_data.get('company_name', 'Unknown'),
                "average_polarity": avg_polarity,
                "positive_count": positive,
                "negative_count": negative,
                "neutral_count": neutral,
                "overall": "positive" if avg_polarity > 0.1 else "negative" if avg_polarity < -0.1 else "neutral",
                "sentiments": sentiments[:3]
            }
        
        return {
            "company": competitor_data.get('company_name', 'Unknown'),
            "average_polarity": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "overall": "neutral",
            "sentiments": []
        }
    
    def track_sentiment_over_time(self, company: str, new_data: Dict):
        """Track sentiment changes over time"""
        analysis = self.analyze_competitor_sentiment(new_data)
        self.sentiment_history.append({
            "company": company,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        })
        return analysis

# Global sentiment analyzer instance
sentiment_analyzer = SentimentAnalyzer()

# Test sentiment analyzer
print("✅ Sentiment analyzer initialized")
