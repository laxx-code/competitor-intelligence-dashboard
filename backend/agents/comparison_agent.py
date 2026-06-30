"""
Comparison Agent - Compares target company with competitors
Handles missing data gracefully with safe defaults
"""

import json
from typing import Dict, Any, List
from datetime import datetime
from collections import Counter
from .base_agent import BaseAgent

class ComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__("ComparisonAgent")
    
    async def process(self, input_data: Dict) -> Dict:
        """Process comparison between target and competitors"""
        self.log("Starting comparison analysis")
        
        target = input_data.get("target", {})
        competitors = input_data.get("competitors", [])
        
        # Ensure we have data
        if not target:
            self.log("Warning: No target data provided")
            target = self._create_empty_company("Unknown Target")
        
        if not competitors:
            self.log("Warning: No competitors provided")
            competitors = [self._create_empty_company("Unknown Competitor")]
        
        comparison = self._compare_safe(target, competitors)
        
        return {
            "comparison": comparison,
            "generated_at": datetime.now().isoformat(),
            "target": target.get("company", "Unknown"),
            "competitor_count": len(competitors)
        }
    
    def _create_empty_company(self, name: str) -> Dict:
        """Create an empty company with safe defaults"""
        return {
            "company": name,
            "url": "",
            "services": [],
            "tech_stack": [],
            "clients": {"names": []},
            "team_size": {"count": 0},
            "founded_year": "Unknown",
            "industry": [],
            "about": ""
        }
    
    def _compare_safe(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Perform comparison with safe data access"""
        
        # Ensure all data has default values
        target = self._ensure_defaults(target)
        competitors = [self._ensure_defaults(c) for c in competitors]
        
        # 1. Service Comparison
        service_comparison = self._compare_services(target, competitors)
        
        # 2. Technology Comparison
        tech_comparison = self._compare_technologies(target, competitors)
        
        # 3. Client Comparison
        client_comparison = self._compare_clients(target, competitors)
        
        # 4. Metrics Comparison
        metrics_comparison = self._compare_metrics(target, competitors)
        
        # 5. Gap Analysis
        gap_analysis = self._analyze_gaps(target, competitors)
        
        # 6. Competitive Position
        competitive_position = self._calculate_position(target, competitors)
        
        # 7. Recommendations
        recommendations = self._generate_recommendations(
            target, competitors, gap_analysis, competitive_position
        )
        
        return {
            "service_comparison": service_comparison,
            "technology_comparison": tech_comparison,
            "client_comparison": client_comparison,
            "metrics_comparison": metrics_comparison,
            "gap_analysis": gap_analysis,
            "competitive_position": competitive_position,
            "recommendations": recommendations
        }
    
    def _ensure_defaults(self, company: Dict) -> Dict:
        """Ensure company data has default values"""
        return {
            "company": company.get("company", "Unknown"),
            "url": company.get("url", ""),
            "services": company.get("services", []) or [],
            "tech_stack": company.get("tech_stack", []) or [],
            "clients": company.get("clients", {"names": []}) or {"names": []},
            "team_size": company.get("team_size", {"count": 0}) or {"count": 0},
            "founded_year": company.get("founded_year", "Unknown"),
            "industry": company.get("industry", []) or [],
            "about": company.get("about", "")
        }
    
    def _compare_services(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Compare services between target and competitors"""
        target_services = set(target.get("services", []))
        
        competitor_services = []
        for comp in competitors:
            competitor_services.append({
                "name": comp.get("company", "Unknown"),
                "services": set(comp.get("services", []))
            })
        
        all_competitor_services = set()
        for comp in competitor_services:
            all_competitor_services.update(comp["services"])
        
        common_services = target_services & all_competitor_services
        unique_target = target_services - all_competitor_services
        missing_from_target = all_competitor_services - target_services
        
        return {
            "target_services": list(target_services)[:10],
            "total_competitor_services": list(all_competitor_services)[:10],
            "common_services": list(common_services)[:10],
            "unique_to_target": list(unique_target)[:10],
            "missing_from_target": list(missing_from_target)[:10],
            "competitor_services": competitor_services
        }
    
    def _compare_technologies(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Compare technologies between target and competitors"""
        target_tech = set(target.get("tech_stack", []))
        
        competitor_tech = []
        for comp in competitors:
            competitor_tech.append({
                "name": comp.get("company", "Unknown"),
                "tech": set(comp.get("tech_stack", []))
            })
        
        all_competitor_tech = set()
        for comp in competitor_tech:
            all_competitor_tech.update(comp["tech"])
        
        common_tech = target_tech & all_competitor_tech
        unique_target = target_tech - all_competitor_tech
        missing_from_target = all_competitor_tech - target_tech
        
        return {
            "target_technologies": list(target_tech)[:10],
            "total_competitor_technologies": list(all_competitor_tech)[:10],
            "common_technologies": list(common_tech)[:10],
            "unique_to_target": list(unique_target)[:10],
            "missing_from_target": list(missing_from_target)[:10],
            "competitor_technologies": competitor_tech
        }
    
    def _compare_clients(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Compare clients between target and competitors"""
        target_clients = set(target.get("clients", {}).get("names", []))
        
        competitor_clients = []
        for comp in competitors:
            comp_clients = comp.get("clients", {}).get("names", [])
            competitor_clients.append({
                "name": comp.get("company", "Unknown"),
                "clients": set(comp_clients)
            })
        
        all_competitor_clients = set()
        for comp in competitor_clients:
            all_competitor_clients.update(comp["clients"])
        
        common_clients = target_clients & all_competitor_clients
        unique_target = target_clients - all_competitor_clients
        missing_from_target = all_competitor_clients - target_clients
        
        return {
            "target_clients": list(target_clients)[:10],
            "total_competitor_clients": list(all_competitor_clients)[:10],
            "common_clients": list(common_clients)[:10],
            "unique_to_target": list(unique_target)[:10],
            "missing_from_target": list(missing_from_target)[:10],
            "competitor_clients": competitor_clients
        }
    
    def _compare_metrics(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Compare company metrics"""
        target_metrics = {
            "team_size": target.get("team_size", {}).get("count", 0),
            "founded_year": target.get("founded_year", "Unknown"),
            "services_count": len(target.get("services", [])),
            "tech_count": len(target.get("tech_stack", [])),
            "client_count": len(target.get("clients", {}).get("names", []))
        }
        
        competitor_metrics = []
        for comp in competitors:
            competitor_metrics.append({
                "name": comp.get("company", "Unknown"),
                "team_size": comp.get("team_size", {}).get("count", 0),
                "founded_year": comp.get("founded_year", "Unknown"),
                "services_count": len(comp.get("services", [])),
                "tech_count": len(comp.get("tech_stack", [])),
                "client_count": len(comp.get("clients", {}).get("names", []))
            })
        
        # Calculate averages (handle division by zero)
        avg_services = sum(m["services_count"] for m in competitor_metrics) / len(competitor_metrics) if competitor_metrics else 0
        avg_tech = sum(m["tech_count"] for m in competitor_metrics) / len(competitor_metrics) if competitor_metrics else 0
        avg_clients = sum(m["client_count"] for m in competitor_metrics) / len(competitor_metrics) if competitor_metrics else 0
        
        return {
            "target": target_metrics,
            "competitors": competitor_metrics,
            "averages": {
                "services": avg_services,
                "technologies": avg_tech,
                "clients": avg_clients
            },
            "rankings": {
                "team_size": self._rank_metric(competitor_metrics, "team_size", target_metrics["team_size"]),
                "services": self._rank_metric(competitor_metrics, "services_count", target_metrics["services_count"]),
                "technologies": self._rank_metric(competitor_metrics, "tech_count", target_metrics["tech_count"]),
                "clients": self._rank_metric(competitor_metrics, "client_count", target_metrics["client_count"])
            }
        }
    
    def _rank_metric(self, competitors: List[Dict], metric: str, target_value: int) -> Dict:
        """Calculate rank for a metric"""
        values = [c[metric] for c in competitors]
        values.append(target_value)
        sorted_values = sorted(values, reverse=True)
        
        if target_value in sorted_values:
            rank = sorted_values.index(target_value) + 1
        else:
            rank = len(values)
        
        return {
            "rank": rank,
            "total": len(values),
            "target_value": target_value,
            "range": f"{min(values)} - {max(values)}" if values else "N/A"
        }
    
    def _analyze_gaps(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Identify gaps between target and competitors"""
        target_services = set(target.get("services", []))
        target_tech = set(target.get("tech_stack", []))
        target_clients = set(target.get("clients", {}).get("names", []))
        
        all_competitor_services = set()
        all_competitor_tech = set()
        all_competitor_clients = set()
        
        for comp in competitors:
            all_competitor_services.update(comp.get("services", []))
            all_competitor_tech.update(comp.get("tech_stack", []))
            all_competitor_clients.update(comp.get("clients", {}).get("names", []))
        
        return {
            "service_gaps": list(all_competitor_services - target_services)[:10],
            "technology_gaps": list(all_competitor_tech - target_tech)[:10],
            "client_gaps": list(all_competitor_clients - target_clients)[:10],
            "unique_services": list(target_services - all_competitor_services)[:10],
            "unique_technologies": list(target_tech - all_competitor_tech)[:10],
            "unique_clients": list(target_clients - all_competitor_clients)[:10]
        }
    
    def _calculate_position(self, target: Dict, competitors: List[Dict]) -> Dict:
        """Calculate competitive position"""
        target_services = len(target.get("services", []))
        target_tech = len(target.get("tech_stack", []))
        target_clients = len(target.get("clients", {}).get("names", []))
        
        avg_services = sum(len(c.get("services", [])) for c in competitors) / len(competitors) if competitors else 0
        avg_tech = sum(len(c.get("tech_stack", [])) for c in competitors) / len(competitors) if competitors else 0
        avg_clients = sum(len(c.get("clients", {}).get("names", [])) for c in competitors) / len(competitors) if competitors else 0
        
        # Calculate scores (avoid division by zero)
        service_score = min(100, (target_services / avg_services * 100) if avg_services > 0 else 50)
        tech_score = min(100, (target_tech / avg_tech * 100) if avg_tech > 0 else 50)
        client_score = min(100, (target_clients / avg_clients * 100) if avg_clients > 0 else 50)
        
        overall_score = (service_score + tech_score + client_score) / 3
        
        # Determine position
        if overall_score >= 80:
            position = "Market Leader"
        elif overall_score >= 60:
            position = "Strong Competitor"
        elif overall_score >= 40:
            position = "Mid-Tier Player"
        else:
            position = "Emerging Player"
        
        return {
            "position": position,
            "overall_score": overall_score,
            "service_score": service_score,
            "tech_score": tech_score,
            "client_score": client_score,
            "ranking": f"{overall_score:.0f}% vs competitors"
        }
    
    def _generate_recommendations(self, target: Dict, competitors: List[Dict], 
                                  gaps: Dict, position: Dict) -> List[Dict]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Service recommendations
        if gaps.get("service_gaps") and len(gaps["service_gaps"]) > 0:
            recommendations.append({
                "category": "Services",
                "title": "Add Missing Services",
                "description": f"Consider adding: {', '.join(gaps['service_gaps'][:3])}",
                "priority": "High",
                "impact": "High",
                "reason": "These services are offered by competitors but not by you",
                "missing": gaps["service_gaps"][:3]
            })
        
        # Technology recommendations
        if gaps.get("technology_gaps") and len(gaps["technology_gaps"]) > 0:
            recommendations.append({
                "category": "Technology",
                "title": "Adopt New Technologies",
                "description": f"Consider adopting: {', '.join(gaps['technology_gaps'][:3])}",
                "priority": "High",
                "impact": "Medium",
                "reason": "These technologies are used by competitors but not by you",
                "missing": gaps["technology_gaps"][:3]
            })
        
        # Client recommendations
        if gaps.get("client_gaps") and len(gaps["client_gaps"]) > 0:
            recommendations.append({
                "category": "Sales",
                "title": "Target New Clients",
                "description": f"Target clients: {', '.join(gaps['client_gaps'][:3])}",
                "priority": "Medium",
                "impact": "High",
                "reason": "These clients work with competitors but not with you",
                "missing": gaps["client_gaps"][:3]
            })
        
        # Unique strengths
        if gaps.get("unique_services") and len(gaps["unique_services"]) > 0:
            recommendations.append({
                "category": "Differentiation",
                "title": "Leverage Unique Services",
                "description": f"You offer unique services: {', '.join(gaps['unique_services'][:3])}",
                "priority": "High",
                "impact": "High",
                "reason": "These services differentiate you from competitors",
                "missing": []
            })
        
        # Position-based recommendations
        if position.get("position") == "Emerging Player":
            recommendations.append({
                "category": "Strategy",
                "title": "Build Market Presence",
                "description": "Focus on building market presence and awareness",
                "priority": "High",
                "impact": "High",
                "reason": "As an emerging player, focus on visibility and credibility",
                "missing": []
            })
        
        return recommendations

# Create instance
comparison_agent = ComparisonAgent()
