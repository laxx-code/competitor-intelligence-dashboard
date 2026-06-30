from typing import List, Dict

class CompanySearchService:
    """Search for companies based on location and technology"""
    
    def __init__(self):
        self.company_data = self._load_company_data()
    
    def _load_company_data(self) -> Dict:
        """Load company data"""
        return {
            'pune': [
                {'name': 'Persistent Systems', 'url': 'https://www.persistent.com', 'tech': 'Digital Engineering'},
                {'name': 'KPIT Technologies', 'url': 'https://www.kpit.com', 'tech': 'Automotive Engineering'},
                {'name': 'Zensar Technologies', 'url': 'https://www.zensar.com', 'tech': 'Digital Solutions'},
                {'name': 'Xoriant', 'url': 'https://www.xoriant.com', 'tech': 'Digital Engineering'},
                {'name': 'Cybage Software', 'url': 'https://www.cybage.com', 'tech': 'Software Development'},
                {'name': 'Stark Digital', 'url': 'https://www.starkdigital.net', 'tech': 'AI & Automation'},
                {'name': 'Hidden Brains', 'url': 'https://www.hiddenbrains.com', 'tech': 'AI & Custom Software'},
                {'name': 'Hats-Off Digital', 'url': 'https://www.hatsoffdigital.com', 'tech': 'Digital Marketing'},
            ],
            'bangalore': [
                {'name': 'Flipkart', 'url': 'https://www.flipkart.com', 'tech': 'E-commerce'},
                {'name': 'Swiggy', 'url': 'https://www.swiggy.com', 'tech': 'Food Delivery'},
                {'name': 'Ola Cabs', 'url': 'https://www.olacabs.com', 'tech': 'Ride-hailing'},
                {'name': 'Byjus', 'url': 'https://www.byjus.com', 'tech': 'Edtech'},
                {'name': 'Razorpay', 'url': 'https://www.razorpay.com', 'tech': 'Fintech'},
                {'name': 'CRED', 'url': 'https://www.cred.club', 'tech': 'Fintech'},
                {'name': 'Groww', 'url': 'https://www.groww.in', 'tech': 'Investment'},
            ],
            'mumbai': [
                {'name': 'TCS', 'url': 'https://www.tcs.com', 'tech': 'IT Services'},
                {'name': 'Reliance Jio', 'url': 'https://www.jio.com', 'tech': 'Telecom'},
                {'name': 'L&T Infotech', 'url': 'https://www.lntinfotech.com', 'tech': 'IT Services'},
                {'name': 'Hexaware', 'url': 'https://www.hexaware.com', 'tech': 'IT Services'},
            ],
            'ai': [
                {'name': 'OpenAI', 'url': 'https://www.openai.com', 'tech': 'AI Research'},
                {'name': 'Anthropic', 'url': 'https://www.anthropic.com', 'tech': 'AI Safety'},
                {'name': 'Hugging Face', 'url': 'https://www.huggingface.co', 'tech': 'AI Models'},
                {'name': 'Cohere', 'url': 'https://www.cohere.com', 'tech': 'NLP'},
                {'name': 'Mistral AI', 'url': 'https://www.mistral.ai', 'tech': 'LLM'},
                {'name': 'DeepMind', 'url': 'https://www.deepmind.com', 'tech': 'AI Research'},
                {'name': 'Databricks', 'url': 'https://www.databricks.com', 'tech': 'Data + AI'},
                {'name': 'Snowflake', 'url': 'https://www.snowflake.com', 'tech': 'Data Cloud'},
                {'name': 'Palantir', 'url': 'https://www.palantir.com', 'tech': 'AI Analytics'},
                {'name': 'C3.ai', 'url': 'https://www.c3.ai', 'tech': 'Enterprise AI'},
            ]
        }
    
    def search_companies(self, location: str) -> List[Dict]:
        """Search for companies based on location"""
        location_lower = location.lower()
        
        # Check if searching for AI companies
        if 'ai' in location_lower or 'artificial' in location_lower:
            return self.company_data.get('ai', [])
        
        # Search by location
        for key, companies in self.company_data.items():
            if key in location_lower or location_lower in key:
                return companies
        
        # Return AI companies as fallback
        return self.company_data.get('ai', [])[:10]
    
    def search_with_llm(self, query: str) -> List[Dict]:
        """Search companies using LLM-style query"""
        # Extract location from query
        locations = ['pune', 'bangalore', 'mumbai', 'hyderabad', 'delhi', 'chennai']
        location = None
        
        for loc in locations:
            if loc in query.lower():
                location = loc
                break
        
        if location:
            return self.search_companies(location)
        
        # If no location found, search for AI companies
        return self.company_data.get('ai', [])[:10]

# Create instance
company_search = CompanySearchService()
