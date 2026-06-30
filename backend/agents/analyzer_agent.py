from .base_agent import BaseAgent
from typing import Dict, Any, List
from collections import Counter
import statistics

class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnalyzerAgent")
    
    async def process(self, input_data: Dict) -> Dict:
        self.log("Analyzing company data")
        
        cleaned_data = input_data.get("cleaned_data", [])
        if not cleaned_data:
            return {"error": "No data to analyze"}
        
        analysis = self._analyze_companies(cleaned_data)
        return {"analysis": analysis}
    
    def _analyze_companies(self, data: List[Dict]) -> Dict:
        # Extract all services
        all_services = []
        all_service_categories = []
        all_projects = []
        all_tech = []
        all_clients = []
        all_testimonials = []
        team_sizes = []
        founded_years = []
        
        for item in data:
            # Services
            services = item.get("services", [])
            if services:
                for service in services:
                    if isinstance(service, dict):
                        if service.get("name"):
                            all_services.append(service["name"])
                    elif isinstance(service, str):
                        all_services.append(service)
            
            # Service categories
            categories = item.get("service_categories", [])
            if categories:
                all_service_categories.extend(categories)
            
            # Projects
            projects = item.get("projects", [])
            if projects:
                for project in projects:
                    if isinstance(project, dict):
                        if project.get("name"):
                            all_projects.append(project["name"])
                    elif isinstance(project, str):
                        all_projects.append(project)
            
            # Tech stack
            tech = item.get("tech_stack", [])
            if tech:
                all_tech.extend(tech)
            
            # Clients
            clients = item.get("clients", [])
            if clients:
                all_clients.extend(clients)
            
            # Testimonials
            testimonials = item.get("testimonials", [])
            if testimonials:
                all_testimonials.extend(testimonials)
            
            # Team size - handle both dict and int
            team = item.get("team_size", {})
            if isinstance(team, dict):
                if team.get("count"):
                    team_sizes.append(team["count"])
            elif isinstance(team, (int, float)):
                team_sizes.append(team)
            
            # Founded year
            year = item.get("founded_year", "Unknown")
            if year != "Unknown":
                try:
                    founded_years.append(int(year))
                except:
                    pass
        
        # Service frequency
        service_counter = Counter(all_services)
        top_services = service_counter.most_common(10)
        
        # Category frequency
        category_counter = Counter(all_service_categories)
        top_categories = category_counter.most_common(10)
        
        # Tech stack frequency
        tech_counter = Counter(all_tech)
        top_tech = tech_counter.most_common(10)
        
        # Project frequency
        project_counter = Counter(all_projects)
        top_projects = project_counter.most_common(10)
        
        # Client frequency
        client_counter = Counter(all_clients)
        top_clients = client_counter.most_common(10)
        
        # Team size analysis
        team_stats = {}
        if team_sizes:
            team_stats = {
                "average": statistics.mean(team_sizes),
                "min": min(team_sizes),
                "max": max(team_sizes),
                "median": statistics.median(team_sizes)
            }
        
        # Founded year analysis
        year_stats = {}
        if founded_years:
            year_stats = {
                "average": statistics.mean(founded_years),
                "min": min(founded_years),
                "max": max(founded_years),
                "median": statistics.median(founded_years)
            }
        
        # Generate insights
        insights = []
        
        # Service insights
        if top_services:
            insights.append({
                "type": "Top Services",
                "description": f"Most common service: {top_services[0][0]} (mentioned {top_services[0][1]} times)",
                "details": [f"{s[0]}: {s[1]}x" for s in top_services[:5]]
            })
        
        # Category insights
        if top_categories:
            insights.append({
                "type": "Service Categories",
                "description": f"Top category: {top_categories[0][0]} (appears in {top_categories[0][1]} companies)",
                "details": [f"{c[0]}: {c[1]} companies" for c in top_categories[:5]]
            })
        
        # Tech insights
        if top_tech:
            insights.append({
                "type": "Technology Stack",
                "description": f"Most used technology: {top_tech[0][0]} (used by {top_tech[0][1]} companies)",
                "details": [f"{t[0]}: {t[1]} companies" for t in top_tech[:5]]
            })
        
        # Team insights
        if team_sizes:
            insights.append({
                "type": "Team Size",
                "description": f"Average team size: {team_stats['average']:.0f} employees",
                "details": [
                    f"Smallest: {team_stats['min']} employees",
                    f"Largest: {team_stats['max']} employees",
                    f"Median: {team_stats['median']:.0f} employees"
                ]
            })
        
        # Project insights
        if top_projects:
            insights.append({
                "type": "Projects",
                "description": f"Total projects found: {len(all_projects)}",
                "details": [f"{p[0][:50]}..." for p in top_projects[:5]]
            })
        
        return {
            "total_companies": len(data),
            "companies": [d.get("company") for d in data],
            
            # Service Analysis
            "service_analysis": {
                "total_services": len(set(all_services)),
                "top_services": [{"name": s[0], "count": s[1]} for s in top_services[:10]],
                "service_categories": [{"name": c[0], "count": c[1]} for c in top_categories[:10]]
            },
            
            # Technology Analysis
            "technology_analysis": {
                "total_technologies": len(set(all_tech)),
                "top_technologies": [{"name": t[0], "count": t[1]} for t in top_tech[:10]]
            },
            
            # Project Analysis
            "project_analysis": {
                "total_projects": len(all_projects),
                "top_projects": [{"name": p[0][:100], "count": p[1]} for p in top_projects[:10]]
            },
            
            # Client Analysis
            "client_analysis": {
                "total_clients": len(all_clients),
                "top_clients": [{"name": c[0], "count": c[1]} for c in top_clients[:10]]
            },
            
            # Team Analysis
            "team_analysis": team_stats,
            
            # Year Analysis
            "year_analysis": year_stats,
            
            # Testimonials
            "testimonial_count": len(all_testimonials),
            
            # Insights
            "insights": insights
        }
