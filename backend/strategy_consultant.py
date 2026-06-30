"""
Business Strategy Agent using Local LLM (Ollama)
Generates AI-powered insights without hardcoded rules
"""

import json
import logging
import re
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests
from pydantic import BaseModel, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StrategyReport(BaseModel):
    """Pydantic model for strategy report validation"""
    executive_summary: Dict[str, Any]
    market_opportunities: List[Dict[str, Any]]
    technology_trends: Dict[str, Any]
    technology_gap_analysis: Dict[str, Any]
    service_gap_analysis: Dict[str, Any]
    industry_analysis: Dict[str, Any]
    client_analysis: Dict[str, Any]
    competitor_ranking: List[Dict[str, Any]]
    swot_analysis: Dict[str, Any]
    investment_recommendations: List[Dict[str, Any]]
    hiring_recommendations: List[Dict[str, Any]]
    business_expansion: Dict[str, Any]
    strategic_recommendations: List[Dict[str, Any]]
    risk_analysis: List[Dict[str, Any]]
    action_plan: Dict[str, Any]
    ai_insights: List[Dict[str, Any]]


class OllamaClient:
    """Client for interacting with local Ollama instance"""
    
    def __init__(self, model: str = "qwen3:8b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.timeout = 120
        
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 4000) -> str:
        """Generate response from Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama. Is it running?")
            logger.info("Start Ollama with: ollama serve")
            raise
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            raise
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


class PromptBuilder:
    """Builds prompts for the LLM"""
    
    def __init__(self, target_company: str = "Stark Digital"):
        self.target_company = target_company
    
    def build_prompt(self, cleaned_data: List[Dict], analysis: Dict) -> str:
        """Build the complete prompt for the LLM"""
        
        # Prepare data summary
        data_summary = self._prepare_data_summary(cleaned_data, analysis)
        
        prompt = f"""You are a Senior Business Strategy Consultant, Competitive Intelligence Expert, and AI Technology Advisor.

TARGET COMPANY: {self.target_company}

COMPETITOR DATA:
{json.dumps(data_summary, indent=2)}

Your task is to analyze this competitor data and provide a comprehensive business strategy report.

IMPORTANT RULES:
1. Do NOT hardcode values or make up data
2. Every insight must be based on the provided data
3. If evidence is insufficient, say "Insufficient evidence from competitor dataset"
4. Do NOT fabricate numbers, percentages, or pricing
5. Think like a McKinsey consultant - compare all companies
6. Identify patterns, opportunities, and risks

OUTPUT FORMAT: Return ONLY valid JSON with this exact structure:

{{
  "executive_summary": {{
    "overview": "Brief overview of the competitive landscape",
    "market_position": "Description of market position",
    "competitive_landscape": "Analysis of competition",
    "overall_recommendation": "Strategic recommendation"
  }},
  "swot_analysis": {{
    "strengths": ["Strength 1", "Strength 2"],
    "weaknesses": ["Weakness 1", "Weakness 2"],
    "opportunities": ["Opportunity 1", "Opportunity 2"],
    "threats": ["Threat 1", "Threat 2"]
  }},
  "market_opportunities": [
    {{"title": "Opportunity Title", "description": "Description", "impact": "High|Medium|Low", "confidence": 85, "reasoning": "Why this is an opportunity"}}
  ],
  "competitive_risks": [
    {{"title": "Risk Title", "description": "Description", "severity": "High|Medium|Low", "confidence": 80, "reasoning": "Why this is a risk"}}
  ],
  "technology_trends": {{
    "rapid_growth": ["Tech1", "Tech2"],
    "stable": ["Tech1", "Tech2"],
    "declining": ["Tech1", "Tech2"],
    "emerging": ["Tech1", "Tech2"],
    "recommended_adoption": ["Tech1", "Tech2"]
  }},
  "technology_gap_analysis": {{
    "widely_used_by_competitors": ["Tech1", "Tech2"],
    "rare_technologies": ["Tech1", "Tech2"],
    "future_trending": ["Tech1", "Tech2"],
    "recommendation": "Strategic recommendation"
  }},
  "service_gap_analysis": {{
    "most_common_services": ["Service1", "Service2"],
    "underserved_services": ["Service1", "Service2"],
    "high_demand_services": ["Service1", "Service2"],
    "recommended_services": ["Service1", "Service2"]
  }},
  "industry_analysis": {{
    "top_industries": ["Industry1", "Industry2"],
    "least_served_industries": ["Industry1", "Industry2"],
    "recommended_expansion": ["Industry1", "Industry2"],
    "industry_opportunities": ["Opportunity1", "Opportunity2"]
  }},
  "client_analysis": {{
    "major_shared_clients": ["Client1", "Client2"],
    "high_competition_segments": ["Segment1", "Segment2"],
    "recommended_target_clients": ["Client1", "Client2"]
  }},
  "competitor_ranking": [
    {{"company": "Company1", "innovation_score": 85, "technology_score": 80, "market_score": 75, "service_score": 90, "overall_score": 82, "reasoning": "Reasoning"}}
  ],
  "investment_recommendations": [
    {{"category": "Category", "priority": "High|Medium|Low", "reason": "Reason"}}
  ],
  "hiring_recommendations": [
    {{"role": "Role", "reason": "Reason", "priority": "High|Medium|Low"}}
  ],
  "business_expansion": {{
    "recommended_regions": ["Region1", "Region2"],
    "recommended_industries": ["Industry1", "Industry2"],
    "recommended_services": ["Service1", "Service2"]
  }},
  "strategic_recommendations": [
    {{"title": "Recommendation", "description": "Description", "priority": "High|Medium|Low", "impact": "Description of impact"}}
  ],
  "risk_analysis": [
    {{"risk": "Risk Description", "probability": "High|Medium|Low", "impact": "High|Medium|Low", "mitigation": "How to mitigate"}}
  ],
  "action_plan": {{
    "immediate": ["Action1", "Action2"],
    "next_30_days": ["Action1", "Action2"],
    "next_90_days": ["Action1", "Action2"],
    "next_6_months": ["Action1", "Action2"]
  }},
  "ai_insights": [
    {{"title": "Insight Title", "description": "Description", "category": "Category", "priority": "High|Medium|Low", "confidence": 85, "action": "Recommended action"}}
  ]
}}

Generate the JSON now. Think deeply and provide meaningful analysis based on the data."""
        
        return prompt
    
    def _prepare_data_summary(self, cleaned_data: List[Dict], analysis: Dict) -> Dict:
        """Prepare a concise data summary for the prompt"""
        return {
            "target_company": self.target_company,
            "competitors": [
                {
                    "name": c.get("company", "Unknown"),
                    "services": c.get("services", []),
                    "tech_stack": c.get("tech_stack", []),
                    "industry": c.get("industry", []),
                    "clients": c.get("clients", {}).get("names", []),
                    "founded_year": c.get("founded_year", "Unknown"),
                    "team_size": c.get("team_size", {}),
                    "about": c.get("about", "")[:200] + "..."
                }
                for c in cleaned_data
            ],
            "analysis_summary": {
                "total_companies": len(cleaned_data),
                "total_services": analysis.get('service_analysis', {}).get('total_services', 0),
                "total_technologies": analysis.get('technology_analysis', {}).get('total_technologies', 0),
                "common_services": analysis.get('service_analysis', {}).get('top_services', [])[:5],
                "common_technologies": analysis.get('technology_analysis', {}).get('top_technologies', [])[:5]
            }
        }


class JSONParser:
    """Parse and validate JSON from LLM response"""
    
    def parse(self, response: str) -> Dict:
        """Parse JSON from LLM response"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return None


class ResponseValidator:
    """Validate the structure of the strategy report"""
    
    def validate(self, report: Dict) -> bool:
        """Validate the report structure"""
        required_keys = [
            "executive_summary", "market_opportunities", "technology_trends",
            "technology_gap_analysis", "service_gap_analysis", "industry_analysis",
            "client_analysis", "competitor_ranking", "swot_analysis",
            "investment_recommendations", "hiring_recommendations",
            "business_expansion", "strategic_recommendations", "risk_analysis",
            "action_plan", "ai_insights"
        ]
        
        for key in required_keys:
            if key not in report:
                logger.warning(f"Missing required key: {key}")
                return False
        
        return True
    
    def fill_missing_fields(self, report: Dict) -> Dict:
        """Fill missing fields with empty values"""
        default_report = {
            "executive_summary": {
                "overview": "Analysis of competitors.",
                "market_position": "Emerging market",
                "competitive_landscape": "Moderate competition",
                "overall_recommendation": "Focus on differentiation."
            },
            "market_opportunities": [],
            "technology_trends": {
                "rapid_growth": [], "stable": [], "declining": [], "emerging": [], "recommended_adoption": []
            },
            "technology_gap_analysis": {
                "widely_used_by_competitors": [], "rare_technologies": [], "future_trending": [], "recommendation": ""
            },
            "service_gap_analysis": {
                "most_common_services": [], "underserved_services": [], "high_demand_services": [], "recommended_services": []
            },
            "industry_analysis": {
                "top_industries": [], "least_served_industries": [], "recommended_expansion": [], "industry_opportunities": []
            },
            "client_analysis": {
                "major_shared_clients": [], "high_competition_segments": [], "recommended_target_clients": []
            },
            "competitor_ranking": [],
            "swot_analysis": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
            "investment_recommendations": [],
            "hiring_recommendations": [],
            "business_expansion": {"recommended_regions": [], "recommended_industries": [], "recommended_services": []},
            "strategic_recommendations": [],
            "risk_analysis": [],
            "action_plan": {"immediate": [], "next_30_days": [], "next_90_days": [], "next_6_months": []},
            "ai_insights": []
        }
        
        # Merge with defaults for missing keys
        for key, default_value in default_report.items():
            if key not in report:
                report[key] = default_value
            elif isinstance(default_value, dict) and isinstance(report[key], dict):
                for sub_key, sub_value in default_value.items():
                    if sub_key not in report[key]:
                        report[key][sub_key] = sub_value
        
        return report


class StrategyConsultant:
    """Main Strategy Consultant class"""
    
    def __init__(self, model: str = "qwen3:8b", target_company: str = "Stark Digital"):
        self.ollama = OllamaClient(model)
        self.prompt_builder = PromptBuilder(target_company)
        self.parser = JSONParser()
        self.validator = ResponseValidator()
        self.target_company = target_company
        
    def analyze(self, cleaned_data: List[Dict], analysis: Dict) -> Dict:
        """Generate business strategy report"""
        
        logger.info(f"Generating strategy report for {self.target_company}")
        logger.info(f"Analyzing {len(cleaned_data)} competitors")
        
        # Check if Ollama is available
        if not self.ollama.is_available():
            logger.error("Ollama is not available")
            return self._generate_error_report("Ollama service is not running. Please start Ollama with: ollama serve")
        
        if not cleaned_data:
            return self._generate_error_report("No competitor data available")
        
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt(cleaned_data, analysis)
            logger.info("Prompt built successfully")
            
            # Get response from Ollama
            response = self.ollama.generate(prompt)
            logger.info("Ollama response received")
            
            # Parse JSON
            report = self.parser.parse(response)
            if not report:
                logger.warning("Failed to parse JSON, retrying...")
                # Retry once
                response = self.ollama.generate(prompt)
                report = self.parser.parse(response)
                
                if not report:
                    logger.error("Failed to parse JSON after retry")
                    return self._generate_error_report("Failed to parse AI response")
            
            # Validate report
            if not self.validator.validate(report):
                logger.warning("Report validation failed, filling missing fields")
                report = self.validator.fill_missing_fields(report)
            
            # Add metadata
            report["generated_at"] = datetime.now().isoformat()
            report["companies_analyzed"] = len(cleaned_data)
            report["target_company"] = self.target_company
            report["model"] = self.ollama.model
            
            logger.info("Strategy report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Error generating strategy report: {e}")
            return self._generate_error_report(str(e))
    
    def _generate_error_report(self, error_message: str) -> Dict:
        """Generate error report"""
        return {
            "error": True,
            "message": error_message,
            "executive_summary": {
                "overview": f"Error: {error_message}",
                "market_position": "Unknown",
                "competitive_landscape": "Unable to analyze",
                "overall_recommendation": "Check Ollama connection and try again."
            },
            "market_opportunities": [],
            "technology_trends": {
                "rapid_growth": [], "stable": [], "declining": [], "emerging": [], "recommended_adoption": []
            },
            "technology_gap_analysis": {
                "widely_used_by_competitors": [], "rare_technologies": [], "future_trending": [], "recommendation": ""
            },
            "service_gap_analysis": {
                "most_common_services": [], "underserved_services": [], "high_demand_services": [], "recommended_services": []
            },
            "industry_analysis": {
                "top_industries": [], "least_served_industries": [], "recommended_expansion": [], "industry_opportunities": []
            },
            "client_analysis": {
                "major_shared_clients": [], "high_competition_segments": [], "recommended_target_clients": []
            },
            "competitor_ranking": [],
            "swot_analysis": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
            "investment_recommendations": [],
            "hiring_recommendations": [],
            "business_expansion": {"recommended_regions": [], "recommended_industries": [], "recommended_services": []},
            "strategic_recommendations": [],
            "risk_analysis": [],
            "action_plan": {"immediate": [], "next_30_days": [], "next_90_days": [], "next_6_months": []},
            "ai_insights": [],
            "generated_at": datetime.now().isoformat(),
            "companies_analyzed": 0
        }


# Singleton instance
strategy_consultant = StrategyConsultant(target_company="Stark Digital")
