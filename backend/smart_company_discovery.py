"""
Smart Company Discovery Module
Visits websites, reads About/Services pages, validates company domain
"""

import re
import time
import json
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import tldextract
from duckduckgo_search import DDGS

class SmartCompanyDiscovery:
    """Intelligent company discovery with website validation"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.session.timeout = 10
        
        # Company keywords for validation
        self.service_keywords = {
            'software development': [
                'software', 'development', 'engineering', 'application', 'custom software',
                'web development', 'mobile development', 'product development'
            ],
            'digital marketing': [
                'digital marketing', 'seo', 'social media', 'content marketing',
                'ppc', 'google ads', 'facebook ads', 'marketing agency'
            ],
            'ai development': [
                'artificial intelligence', 'machine learning', 'deep learning',
                'ai', 'ml', 'computer vision', 'nlp', 'llm', 'chatbot'
            ],
            'web development': [
                'web development', 'website development', 'web design',
                'frontend', 'backend', 'full stack', 'react', 'angular'
            ],
            'mobile app development': [
                'mobile app', 'ios development', 'android development',
                'react native', 'flutter', 'hybrid app'
            ]
        }
        
        # Blacklist domains
        self.blacklist_domains = {
            'linkedin.com', 'clutch.co', 'goodfirms.co', 'justdial.com',
            'glassdoor.com', 'ambitionbox.com', 'indeed.com', 'crunchbase.com',
            'facebook.com', 'instagram.com', 'youtube.com', 'x.com', 'twitter.com',
            'github.com', 'angel.co', 'wellfound.com', 'upwork.com', 'freelancer.com',
            'fiverr.com', 'toptal.com', 'yelp.com', 'google.com', 'bing.com',
            'wikipedia.org', 'medium.com', 'quora.com', 'reddit.com',
            'stackoverflow.com', 'blogspot.com', 'wordpress.com',
            'thrillophilia.com', 'tripadvisor.com', 'makemytrip.com'
        }
        
        # Cache for visited pages
        self.page_cache = {}
    
    def discover(self, location: str, company_type: str) -> List[Dict]:
        """Main discovery method"""
        print(f"🔍 Smart discovering {company_type} companies in {location}")
        
        # Normalize company type
        company_type_key = company_type.lower().strip()
        
        # Step 1: Search for companies
        candidate_urls = self._search_candidates(location, company_type)
        print(f"📊 Found {len(candidate_urls)} candidate URLs")
        
        # Step 2: Remove duplicates and filter domains
        filtered_urls = self._filter_and_deduplicate(candidate_urls)
        print(f"✅ {len(filtered_urls)} unique valid domains")
        
        # Step 3: Visit and validate each website
        validated_companies = self._validate_companies(filtered_urls, company_type)
        print(f"🏢 Validated {len(validated_companies)} companies")
        
        # Step 4: Rank by relevance
        ranked_companies = self._rank_companies(validated_companies, company_type)
        print(f"📈 Ranked {len(ranked_companies)} companies")
        
        return ranked_companies[:20]
    
    def _search_candidates(self, location: str, company_type: str) -> Set[str]:
        """Search for candidate companies"""
        urls = set()
        location = location.strip()
        company_type = company_type.strip()
        
        # Generate search queries
        queries = [
            f'"{company_type}" companies "{location}"',
            f'"{company_type}" services "{location}"',
            f'"{company_type}" agency "{location}"',
            f'"{company_type}" firm "{location}"',
            f'"{company_type}" solutions "{location}"',
            f'Top {company_type} companies {location}',
            f'Best {company_type} companies {location}',
        ]
        
        for query in queries:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=15))
                    for result in results:
                        href = result.get('href')
                        if href:
                            clean_url = self._clean_url(href)
                            if clean_url and self._is_valid_domain(clean_url):
                                urls.add(clean_url)
                    time.sleep(0.3)
            except Exception as e:
                print(f"  Search error: {e}")
        
        return urls
    
    def _clean_url(self, url: str) -> Optional[str]:
        """Clean and normalize URL"""
        if not url:
            return None
        
        try:
            # Handle DuckDuckGo redirects
            if 'duckduckgo.com/l/' in url:
                import urllib.parse
                parsed = urlparse(url)
                if parsed.query:
                    query_params = urllib.parse.parse_qs(parsed.query)
                    if 'uddg' in query_params:
                        import base64
                        try:
                            decoded = base64.b64decode(query_params['uddg'][0]).decode('utf-8')
                            return self._clean_url(decoded)
                        except:
                            pass
                return None
            
            # Handle Google redirects
            if 'google.com/url' in url:
                import urllib.parse
                parsed = urlparse(url)
                query_params = urllib.parse.parse_qs(parsed.query)
                if 'q' in query_params:
                    return query_params['q'][0]
                return None
            
            parsed = urlparse(url)
            if not parsed.scheme:
                url = 'https://' + url
                parsed = urlparse(url)
            
            clean = f"{parsed.scheme}://{parsed.netloc}"
            return clean.rstrip('/')
            
        except:
            return None
    
    def _is_valid_domain(self, url: str) -> bool:
        """Check if domain is valid and not blacklisted"""
        if not url:
            return False
        
        try:
            extracted = tldextract.extract(url)
            domain = f"{extracted.domain}.{extracted.suffix}".lower()
            
            # Check blacklist
            for blacklisted in self.blacklist_domains:
                if blacklisted in domain or domain in blacklisted:
                    return False
            
            # Check if it's a valid domain
            if '.' not in domain or len(domain) < 4:
                return False
            
            return True
        except:
            return False
    
    def _filter_and_deduplicate(self, urls: Set[str]) -> List[str]:
        """Remove duplicates and filter domains"""
        seen = set()
        valid = []
        
        for url in urls:
            if not url:
                continue
            
            try:
                # Extract base domain
                extracted = tldextract.extract(url)
                domain = f"{extracted.domain}.{extracted.suffix}".lower()
                
                if domain in seen:
                    continue
                
                seen.add(domain)
                valid.append(url)
                
            except:
                continue
        
        return valid
    
    def _validate_companies(self, urls: List[str], company_type: str) -> List[Dict]:
        """Validate each company by visiting their website"""
        companies = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {
                executor.submit(self._validate_single_company, url, company_type): url
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    companies.append(result)
        
        return companies
    
    def _validate_single_company(self, url: str, company_type: str) -> Optional[Dict]:
        """Validate a single company website"""
        try:
            # Try to get homepage
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # Check if company_type exists in content
            company_type_lower = company_type.lower()
            type_keywords = self.service_keywords.get(company_type_lower, [company_type_lower])
            
            # Score the company
            score = 0
            matched_services = []
            
            # Check homepage for keywords
            for keyword in type_keywords:
                if keyword in text:
                    score += 2
                    matched_services.append(keyword)
            
            # Find and check About page
            about_score, about_services = self._check_page(url, 'about', type_keywords)
            score += about_score
            matched_services.extend(about_services)
            
            # Find and check Services page
            services_score, services_services = self._check_page(url, 'services', type_keywords)
            score += services_score
            matched_services.extend(services_services)
            
            # Find and check Solutions page
            solutions_score, solutions_services = self._check_page(url, 'solutions', type_keywords)
            score += solutions_score
            matched_services.extend(solutions_services)
            
            # If score is too low, skip
            if score < 3:
                return None
            
            # Extract company name
            company_name = self._extract_company_name(soup, url)
            
            # Calculate confidence based on score
            confidence = min(100, int(score * 8))
            
            return {
                'name': company_name,
                'website': url,
                'confidence': confidence,
                'matched_services': list(set(matched_services))[:10]
            }
            
        except Exception as e:
            print(f"  Error validating {url}: {e}")
            return None
    
    def _check_page(self, base_url: str, page_type: str, keywords: List[str]) -> tuple:
        """Check a specific page type (about, services, solutions)"""
        page_urls = [
            urljoin(base_url, f'/{page_type}'),
            urljoin(base_url, f'/{page_type}s'),
            urljoin(base_url, f'/{page_type}-page'),
            urljoin(base_url, f'/{page_type}.html'),
        ]
        
        score = 0
        matched = []
        
        for url in page_urls:
            try:
                response = self.session.get(url, timeout=8)
                if response.status_code == 200:
                    text = response.text.lower()
                    for keyword in keywords:
                        if keyword in text:
                            score += 3
                            matched.append(keyword)
                    break
            except:
                continue
        
        return score, matched
    
    def _extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name from website"""
        # Try og:site_name
        og_site = soup.find('meta', property='og:site_name')
        if og_site and og_site.get('content'):
            name = og_site['content'].strip()
            if len(name) > 2 and len(name) < 80:
                return name
        
        # Try title
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            # Split by common separators
            for sep in ['|', '–', '—', '·', '•', '-']:
                if sep in title:
                    parts = title.split(sep)
                    for part in parts:
                        part = part.strip()
                        if len(part) > 2 and len(part) < 60:
                            return self._clean_company_name(part)
        
        # Try h1
        h1 = soup.find('h1')
        if h1:
            text = h1.get_text().strip()
            if len(text) > 2 and len(text) < 60:
                return self._clean_company_name(text)
        
        # Fallback to domain
        extracted = tldextract.extract(url)
        return extracted.domain.capitalize()
    
    def _clean_company_name(self, name: str) -> str:
        """Clean company name"""
        if not name:
            return None
        
        # Remove common suffixes
        suffixes = [
            r'\s*(Inc|Corp|Corporation|LLC|LLP|Ltd|Limited|Pvt|Private)\s*$',
            r'\s*(Technologies|Technology|Solutions|Services|Company|Agency|Firm|Digital)\s*$'
        ]
        
        for pattern in suffixes:
            name = re.sub(pattern, '', name, flags=re.I)
        
        name = name.strip()
        
        if len(name) > 2 and len(name) < 60:
            return name
        
        return None
    
    def _rank_companies(self, companies: List[Dict], company_type: str) -> List[Dict]:
        """Rank companies by relevance"""
        company_type_lower = company_type.lower()
        type_keywords = self.service_keywords.get(company_type_lower, [company_type_lower])
        
        for company in companies:
            # Boost score based on matched services
            matched_count = len(company.get('matched_services', []))
            company['confidence'] = min(100, company['confidence'] + matched_count * 2)
            
            # Boost if company name is relevant
            name = company.get('name', '').lower()
            if any(kw in name for kw in type_keywords):
                company['confidence'] += 10
        
        # Sort by confidence
        companies.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        return companies

# Create instance
smart_discovery = SmartCompanyDiscovery()
