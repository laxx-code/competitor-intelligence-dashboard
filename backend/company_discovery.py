import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import time
from typing import List, Dict, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

class CompanyDiscovery:
    def __init__(self):
        self.blacklist_domains = {
            'linkedin.com', 'clutch.co', 'goodfirms.co', 'justdial.com',
            'glassdoor.com', 'ambitionbox.com', 'indeed.com', 'crunchbase.com',
            'facebook.com', 'instagram.com', 'youtube.com', 'x.com', 'twitter.com',
            'github.com', 'angel.co', 'wellfound.com', 'upwork.com', 'freelancer.com',
            'fiverr.com', 'toptal.com', 'yelp.com', 'google.com',
            'geeksforgeeks.org', 'tutorialspoint.com', 'simplilearn.com',
            'coursera.org', 'udemy.com', 'w3schools.com', 'javatpoint.com',
            'dictionary.cambridge.org', 'oxfordlearnersdictionaries.com',
            'zhihu.com', 'baidu.com', 'csdn.net', 'gaana.com', 'jiosaavn.com',
            'amazon.com', 'amazon.in', 'flipkart.com', 'myntra.com',
            'microsoft.com', 'oracle.com', 'ibm.com', 'cisco.com',
            'medium.com', 'quora.com', 'reddit.com', 'stackoverflow.com',
            'wikipedia.org', 'techcrunch.com', 'theverge.com',
            'zomato.com', 'swiggy.com', 'oyorooms.com'
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.max_results_per_query = 10
        
    def discover_companies(self, location: str, company_type: str) -> List[Dict]:
        if not location or not company_type:
            return []
        
        print(f"🔍 Searching for {company_type} companies in {location}...")
        
        search_queries = self._generate_search_queries(location, company_type)
        all_urls = set()
        
        for query in search_queries:
            urls = self._search_duckduckgo(query)
            all_urls.update(urls)
            time.sleep(0.3)
        
        print(f"🌐 Found {len(all_urls)} unique URLs")
        
        if not all_urls:
            return []
        
        valid_urls = self._filter_valid_domains(all_urls)
        print(f"✅ {len(valid_urls)} valid domains")
        
        if not valid_urls:
            return []
        
        companies = self._validate_and_extract_companies(valid_urls)
        print(f"🏢 Verified {len(companies)} companies")
        
        return companies
    
    def _generate_search_queries(self, location: str, company_type: str) -> List[str]:
        location = location.strip()
        company_type = company_type.strip()
        main_keyword = company_type.split()[0] if company_type.split() else company_type
        
        return [
            f'"{main_keyword}" company "{location}"',
            f'"{company_type}" companies "{location}"',
            f'"{company_type}" services "{location}"',
            f'top "{company_type}" companies "{location}"',
            f'best "{company_type}" companies "{location}"',
            f'"{location}" "{company_type}" companies',
            f'"{company_type}" agency "{location}"',
        ]
    
    def _search_duckduckgo(self, query: str) -> Set[str]:
        urls = set()
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results_per_query))
                for result in results:
                    href = result.get('href')
                    if href:
                        clean_url = self._clean_url(href)
                        if clean_url:
                            urls.add(clean_url)
        except Exception as e:
            print(f"  Search error: {e}")
        return urls
    
    def _clean_url(self, url: str) -> str:
        if not url:
            return None
        
        try:
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
            
        except Exception:
            return None
    
    def _filter_valid_domains(self, urls: Set[str]) -> List[str]:
        valid = []
        for url in urls:
            if not url:
                continue
            
            try:
                extracted = tldextract.extract(url)
                domain = f"{extracted.domain}.{extracted.suffix}".lower()
                
                is_blacklisted = False
                for blacklisted in self.blacklist_domains:
                    if blacklisted in domain or domain in blacklisted:
                        is_blacklisted = True
                        break
                
                if is_blacklisted:
                    continue
                
                valid.append(url)
                    
            except Exception:
                continue
        
        return valid
    
    def _validate_and_extract_companies(self, urls: List[str]) -> List[Dict]:
        companies = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {
                executor.submit(self._validate_single_website, url): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    companies.append(result)
        
        return companies
    
    def _validate_single_website(self, url: str) -> Dict:
        try:
            response = self.session.get(url, timeout=8, allow_redirects=True)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            company_name = self._extract_company_name(soup, url)
            
            if not company_name or len(company_name) < 2:
                return None
            
            return {
                'name': company_name,
                'website': url,
                'title': soup.title.string[:100] if soup.title else '',
                'description': self._extract_description(soup)
            }
            
        except Exception:
            return None
    
    def _extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        # Try og:site_name
        og_site = soup.find('meta', property='og:site_name')
        if og_site and og_site.get('content'):
            name = og_site['content'].strip()
            if len(name) > 2:
                return self._clean_name(name)
        
        # Try title
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            # Clean common separators
            for sep in ['|', '–', '—', '·', '•', '-']:
                if sep in title:
                    parts = title.split(sep)
                    for part in parts:
                        part = part.strip()
                        if len(part) > 2:
                            return self._clean_name(part)
            
            if len(title) > 2:
                return self._clean_name(title)
        
        # Fallback to domain
        extracted = tldextract.extract(url)
        name = extracted.domain.capitalize()
        if name and len(name) > 2:
            return name
        
        return None
    
    def _clean_name(self, name: str) -> str:
        if not name:
            return None
        
        # Remove common suffixes but be less aggressive
        suffixes = [
            r'\s*(Inc|Corp|LLC|LLP|Ltd|Limited|Pvt|Private)\s*$',
            r'\s*(Technologies|Technology|Solutions|Services|Company|Agency|Firm)\s*$'
        ]
        
        for pattern in suffixes:
            name = re.sub(pattern, '', name, flags=re.I)
        
        name = name.strip()
        
        if len(name) > 2 and len(name) < 60:
            return name
        
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta.get('content')[:200]
        
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'][:200]
        
        return ''

company_discovery = CompanyDiscovery()
