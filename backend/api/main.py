from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.enhanced_scraper import EnhancedScraperAgent
from agents.cleaner_agent import CleanerAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.base_agent import AgentOrchestrator
from company_search import company_search
from company_discovery_v2 import company_discovery

app = FastAPI(title="Competitor Intelligence Dashboard")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
orchestrator = AgentOrchestrator()
orchestrator.register(EnhancedScraperAgent())
orchestrator.register(CleanerAgent())
orchestrator.register(AnalyzerAgent())

reports = {}

class AnalyzeRequest(BaseModel):
    urls: List[str]

class DiscoverRequest(BaseModel):
    location: str
    company_type: str

@app.get("/")
def root():
    return {
        "message": "Competitor Intelligence API",
        "status": "running",
        "agents": ["EnhancedScraperAgent", "CleanerAgent", "AnalyzerAgent"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        workflow = [
            {"name": "scrape", "agent": "EnhancedScraperAgent", "input": {"urls": request.urls}},
            {"name": "clean", "agent": "CleanerAgent", "depends_on": "EnhancedScraperAgent"},
            {"name": "analyze", "agent": "AnalyzerAgent", "depends_on": "CleanerAgent"}
        ]
        
        results = await orchestrator.execute(workflow)
        
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        reports[report_id] = {
            "report_id": report_id,
            "generated_at": datetime.now().isoformat(),
            "urls": request.urls,
            "status": "completed",
            **results
        }
        
        return {
            "status": "success",
            "report_id": report_id,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
def get_reports():
    return {"reports": list(reports.values())}

@app.get("/api/alerts")
def get_alerts():
    return {"alerts": []}

@app.get("/api/sentiment/{company}")
def get_sentiment(company: str):
    return {"sentiment": {
        "company": company,
        "average_polarity": 0,
        "positive_count": 0,
        "negative_count": 0,
        "neutral_count": 0,
        "overall": "neutral",
        "sentiments": []
    }}

@app.get("/api/search/companies")
def search_companies(q: str):
    if not q:
        return {"error": "Please provide a search query"}
    companies = company_search.search_with_llm(q)
    return {
        "query": q,
        "count": len(companies),
        "companies": companies
    }

@app.post("/api/discover-companies-v2")
def discover_companies_v2(request: DiscoverRequest):
    """Company discovery - synchronous version"""
    if not request.location or not request.company_type:
        return {"error": "Location and company type are required"}
    
    companies = company_discovery.discover(request.location, request.company_type)
    
    return {
        "location": request.location,
        "company_type": request.company_type,
        "count": len(companies),
        "companies": companies
    }

@app.get("/api/agents/status")
def agent_status():
    return {"agents": {
        name: {"status": agent.status, "memory": len(agent.memory)}
        for name, agent in orchestrator.agents.items()
    }}

@app.delete("/api/reports/{report_id}")
def delete_report(report_id: str):
    if report_id in reports:
        del reports[report_id]
        return {"status": "deleted"}
    raise HTTPException(404, "Report not found")

from agents.comparison_agent import ComparisonAgent

@app.post("/api/compare")
async def compare_companies(request: dict):
    """Compare target company with competitors"""
    target_url = request.get("target_url", "").strip()
    competitor_urls = request.get("competitor_urls", [])
    
    if not target_url:
        return {"error": "Target URL is required"}
    
    if not competitor_urls:
        return {"error": "At least one competitor URL is required"}
    
    try:
        # Scrape target company
        target_workflow = [
            {"name": "scrape", "agent": "EnhancedScraperAgent", "input": {"urls": [target_url]}},
            {"name": "clean", "agent": "CleanerAgent", "depends_on": "EnhancedScraperAgent"}
        ]
        
        target_results = await orchestrator.execute(target_workflow)
        target_data = target_results.get('CleanerAgent', {}).get('cleaned_data', [])
        
        if not target_data:
            return {"error": f"Failed to scrape target: {target_url}"}
        
        target_company = target_data[0]
        
        # Scrape competitors
        competitor_workflow = [
            {"name": "scrape", "agent": "EnhancedScraperAgent", "input": {"urls": competitor_urls}},
            {"name": "clean", "agent": "CleanerAgent", "depends_on": "EnhancedScraperAgent"}
        ]
        
        competitor_results = await orchestrator.execute(competitor_workflow)
        competitor_data = competitor_results.get('CleanerAgent', {}).get('cleaned_data', [])
        
        if not competitor_data:
            return {"error": "Failed to scrape competitors"}
        
        # Run comparison
        comparison_agent = ComparisonAgent()
        comparison_result = await comparison_agent.process({
            "target": target_company,
            "competitors": competitor_data
        })
        
        return {
            "status": "success",
            "target": target_company,
            "competitors": competitor_data,
            "comparison": comparison_result.get("comparison", {}),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from agents.comparison_agent import ComparisonAgent
import traceback

@app.post("/api/compare")
async def compare_companies(request: dict):
    """Compare target company with competitors"""
    try:
        target_url = request.get("target_url", "").strip()
        competitor_urls = request.get("competitor_urls", [])
        
        if not target_url:
            return {"error": "Target URL is required"}
        
        if not competitor_urls:
            return {"error": "At least one competitor URL is required"}
        
        # Scrape target company
        target_workflow = [
            {"name": "scrape", "agent": "EnhancedScraperAgent", "input": {"urls": [target_url]}},
            {"name": "clean", "agent": "CleanerAgent", "depends_on": "EnhancedScraperAgent"}
        ]
        
        target_results = await orchestrator.execute(target_workflow)
        target_data = target_results.get('CleanerAgent', {}).get('cleaned_data', [])
        
        if not target_data:
            return {"error": f"Failed to scrape target: {target_url}"}
        
        target_company = target_data[0]
        
        # Scrape competitors
        competitor_workflow = [
            {"name": "scrape", "agent": "EnhancedScraperAgent", "input": {"urls": competitor_urls}},
            {"name": "clean", "agent": "CleanerAgent", "depends_on": "EnhancedScraperAgent"}
        ]
        
        competitor_results = await orchestrator.execute(competitor_workflow)
        competitor_data = competitor_results.get('CleanerAgent', {}).get('cleaned_data', [])
        
        if not competitor_data:
            return {"error": "Failed to scrape competitors"}
        
        # Run comparison with error handling
        try:
            comparison_agent = ComparisonAgent()
            comparison_result = await comparison_agent.process({
                "target": target_company,
                "competitors": competitor_data
            })
        except Exception as e:
            print(f"Comparison agent error: {str(e)}")
            print(traceback.format_exc())
            return {
                "error": "Comparison failed",
                "detail": str(e),
                "target": target_company,
                "competitors": competitor_data
            }
        
        return {
            "status": "success",
            "target": target_company,
            "competitors": competitor_data,
            "comparison": comparison_result.get("comparison", {}),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"API error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
