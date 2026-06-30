from datetime import datetime
from typing import List, Dict, Any
import json

class AlertSystem:
    """Smart alert system for startup competitor changes"""
    
    def __init__(self):
        self.alerts = []
        self.channels = ['websocket', 'console']
    
    def check_for_changes(self, old_data: Dict, new_data: Dict) -> List[Dict]:
        """Check for changes between old and new competitor data"""
        alerts = []
        
        # Check for new services
        old_services = set(old_data.get('services', []))
        new_services = set(new_data.get('services', []))
        new_services_added = new_services - old_services
        
        if new_services_added:
            alerts.append({
                "type": "PRODUCT_LAUNCH",
                "competitor": new_data.get('company_name', 'Unknown'),
                "message": f"Launched new product/service: {', '.join(list(new_services_added)[:5])}",
                "severity": "high",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check for new clients
        old_clients = set(old_data.get('clients', {}).get('names', []))
        new_clients = set(new_data.get('clients', {}).get('names', []))
        new_clients_added = new_clients - old_clients
        
        if new_clients_added:
            alerts.append({
                "type": "NEW_CLIENT",
                "competitor": new_data.get('company_name', 'Unknown'),
                "message": f"Acquired new client: {', '.join(list(new_clients_added)[:5])}",
                "severity": "medium",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check for tech stack changes
        old_tech = set(old_data.get('tech_stack', []))
        new_tech = set(new_data.get('tech_stack', []))
        new_tech_added = new_tech - old_tech
        
        if new_tech_added:
            alerts.append({
                "type": "TECH_STACK_UPDATE",
                "competitor": new_data.get('company_name', 'Unknown'),
                "message": f"Adopted new technology: {', '.join(list(new_tech_added)[:5])}",
                "severity": "medium",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check for team growth (if we detect hiring)
        old_team = old_data.get('team_size', {}).get('count', 0)
        new_team = new_data.get('team_size', {}).get('count', 0)
        
        if new_team and old_team and new_team > old_team:
            alerts.append({
                "type": "TEAM_GROWTH",
                "competitor": new_data.get('company_name', 'Unknown'),
                "message": f"Team grew from {old_team} to {new_team} employees",
                "severity": "high",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check for funding (looking for keywords)
        about_text = new_data.get('about', '').lower()
        funding_keywords = ['funding', 'raised', 'series', 'investment', 'million', 'venture']
        
        if any(keyword in about_text for keyword in funding_keywords):
            # Try to extract funding amount
            import re
            amount_match = re.search(r'(\d+)\s*(?:million|m)', about_text, re.IGNORECASE)
            amount = f"${amount_match.group(1)}M" if amount_match else "Undisclosed amount"
            
            alerts.append({
                "type": "FUNDING",
                "competitor": new_data.get('company_name', 'Unknown'),
                "amount": amount,
                "message": f"Secured funding: {amount}",
                "severity": "high",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
    
    def send_alert(self, alert: Dict):
        """Send alert through configured channels"""
        self.alerts.append(alert)
        
        # Broadcast via WebSocket
        if 'websocket' in self.channels:
            try:
                from websocket_manager import ws_manager
                import asyncio
                asyncio.create_task(ws_manager.broadcast_alert(alert))
            except:
                pass
        
        # Console logging
        if 'console' in self.channels:
            print(f"🚀 STARTUP ALERT: {alert['message']}")
    
    def get_active_alerts(self) -> List[Dict]:
        """Get all active alerts"""
        return self.alerts[-50:]  # Return last 50 alerts

# Global alert system instance
alert_system = AlertSystem()
