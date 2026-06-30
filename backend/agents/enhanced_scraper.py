"""
Enhanced Scraper Agent - Improved filtering for services
"""

import re
import asyncio
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .base_agent import BaseAgent

class EnhancedScraperAgent(BaseAgent):
    def __init__(self):
        super().__init__("EnhancedScraperAgent")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.visited_urls = set()
        
        # Keywords to filter out (navigation, footer, generic)
        self.skip_keywords = [
            'let\'s connect', 'contact us', 'sign in', 'register', 'login',
            'privacy policy', 'terms of use', 'cookie policy', 'about us',
            'careers', 'blog', 'news', 'events', 'webinars', 'podcasts',
            'sitemap', 'help', 'support', 'faq', 'search', 'menu',
            'home', 'back to top', 'view all', 'read more', 'learn more',
            'get started', 'request demo', 'free trial', 'download',
            'follow us', 'share', 'subscribe', 'newsletter'
        ]
        
        # Country/region names to filter out
        self.country_names = [
            'afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua', 'argentina',
            'armenia', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh',
            'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bhutan', 'bolivia',
            'bosnia', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina', 'burundi',
            'cambodia', 'cameroon', 'canada', 'cape verde', 'central african', 'chad',
            'chile', 'china', 'colombia', 'comoros', 'congo', 'costa rica', 'croatia',
            'cuba', 'cyprus', 'czech', 'denmark', 'djibouti', 'dominica', 'dominican',
            'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia',
            'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia', 'georgia',
            'germany', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea', 'guyana',
            'haiti', 'honduras', 'hungary', 'iceland', 'india', 'indonesia', 'iran',
            'iraq', 'ireland', 'israel', 'italy', 'ivory coast', 'jamaica', 'japan',
            'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kuwait', 'kyrgyzstan', 'laos',
            'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania',
            'luxembourg', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta',
            'marshall islands', 'mauritania', 'mauritius', 'mexico', 'micronesia', 'moldova',
            'monaco', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'myanmar', 'namibia',
            'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria',
            'north korea', 'north macedonia', 'norway', 'oman', 'pakistan', 'palau', 'panama',
            'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal',
            'qatar', 'romania', 'russia', 'rwanda', 'saint kitts', 'saint lucia',
            'saint vincent', 'samoa', 'san marino', 'sao tome', 'saudi arabia', 'senegal',
            'serbia', 'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia',
            'solomon islands', 'somalia', 'south africa', 'south korea', 'south sudan',
            'spain', 'sri lanka', 'sudan', 'suriname', 'swaziland', 'sweden', 'switzerland',
            'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo',
            'tonga', 'trinidad', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda',
            'ukraine', 'united arab emirates', 'united kingdom', 'united republic of',
            'united states', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican', 'venezuela',
            'vietnam', 'yemen', 'zambia', 'zimbabwe'
        ]
        
        # Common generic words to filter out
        self.generic_words = [
            'services', 'solutions', 'offerings', 'expertise', 'capabilities',
            'about', 'contact', 'home', 'menu', 'back', 'support', 'help',
            'faq', 'events', 'news', 'blog', 'careers', 'partners', 'clients'
        ]
    
    async def process(self, input_data: Dict) -> Dict:
        urls = input_data.get("urls", [])
        self.log(f"Starting enhanced scrape of {len(urls)} companies")
        
        results = []
        for url in urls:
            try:
                data = await self._scrape_company(url)
                results.append({"url": url, "data": data, "status": "success"})
                await asyncio.sleep(1)
            except Exception as e:
                self.log(f"Error: {str(e)}")
                results.append({"url": url, "error": str(e), "status": "failed"})
        
        return {"scraped_data": results, "total": len(results)}
    
    async def _scrape_company(self, url: str) -> Dict:
        """Scrape company data from multiple pages with improved filtering"""
        
        # 1. Scrape homepage
        home_data = await self._scrape_page(url)
        
        # 2. Try to find and scrape services page
        services_data = await self._find_and_scrape_page(url, ['services', 'solutions', 'what-we-do'])
        
        # 3. Try to find and scrape about page
        about_data = await self._find_and_scrape_page(url, ['about', 'company', 'who-we-are'])
        
        # Merge all text
        combined_text = " ".join([
            home_data.get('text', ''),
            services_data.get('text', ''),
            about_data.get('text', '')
        ])
        
        # Extract services with improved filtering
        services = self._extract_services_clean(combined_text, home_data.get('soup'), services_data.get('soup'))
        
        # Extract tech stack
        tech_stack = self._extract_tech_clean(combined_text)
        
        # Extract clients
        clients = self._extract_clients_clean(combined_text, home_data.get('soup'))
        
        # Extract company name
        company_name = self._extract_company_name_clean(home_data.get('soup'), url)
        
        # Extract about
        about = self._extract_about_clean(home_data.get('soup'), about_data.get('soup'), combined_text)
        
        # Extract founded year
        founded_year = self._extract_founded_year_clean(combined_text)
        
        # Extract industry
        industry = self._extract_industry_clean(combined_text)
        
        return {
            "company_name": company_name,
            "url": url,
            "services": services[:20],
            "tech_stack": tech_stack[:15],
            "clients": {"names": clients[:15]},
            "about": about[:500],
            "founded_year": founded_year,
            "industry": industry[:10],
            "page_title": home_data.get('title', ''),
            "meta_description": home_data.get('description', '')
        }
    
    async def _scrape_page(self, url: str) -> Dict:
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return {}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()
            
            return {
                'soup': soup,
                'text': text,
                'title': soup.title.string if soup.title else '',
                'description': self._get_meta_description(soup)
            }
        except:
            return {}
    
    async def _find_and_scrape_page(self, base_url: str, paths: List[str]) -> Dict:
        for path in paths:
            for prefix in ['', '/', '/en/', '/us/', '/global/']:
                url = urljoin(base_url, f"{prefix}{path}")
                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    result = await self._scrape_page(url)
                    if result:
                        return result
        return {}
    
    def _is_valid_service(self, text: str) -> bool:
        """Check if text is a valid service name"""
        if not text or len(text) < 3 or len(text) > 80:
            return False
        
        text_lower = text.lower()
        
        # Skip if it's a country name
        for country in self.country_names:
            if country in text_lower:
                return False
        
        # Skip if it's a generic word
        for word in self.generic_words:
            if text_lower == word or text_lower.endswith(word):
                return False
        
        # Skip if it's navigation/footer text
        for skip in self.skip_keywords:
            if skip in text_lower:
                return False
        
        # Must contain service-related words
        service_indicators = [
            'development', 'services', 'solutions', 'consulting', 'engineering',
            'design', 'build', 'cloud', 'data', 'ai', 'analytics', 'security',
            'automation', 'integration', 'management', 'transformation',
            'strategy', 'architecture', 'platform', 'infrastructure'
        ]
        
        has_indicator = any(ind in text_lower for ind in service_indicators)
        if not has_indicator:
            # Check if it's a common service name
            common_services = [
                'artificial intelligence', 'machine learning', 'cloud computing',
                'cybersecurity', 'digital transformation', 'data analytics',
                'software development', 'web development', 'mobile development',
                'devops', 'iot', 'blockchain', 'saas', 'enterprise solutions'
            ]
            if not any(service in text_lower for service in common_services):
                return False
        
        return True
    
    def _extract_services_clean(self, text: str, *soups) -> List[str]:
        """Extract services with clean filtering"""
        services = []
        
        # Common service keywords to look for
        service_keywords = [
            'AI Development', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'Custom Software Development', 'Web Development', 'Mobile Development',
            'Cloud Computing', 'Cloud Services', 'DevOps', 'Data Analytics',
            'Data Engineering', 'Digital Transformation', 'IoT', 'Blockchain',
            'Cybersecurity', 'Enterprise Solutions', 'SaaS', 'API Development',
            'IT Consulting', 'Managed Services', 'Quality Assurance', 'Automation',
            'RPA', 'Business Intelligence', 'Big Data', 'Application Modernization',
            'Cloud Migration', 'Infrastructure Management', 'Security Consulting',
            'Strategy Consulting', 'Product Engineering', 'Platform Engineering',
            'Salesforce', 'SAP', 'Oracle', 'ERP', 'CRM', 'Data Science',
            'AI Consulting', 'MLOps', 'DevSecOps', 'Cloud Native Development',
            'Microservices', 'Serverless', 'Containerization', 'Kubernetes',
            'Azure', 'AWS', 'GCP', 'Snowflake', 'Databricks', 'Tableau', 'PowerBI',
            'React', 'Angular', 'Vue.js', 'Node.js', 'Python', 'Java', 'Go', 'Rust'
        ]
        
        # Check for each keyword
        for keyword in service_keywords:
            if keyword.lower() in text.lower():
                if self._is_valid_service(keyword):
                    services.append(keyword)
        
        # Also extract from HTML sections
        for soup in soups:
            if not soup:
                continue
            
            # Look for service sections
            service_sections = soup.find_all(['div', 'section', 'ul'], 
                class_=re.compile(r'service|solution|offer|capability|expertise|what we do', re.I))
            
            for section in service_sections:
                # Get headings and list items
                items = section.find_all(['h2', 'h3', 'h4', 'h5', 'li', 'strong', 'b', 'span'])
                for item in items:
                    item_text = item.get_text(strip=True)
                    if self._is_valid_service(item_text):
                        services.append(item_text)
        
        # Also look for service-related paragraphs
        for soup in soups:
            if not soup:
                continue
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                p_text = p.get_text(strip=True)
                if len(p_text) > 10 and len(p_text) < 100:
                    if any(word in p_text.lower() for word in ['offer', 'provide', 'service', 'solution', 'develop', 'build']):
                        if self._is_valid_service(p_text):
                            services.append(p_text)
        
        # Remove duplicates and clean
        seen = set()
        unique = []
        for s in services:
            s = s.strip()
            # Remove numbering
            s = re.sub(r'^\d+\.\s*', '', s)
            s = re.sub(r'^[•●·\-*]\s*', '', s)
            if s and len(s) > 3 and s not in seen:
                seen.add(s)
                unique.append(s)
        
        return unique
    
    def _extract_tech_clean(self, text: str) -> List[str]:
        """Extract technology stack"""
        tech_stack = []
        
        technologies = [
            'Python', 'JavaScript', 'TypeScript', 'React', 'Angular', 'Vue.js', 'Next.js',
            'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot', 'Java', 'C#', '.NET',
            'Go', 'Rust', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
            'Kafka', 'Spark', 'Hadoop', 'Tableau', 'PowerBI', 'Snowflake', 'Databricks',
            'Git', 'GitHub', 'GitLab', 'Jenkins', 'Terraform', 'Salesforce', 'SAP', 'Oracle',
            'OpenAI', 'LangChain', 'LLM', 'RAG', 'Gemini', 'ChatGPT'
        ]
        
        for tech in technologies:
            if tech.lower() in text.lower():
                tech_stack.append(tech)
        
        return list(set(tech_stack))
    
    def _extract_clients_clean(self, text: str, soup) -> List[str]:
        """Extract client names"""
        clients = []
        
        # Look for client sections
        if soup:
            client_sections = soup.find_all(['div', 'section', 'ul'], 
                class_=re.compile(r'client|customer|partner|brand|clientele', re.I))
            for section in client_sections:
                section_text = section.get_text()
                # Look for company names
                company_pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})\b'
                matches = re.findall(company_pattern, section_text)
                for match in matches:
                    clean = match.strip()
                    if 3 < len(clean) < 40:
                        skip_words = ['Client', 'Customer', 'Partner', 'Brand', 'Logo', 'Trusted', 'View', 'All']
                        if clean not in skip_words and not any(word in clean.lower() for word in ['logo', 'icon', 'button']):
                            clients.append(clean)
        
        # Also look in text
        patterns = [
            r'(?:clients|customers|partners|trusted by)[:\s]+([^.\n]{10,80})',
            r'worked with\s+([^.\n]{10,80})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                names = re.split(r',\s*|\s+and\s+|\s*&\s*', match)
                for name in names:
                    clean = name.strip()
                    if 3 < len(clean) < 40:
                        skip_words = ['clients', 'customers', 'partners', 'include', 'trusted', 'more']
                        if not any(word in clean.lower() for word in skip_words):
                            clients.append(clean)
        
        return list(set(clients))
    
    def _extract_company_name_clean(self, soup, url: str) -> str:
        """Extract company name"""
        if soup:
            og = soup.find('meta', property='og:site_name')
            if og and og.get('content'):
                name = og['content'].strip()
                if len(name) > 2 and len(name) < 80:
                    return name
            
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
                for sep in ['|', '–', '—', '-']:
                    if sep in title:
                        parts = title.split(sep)
                        for part in parts:
                            part = part.strip()
                            if len(part) > 2 and len(part) < 60:
                                return part
        
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if domain_match:
            name = domain_match.group(1).split('.')[0]
            return name.capitalize()
        
        return "Unknown"
    
    def _extract_about_clean(self, home_soup, about_soup, text: str) -> str:
        """Extract about text"""
        soup = about_soup or home_soup
        if soup:
            about_section = soup.find(['div', 'section'], class_=re.compile(r'about|overview|company|hero', re.I))
            if about_section:
                about_text = about_section.get_text(strip=True)
                if len(about_text) > 50:
                    return about_text
        
        patterns = [
            r'(?:about|overview)[:\s]+([^.\n]{50,}[.][^.\n]{0,200})',
            r'we are\s+([^.\n]{50,}[.][^.\n]{0,200})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0][:500]
        
        return "No about information available"
    
    def _extract_founded_year_clean(self, text: str) -> str:
        patterns = [
            r'(?:founded|established|since|Years of)\s+(\d{4})',
            r'(\d{4})\s*(?:founded|established)',
            r'est\.\s*(\d{4})'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                year = matches[0]
                if 1900 <= int(year) <= 2025:
                    return year
        return "Unknown"
    
    def _extract_industry_clean(self, text: str) -> List[str]:
        industries = []
        industry_list = [
            'AI', 'Machine Learning', 'Data Science', 'SaaS', 'Cloud Computing',
            'Cybersecurity', 'Fintech', 'Healthtech', 'Edtech', 'E-commerce',
            'Analytics', 'Automation', 'Robotics', 'IoT', 'Blockchain',
            'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Education',
            'Government', 'Telecom', 'Media', 'Energy', 'Banking', 'Insurance'
        ]
        for industry in industry_list:
            if industry.lower() in text.lower():
                industries.append(industry)
        return list(set(industries))
    
    def _get_meta_description(self, soup) -> str:
        meta = soup.find("meta", attrs={"name": "description"})
        return meta.get("content") if meta else None

    def _extract_clients_clean(self, text: str, soup) -> List[str]:
        """Extract client names with better filtering"""
        clients = []
        
        # Skip patterns for noise
        noise_patterns = [
            r'files patents', r'from ideation to prototype', r'are at the heart of',
            r'delivers solutions for', r'retail', r'bfsi', r'and delivers solutions'
        ]
        
        # Look for client sections
        if soup:
            client_sections = soup.find_all(['div', 'section', 'ul'], 
                class_=re.compile(r'client|customer|partner|brand|clientele|logo', re.I))
            for section in client_sections:
                section_text = section.get_text()
                # Look for company names with proper capitalization
                company_pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})\b'
                matches = re.findall(company_pattern, section_text)
                for match in matches:
                    clean = match.strip()
                    # Filter criteria
                    if 3 < len(clean) < 40:
                        skip_words = ['Client', 'Customer', 'Partner', 'Brand', 'Logo', 'Trusted', 
                                    'View', 'All', 'Read', 'More', 'Learn', 'About', 'Contact',
                                    'Services', 'Solutions', 'Products', 'Company', 'Our', 'The']
                        if clean not in skip_words:
                            # Check for noise patterns
                            is_noise = False
                            for pattern in noise_patterns:
                                if re.search(pattern, clean, re.IGNORECASE):
                                    is_noise = True
                                    break
                            if not is_noise:
                                clients.append(clean)
        
        # Also look in text with better patterns
        patterns = [
            r'(?:clients|customers|partners|trusted by)[:\s]+([^.\n]{10,80})',
            r'worked with\s+([^.\n]{10,80})',
            r'(?:including|such as)\s+([^.\n]{10,80})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by commas, "and", "&"
                names = re.split(r',\s*|\s+and\s+|\s*&\s*', match)
                for name in names:
                    clean = name.strip()
                    # Filter criteria
                    if 3 < len(clean) < 40:
                        skip_words = ['clients', 'customers', 'partners', 'include', 'trusted', 
                                    'more', 'view', 'read', 'learn']
                        if not any(word in clean.lower() for word in skip_words):
                            # Check for noise patterns
                            is_noise = False
                            for pattern in noise_patterns:
                                if re.search(pattern, clean, re.IGNORECASE):
                                    is_noise = True
                                    break
                            if not is_noise:
                                clients.append(clean)
        
        return list(set(clients))
