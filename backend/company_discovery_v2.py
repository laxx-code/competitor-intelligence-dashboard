"""
Company Discovery Module - Fixed Scoring
Lower threshold, better validation
"""

import re
import time
import random
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import tldextract
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompanyDiscoveryV2:
    def __init__(self):
        self.blacklist_domains = {
            'linkedin.com', 'clutch.co', 'goodfirms.co', 'justdial.com',
            'glassdoor.com', 'ambitionbox.com', 'indeed.com', 'crunchbase.com',
            'facebook.com', 'instagram.com', 'youtube.com', 'twitter.com',
            'github.com', 'angel.co', 'upwork.com', 'freelancer.com',
            'fiverr.com', 'toptal.com', 'yelp.com', 'wikipedia.org',
            'medium.com', 'quora.com', 'reddit.com', 'stackoverflow.com',
            'indiamart.com', 'tradeindia.com', 'f6s.com', 'yourstory.com',
            'inc42.com', 'vccircle.com', 'moneycontrol.com',
            'blogspot.com', 'wordpress.com'
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.session.timeout = 10
        
        self.tech_keywords = [
            'Python', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Node.js',
            'Django', 'Flask', 'Java', 'AWS', 'Azure', 'GCP',
            'Docker', 'Kubernetes', 'TensorFlow', 'PyTorch',
            'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Git'
        ]
    
    def discover(self, location: str, company_type: str) -> List[Dict]:
        """Main discovery method"""
        logger.info(f"🔍 Searching for {company_type} companies in {location}")
        
        # Search
        urls = self._search_all(location, company_type)
        logger.info(f"🌐 Found {len(urls)} unique URLs")
        
        if not urls:
            return []
        
        # Filter
        valid_urls = self._filter_urls(urls)
        logger.info(f"✅ {len(valid_urls)} valid domains")
        
        if not valid_urls:
            return []
        
        # Scrape and validate
        companies = self._scrape_companies(valid_urls, location, company_type)
        logger.info(f"🏢 Found {len(companies)} companies")
        
        # Sort by score
        companies.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Return top 20 (even if score is low)
        return companies[:20]
    
    def _search_all(self, location: str, company_type: str) -> Set[str]:
        """Search multiple sources"""
        urls = set()
        main_city = location.split(',')[0].strip()
        
        # DuckDuckGo
        queries = [
            f'"{company_type}" companies "{main_city}"',
            f'{company_type} companies {main_city}',
            f'best {company_type} companies {main_city}',
            f'top {company_type} companies {main_city}',
            f'"{company_type}" {main_city}',
            f'"{company_type}" agency {main_city}',
        ]
        
        for query in queries:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=8))
                    for result in results:
                        href = result.get('href')
                        if href:
                            clean = self._clean_url(href)
                            if clean:
                                urls.add(clean)
                    time.sleep(0.3)
            except:
                continue
        
        return urls
    
    def _clean_url(self, url: str) -> Optional[str]:
        if not url:
            return None
        
        try:
            if 'duckduckgo.com/l/' in url:
                import urllib.parse
                parsed = urlparse(url)
                if parsed.query:
                    params = urllib.parse.parse_qs(parsed.query)
                    if 'uddg' in params:
                        import base64
                        try:
                            decoded = base64.b64decode(params['uddg'][0]).decode('utf-8')
                            return self._clean_url(decoded)
                        except:
                            pass
                return None
            
            if 'google.com/url' in url:
                import urllib.parse
                parsed = urlparse(url)
                params = urllib.parse.parse_qs(parsed.query)
                if 'q' in params:
                    return params['q'][0]
                return None
            
            parsed = urlparse(url)
            if not parsed.scheme:
                url = 'https://' + url
                parsed = urlparse(url)
            
            return f"{parsed.scheme}://{parsed.netloc}".rstrip('/')
            
        except:
            return None
    
    def _filter_urls(self, urls: Set[str]) -> List[str]:
        valid = []
        for url in urls:
            if not url:
                continue
            try:
                ext = tldextract.extract(url)
                domain = f"{ext.domain}.{ext.suffix}".lower()
                
                if any(b in domain for b in self.blacklist_domains):
                    continue
                
                valid_tlds = ['.com', '.in', '.io', '.org', '.net', '.co', '.ai', '.tech', '.dev']
                if not any(domain.endswith(tld) for tld in valid_tlds):
                    continue
                
                valid.append(url)
                
            except:
                continue
        
        return valid
    
    def _scrape_companies(self, urls: List[str], location: str, company_type: str) -> List[Dict]:
        companies = []
        keywords = self._get_keywords(company_type)
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {
                executor.submit(self._scrape_one, url, location, keywords): url 
                for url in urls
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    companies.append(result)
        
        return companies
    
    def _get_keywords(self, company_type: str) -> List[str]:
        company_lower = company_type.lower()
        keywords = [company_lower]
        
        if 'ai' in company_lower:
            keywords.extend(['ai', 'artificial intelligence', 'machine learning'])
        if 'software' in company_lower:
            keywords.extend(['software', 'development'])
        if 'digital' in company_lower:
            keywords.extend(['digital', 'marketing', 'seo'])
        if 'web' in company_lower:
            keywords.extend(['web', 'development', 'design'])
        if 'mobile' in company_lower:
            keywords.extend(['mobile', 'app', 'ios', 'android'])
        
        return keywords
    
    def _scrape_one(self, url: str, location: str, keywords: List[str]) -> Optional[Dict]:
        try:
            response = self.session.get(url, timeout=8)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # Check if it's a company
            if not self._is_company(text):
                return None
            
            # Get name
            name = self._get_name(soup, url)
            if not name or len(name) < 3:
                return None
            
            # Get services
            services = self._get_services(soup, text, keywords)
            
            # Get tech
            tech = self._get_tech(text)
            
            # Calculate score - more lenient
            score = self._calculate_score(text, location, keywords, services, tech)
            
            return {
                'name': name,
                'website': url,
                'location': self._get_location(text),
                'services': services[:8],
                'technologies': tech[:8],
                'industries': self._get_industries(text),
                'clients': self._get_clients(text),
                'score': score
            }
            
        except Exception as e:
            return None
    
    def _is_company(self, text: str) -> bool:
        indicators = ['about', 'contact', 'services', 'team', 'portfolio']
        count = sum(1 for ind in indicators if ind in text)
        return count >= 1  # Lowered from 2 to 1
    
    def _get_name(self, soup: BeautifulSoup, url: str) -> str:
        og = soup.find('meta', property='og:site_name')
        if og and og.get('content'):
            return og['content'].strip()[:60]
        
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            for sep in ['|', '–', '—', '-']:
                if sep in title:
                    parts = title.split(sep)
                    for part in parts:
                        part = part.strip()
                        if len(part) > 2 and len(part) < 60:
                            return part
        
        ext = tldextract.extract(url)
        return ext.domain.capitalize()
    
    def _get_services(self, soup: BeautifulSoup, text: str, keywords: List[str]) -> List[str]:
        services = []
        
        # Look for service sections
        service_sections = soup.find_all(['div', 'section', 'ul'], 
                                        class_=re.compile(r'service|solution|offer|expertise', re.I))
        
        for section in service_sections:
            items = section.find_all(['h2', 'h3', 'h4', 'h5', 'li', 'strong'])
            for item in items:
                item_text = item.get_text(strip=True)
                if 5 < len(item_text) < 80:
                    # Check if it matches keywords or is a service name
                    if any(kw in item_text.lower() for kw in keywords) or 'development' in item_text.lower():
                        services.append(item_text)
        
        # If no services found, extract from text
        if not services:
            for keyword in keywords:
                pattern = rf'[^.]*{keyword}[^.]*\.'
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches[:2]:
                    clean = match.strip()
                    if 10 < len(clean) < 100:
                        services.append(clean)
        
        # Clean and deduplicate
        seen = set()
        cleaned = []
        for s in services:
            s = re.sub(r'^\d+\.\s*', '', s)
            s = s.strip()
            if s and s not in seen and len(s) < 60:
                seen.add(s)
                cleaned.append(s)
        
        return cleaned
    
    def _get_tech(self, text: str) -> List[str]:
        tech = []
        for t in self.tech_keywords:
            if t.lower() in text:
                tech.append(t)
        return tech
    
    def _get_location(self, text: str) -> str:
        patterns = [
            r'(?:based in|located in|headquarters|office)\s+([^.\n,]+)',
            r'([A-Z][a-z]+,\s*[A-Z]{2})'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        return ""
    
    def _get_clients(self, text: str) -> List[str]:
        clients = []
        patterns = [
            r'(?:clients|customers|partners)\s+include\s+([^.\n]+)',
            r'trusted by\s+([^.\n]+)'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                names = [n.strip() for n in match.split(',') if len(n.strip()) > 3]
                clients.extend(names[:5])
        return clients
    
    def _get_industries(self, text: str) -> List[str]:
        industries = []
        industry_list = [
            'AI', 'Machine Learning', 'Data Science', 'SaaS', 'Cloud Computing',
            'Cybersecurity', 'Fintech', 'Healthtech', 'Edtech', 'E-commerce',
            'Analytics', 'Automation', 'IoT', 'Blockchain'
        ]
        for industry in industry_list:
            if industry.lower() in text:
                industries.append(industry)
        return industries
    
    def _calculate_score(self, text: str, location: str, keywords: List[str], 
                        services: List[str], tech: List[str]) -> int:
        """Calculate score - more lenient"""
        score = 10  # Base score
        
        # Location match
        location_parts = location.lower().split()
        location_matches = sum(1 for part in location_parts if part in text)
        score += min(15, location_matches * 3)
        
        # Keyword matches
        keyword_matches = sum(1 for kw in keywords if kw in text)
        score += min(25, keyword_matches * 2)
        
        # Services found
        score += len(services) * 2
        
        # Technologies found
        score += len(tech) * 1
        
        # Company indicators
        indicators = ['about', 'contact', 'services', 'team']
        indicator_count = sum(1 for ind in indicators if ind in text)
        score += indicator_count * 2
        
        return min(100, score)

# Create instance
company_discovery = CompanyDiscoveryV2()
