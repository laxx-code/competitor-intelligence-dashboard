from .base_agent import BaseAgent
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
import re
import asyncio
import json
from datetime import datetime

class ScraperAgent(BaseAgent):
    def __init__(self):
        super().__init__("ScraperAgent")
    
    async def process(self, input_data: Dict) -> Dict:
        urls = input_data.get("urls", [])
        self.log(f"Scraping {len(urls)} tech companies")
        
        results = []
        for url in urls:
            try:
                data = await self._scrape_tech_company(url)
                results.append({"url": url, "data": data, "status": "success"})
                await asyncio.sleep(1)
            except Exception as e:
                self.log(f"Error scraping {url}: {str(e)}")
                results.append({"url": url, "error": str(e), "status": "failed"})
        
        return {"scraped_data": results, "total": len(results)}
    
    async def _scrape_tech_company(self, url: str) -> Dict:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            
            # Extract data
            data = {
                "company_name": self._extract_company_name(url, soup),
                "page_title": soup.title.string if soup.title else None,
                "meta_description": self._get_meta_description(soup),
                "scraped_at": datetime.now().isoformat(),
                "features": self._extract_features(soup),
                "tech_stack": self._extract_tech_stack(text),
                "company_size": self._extract_company_size(text),
                "founded_year": self._extract_founded_year(text),
                "headquarters": self._extract_headquarters(text),
                "industry": self._extract_industry(text),
                "pricing": self._extract_pricing(text),
                "social_links": self._extract_social_links(soup)
            }
            
            return data
            
        except Exception as e:
            raise Exception(f"Scraping failed: {str(e)}")
    
    def _extract_company_name(self, url: str, soup: BeautifulSoup) -> str:
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if domain_match:
            name = domain_match.group(1).split('.')[0]
            return name.capitalize()
        return "Unknown"
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find("meta", attrs={"name": "description"})
        return meta.get("content") if meta else None
    
    def _extract_features(self, soup: BeautifulSoup) -> List[str]:
        features = []
        feature_sections = soup.find_all(['ul', 'ol', 'div'], 
                                       class_=re.compile(r'feature|benefit|capability', re.I))
        
        for section in feature_sections:
            items = section.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if len(text) > 5 and len(text) < 200:
                    features.append(text)
        
        # Also look for feature mentions in paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if any(word in text.lower() for word in ['feature', 'include', 'offer']):
                if len(text) > 10 and len(text) < 300:
                    features.append(text)
        
        return list(set(features))[:15]
    
    def _extract_tech_stack(self, text: str) -> List[str]:
        tech_stack = []
        tech_keywords = [
            'python', 'javascript', 'react', 'angular', 'vue', 'node', 'django',
            'flask', 'rails', 'java', 'go', 'rust', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'tensorflow', 'pytorch', 'mongodb', 'postgres',
            'mysql', 'redis', 'elasticsearch', 'kafka', 'spark'
        ]
        
        for tech in tech_keywords:
            if tech in text.lower():
                tech_stack.append(tech)
        
        return list(set(tech_stack))[:10]
    
    def _extract_company_size(self, text: str) -> Dict:
        size = {"category": None, "employees": None}
        
        patterns = [
            r'(\d+)\+?\s*(?:employees|staff|people)',
            r'team\s+of\s+(\d+)',
            r'(\d+)\s*(?:employees|staff)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    size["employees"] = int(matches[0])
                    if size["employees"] < 50:
                        size["category"] = "Startup"
                    elif size["employees"] < 200:
                        size["category"] = "Small Business"
                    elif size["employees"] < 1000:
                        size["category"] = "Medium Business"
                    else:
                        size["category"] = "Enterprise"
                    break
                except:
                    pass
        
        if not size["category"]:
            if "startup" in text.lower():
                size["category"] = "Startup"
            elif "enterprise" in text.lower():
                size["category"] = "Enterprise"
            else:
                size["category"] = "Unknown"
        
        return size
    
    def _extract_founded_year(self, text: str) -> str:
        patterns = [
            r'(?:founded|established|since)\s+(\d{4})',
            r'(\d{4})\s*(?:founded|established)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                year = matches[0]
                if 1900 <= int(year) <= 2025:
                    return year
        
        return "Unknown"
    
    def _extract_headquarters(self, text: str) -> Dict:
        location = {"city": None, "state": None, "country": None}
        
        patterns = [
            r'(?:headquarters|based in|located in|office)\s+([^.\n,]+)',
            r'([A-Z][a-z]+,\s*[A-Z]{2})',
            r'([A-Z][a-z]+,\s*[A-Z][a-z]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                loc = matches[0].strip()
                parts = loc.split(',')
                if len(parts) == 2:
                    location["city"] = parts[0].strip()
                    location["state"] = parts[1].strip()
                else:
                    location["city"] = loc
                break
        
        return location
    
    def _extract_industry(self, text: str) -> List[str]:
        industries = []
        tech_industries = [
            'ai', 'artificial intelligence', 'machine learning', 'data science',
            'saas', 'software', 'cloud', 'devops', 'security', 'cybersecurity',
            'fintech', 'healthtech', 'edtech', 'e-commerce', 'analytics'
        ]
        
        for industry in tech_industries:
            if industry in text.lower():
                industries.append(industry)
        
        return list(set(industries))[:5]
    
    def _extract_pricing(self, text: str) -> Dict:
        pricing = {
            "starting_price": None,
            "free_tier": False,
            "currency": "USD"
        }
        
        patterns = [
            r'\$(\d+\.?\d*)\s*(?:per|/)\s*(?:month|year)',
            r'(?:starting|from|beginning)\s+at\s+\$?(\d+\.?\d*)',
            r'price\s*[:\s]+\$?(\d+\.?\d*)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                price = float(matches[0])
                if not pricing["starting_price"] or price < pricing["starting_price"]:
                    pricing["starting_price"] = price
        
        if 'free' in text.lower():
            pricing["free_tier"] = True
        
        return pricing
    
    def _extract_social_links(self, soup: BeautifulSoup) -> Dict:
        links = {
            "linkedin": None,
            "twitter": None,
            "github": None,
            "youtube": None
        }
        
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            if 'linkedin.com' in href and not links["linkedin"]:
                links["linkedin"] = href
            elif 'twitter.com' in href and not links["twitter"]:
                links["twitter"] = href
            elif 'github.com' in href and not links["github"]:
                links["github"] = href
            elif 'youtube.com' in href and not links["youtube"]:
                links["youtube"] = href
        
        return links
