from .base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime

class CleanerAgent(BaseAgent):
    def __init__(self):
        super().__init__("CleanerAgent")
    
    async def process(self, input_data: Dict) -> Dict:
        self.log("Cleaning tech company data")
        
        scraped_data = input_data.get("scraped_data", [])
        if not scraped_data:
            return {"error": "No data to clean"}
        
        cleaned = []
        for item in scraped_data:
            if item.get("status") == "success":
                data = item.get("data", {})
                cleaned_item = {
                    "company": data.get("company_name", "Unknown"),
                    "url": item.get("url"),
                    "scraped_at": datetime.now().isoformat(),
                    
                    # Business Intelligence
                    "company_size": data.get("company_size", {}),
                    "founded_year": data.get("founded_year", "Unknown"),
                    "headquarters": data.get("headquarters", {}),
                    "industry": data.get("industry_sector", []),
                    "business_model": data.get("business_model", {}),
                    
                    # Team
                    "leadership": data.get("leadership_team", []),
                    "team_size": data.get("team_size", 0),
                    "departments": data.get("departments", []),
                    
                    # Financials
                    "revenue": data.get("revenue", {}),
                    "funding": data.get("funding", {}),
                    "valuation": data.get("valuation", {}),
                    
                    # Products
                    "products": data.get("products", []),
                    "services": data.get("services", []),
                    "features": data.get("features", []),
                    "pricing": data.get("pricing", {}),
                    
                    # Technology
                    "tech_stack": data.get("tech_stack", []),
                    "platforms": data.get("platforms", []),
                    "integrations": data.get("integrations", []),
                    
                    # Market
                    "customers": data.get("customers", {}),
                    "partners": data.get("partners", []),
                    "clients": data.get("clients", []),
                    
                    # Social Proof
                    "awards": data.get("awards", []),
                    "certifications": data.get("certifications", []),
                    "press_mentions": data.get("press_mentions", []),
                    
                    # Online Presence
                    "social_links": data.get("social_links", {}),
                    "has_careers_page": data.get("careers_page", False)
                }
                cleaned.append(cleaned_item)
        
        return {
            "cleaned_data": cleaned,
            "total_items": len(cleaned),
            "cleaned_at": datetime.now().isoformat()
        }
