from .base_agent import BaseAgent
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
import re
import asyncio
from datetime import datetime


class EnhancedScraperAgent(BaseAgent):
    def __init__(self):
        super().__init__("EnhancedScraperAgent")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def process(self, input_data: Dict) -> Dict:
        urls = input_data.get("urls", [])
        self.log(f"Scraping {len(urls)} companies")
        
        results = []
        for url in urls:
            try:
                data = await self._scrape_company(url)
                results.append({"url": url, "data": data, "status": "success"})
                await asyncio.sleep(2)
            except Exception as e:
                self.log(f"Error: {str(e)}")
                results.append({"url": url, "error": str(e), "status": "failed"})
        
        return {"scraped_data": results, "total": len(results)}
    
    async def _scrape_company(self, url: str) -> Dict:
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            
            return {
                "company_name": self._get_company_name(url, soup),
                "url": url,
                "scraped_at": datetime.now().isoformat(),
                "services": self._get_services(soup),
                "projects": self._get_projects_from_content(soup, text),
                "about": self._get_about(soup),
                "founded_year": self._get_founded_year(text),
                "tech_stack": self._get_tech_stack(text),
                "clients": self._get_clients_from_content(soup, text),
                "testimonials": self._get_testimonials(soup),
                "industry": self._get_industry(text),
                "page_title": soup.title.string if soup.title else None,
                "meta_description": self._get_meta_description(soup)
            }
        except Exception as e:
            raise Exception(f"Scraping failed: {str(e)}")
    
    def _get_company_name(self, url: str, soup: BeautifulSoup) -> str:
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if domain_match:
            name = domain_match.group(1).split('.')[0]
            return name.capitalize()
        return "Unknown"
    
    def _get_services(self, soup: BeautifulSoup) -> List[str]:
        """Extract services from the page"""
        services = []
        
        # Look for service sections
        service_sections = soup.find_all(['div', 'section', 'ul'], 
                                        class_=re.compile(r'service|solution|offer|capability|expertise', re.I))
        
        for section in service_sections:
            # Find headings that could be service names
            headings = section.find_all(['h2', 'h3', 'h4', 'h5', 'strong'])
            for heading in headings:
                text = heading.get_text(strip=True)
                if 5 < len(text) < 80:
                    skip_words = ['services', 'solutions', 'offerings', 'expertise', 'capabilities', 'about', 'contact', 'home', 'menu']
                    if not any(word in text.lower() for word in skip_words):
                        services.append(text)
            
            # Also look for list items
            items = section.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if 5 < len(text) < 80:
                    service_indicators = ['development', 'consulting', 'solutions', 'services', 'engineering', 'design', 'build', 'cloud', 'ai', 'data']
                    if any(ind in text.lower() for ind in service_indicators):
                        services.append(text)
        
        # Remove duplicates
        seen = set()
        unique = []
        for s in services:
            clean = re.sub(r'^[•●·\-*]\s*', '', s).strip()
            if clean and len(clean) > 3 and clean not in seen:
                seen.add(clean)
                unique.append(clean)
        
        return unique[:25]
    
    def _get_projects_from_content(self, soup: BeautifulSoup, text: str) -> List[Dict]:
        """Extract projects from the actual content based on the website structure"""
        projects = []
        
        # === METHOD 1: Look for Case Study sections (GeekyAnts) ===
        case_study_sections = soup.find_all(['div', 'section', 'article'], 
                                           class_=re.compile(r'case|study|case-study|casestudy', re.I))
        
        for section in case_study_sections:
            # Find the case study title
            title_elem = section.find(['h2', 'h3', 'h4', 'h5', 'strong'])
            if title_elem:
                title = title_elem.get_text(strip=True)
                if 10 < len(title) < 150:
                    # Find description
                    desc_elem = section.find('p')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Find client if mentioned
                    client_match = re.search(r'(?:for|with|client)\s+([A-Z][a-zA-Z\s]+)', title + " " + description, re.I)
                    client = client_match.group(1).strip() if client_match else None
                    
                    projects.append({
                        "name": title[:100],
                        "description": description[:500] if description else "Case study available",
                        "client": client[:50] if client else None
                    })
        
        # === METHOD 2: Look for Blog/Article sections with project mentions ===
        blog_sections = soup.find_all(['div', 'article', 'section'], 
                                     class_=re.compile(r'blog|post|article|insight', re.I))
        
        for section in blog_sections:
            # Look for titles that might be project-related
            titles = section.find_all(['h2', 'h3', 'h4'])
            for title_elem in titles:
                title = title_elem.get_text(strip=True)
                # Check if it's project-related
                if any(word in title.lower() for word in ['building', 'develop', 'platform', 'system', 'app', 'solution', 'modernize']):
                    if 15 < len(title) < 150:
                        # Find description
                        desc_elem = section.find('p')
                        description = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        projects.append({
                            "name": title[:100],
                            "description": description[:500] if description else "Blog post about project",
                            "client": None
                        })
        
        # === METHOD 3: Look for Client/Project logos (Appinventiv) ===
        client_sections = soup.find_all(['div', 'section'], 
                                       class_=re.compile(r'client|partner|brand|logo', re.I))
        
        for section in client_sections:
            # Look for images with client names
            images = section.find_all('img')
            for img in images:
                alt = img.get('alt', '').strip()
                if 3 < len(alt) < 50:
                    skip_words = ['logo', 'icon', 'image', 'banner', 'hero', 'background', 'button']
                    if not any(word in alt.lower() for word in skip_words):
                        # Check if this is a client name
                        if any(char.isupper() for char in alt):
                            projects.append({
                                "name": f"Client Project - {alt}",
                                "description": f"Worked with {alt}",
                                "client": alt
                            })
        
        # === METHOD 4: Look for explicit project mentions in text ===
        # Pattern for "Company Name - Project Description"
        project_patterns = [
            r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:built|developed|created|launched|delivered)\s+([^.\n]{20,}[.][^.\n]{20,})',
            r'(?:case study|project|client story)\s*[:\s]+([^.\n]{20,}[.][^.\n]{20,})',
            r'helped\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:with|to)\s+([^.\n]{20,}[.][^.\n]{20,})'
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    client_name = match[0].strip()
                    description = match[1].strip()
                    if 20 < len(description) < 400 and len(client_name) > 3:
                        projects.append({
                            "name": f"Project for {client_name[:50]}",
                            "description": description[:500],
                            "client": client_name[:50]
                        })
                elif isinstance(match, str) and len(match) > 30:
                    # Try to extract client name
                    client_match = re.search(r'(?:for|with)\s+([A-Z][a-zA-Z\s]+)', match, re.I)
                    client = client_match.group(1).strip() if client_match else None
                    projects.append({
                        "name": match[:80],
                        "description": match[:500],
                        "client": client[:50] if client else None
                    })
        
        # === METHOD 5: Look for stats that indicate projects ===
        # Look for numbers that might indicate project count
        stat_patterns = [
            r'(\d+)\+?\s*(?:projects|solutions|products|engagements|deliveries)',
            r'(\d+)\+?\s*(?:clients|customers|brands)'
        ]
        
        project_count = None
        for pattern in stat_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    project_count = int(matches[0])
                    break
                except:
                    pass
        
        # Remove duplicates
        seen = set()
        unique_projects = []
        for p in projects:
            key = p["name"].lower()
            if key not in seen and len(p["name"]) > 5:
                seen.add(key)
                unique_projects.append(p)
        
        # If we have project count but no projects, add a summary
        if project_count and len(unique_projects) == 0:
            unique_projects.append({
                "name": f"{project_count}+ Projects Delivered",
                "description": f"The company has delivered {project_count}+ projects across various industries",
                "client": None
            })
        
        return unique_projects[:15]
    
    def _get_clients_from_content(self, soup: BeautifulSoup, text: str) -> Dict:
        """Extract clients from the actual content"""
        clients = []
        
        # Look for client sections with logos
        client_sections = soup.find_all(['div', 'section', 'ul'], 
                                       class_=re.compile(r'client|customer|partner|brand|logo', re.I))
        
        for section in client_sections:
            # Get all text and look for company names
            section_text = section.get_text()
            # Look for capitalized words (potential company names)
            company_pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})\b'
            matches = re.findall(company_pattern, section_text)
            for match in matches:
                clean = match.strip()
                if 3 < len(clean) < 40:
                    skip_words = ['Client', 'Customer', 'Partner', 'Brand', 'Logo', 'Trusted', 'Work', 'Case', 'Study', 'View', 'More', 'Read', 'Learn', 'Menu', 'Home', 'About', 'Contact']
                    if clean not in skip_words and not any(word in clean.lower() for word in ['logo', 'icon', 'button', 'call', 'explore', 'search']):
                        clients.append(clean)
        
        # Also look for client mentions in text
        patterns = [
            r'(?:clients|customers|partners|trusted by)\s+include\s+([^.\n]{10,80})',
            r'worked with\s+([^.\n]{10,80})',
            r'for\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by commas, "and", "&"
                names = re.split(r',\s*|\s+and\s+|\s*&\s*', match)
                for name in names:
                    clean = name.strip()
                    if 3 < len(clean) < 40:
                        skip_words = ['clients', 'customers', 'partners', 'include', 'trusted', 'more', 'view', 'read']
                        if not any(word in clean.lower() for word in skip_words):
                            clients.append(clean)
        
        # Get client count
        count = None
        count_patterns = [
            r'(\d+)\+?\s*(?:clients|customers|partners|brands)',
            r'(\d+)\s*(?:happy|satisfied)\s*(?:clients|customers)'
        ]
        
        for pattern in count_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    count = int(matches[0])
                    break
                except:
                    pass
        
        # Remove duplicates
        seen = set()
        unique = []
        for c in clients:
            if c.lower() not in seen:
                seen.add(c.lower())
                unique.append(c)
        
        return {"names": unique[:20], "count": count}
    
    def _get_about(self, soup: BeautifulSoup) -> str:
        about = soup.find(['div', 'section'], class_=re.compile(r'about|overview|company|hero', re.I))
        if about:
            text = about.get_text(strip=True)
            if len(text) > 50:
                return text[:500]
        
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if len(text) > 50 and any(word in text.lower() for word in ['company', 'we', 'our', 'mission', 'vision']):
                return text[:500]
        
        return "No about information available"
    
    def _get_founded_year(self, text: str) -> str:
        patterns = [
            r'(?:founded|established|since)\s+(\d{4})',
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
    
    def _get_tech_stack(self, text: str) -> List[str]:
        tech_stack = []
        technologies = [
            'Python', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Node.js',
            'Django', 'Flask', 'Java', 'Spring Boot', 'AWS', 'Azure', 'GCP',
            'Docker', 'Kubernetes', 'TensorFlow', 'PyTorch',
            'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'Git', 'GitHub', 'GitLab', 'Jenkins', 'Kafka', 'Spark'
        ]
        for tech in technologies:
            if tech.lower() in text.lower():
                tech_stack.append(tech)
        return list(set(tech_stack))[:15]
    
    def _get_industry(self, text: str) -> List[str]:
        industries = []
        industry_list = [
            'AI', 'Machine Learning', 'Data Science', 'SaaS', 'Cloud Computing',
            'Cybersecurity', 'Fintech', 'Healthtech', 'Edtech', 'E-commerce',
            'Analytics', 'Automation', 'Robotics', 'IoT', 'Blockchain'
        ]
        for industry in industry_list:
            if industry.lower() in text.lower():
                industries.append(industry)
        return list(set(industries))[:10]
    
    def _get_testimonials(self, soup: BeautifulSoup) -> List[Dict]:
        testimonials = []
        sections = soup.find_all(['div', 'blockquote'], 
                               class_=re.compile(r'testimonial|review|quote', re.I))
        for section in sections:
            text = section.get_text(strip=True)
            if len(text) > 20 and len(text) < 500:
                author = None
                author_elem = section.find(['span', 'cite', 'p'], 
                                         class_=re.compile(r'author|name|by', re.I))
                if author_elem:
                    author = author_elem.get_text(strip=True)
                testimonials.append({"text": text[:300], "author": author or "Anonymous"})
        return testimonials[:5]
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find("meta", attrs={"name": "description"})
        return meta.get("content") if meta else None
