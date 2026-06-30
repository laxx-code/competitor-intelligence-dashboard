"""
Database Manager for Competitor Intelligence
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from .models import (
    Company, Service, TechStack, Client, Project, 
    Report, ComparisonReport, init_db, get_db_url
)

class DatabaseManager:
    def __init__(self):
        self.db_url = get_db_url()
        self.engine = init_db(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._test_connection()
    
    def _test_connection(self):
        """Test database connection"""
        try:
            session = self.Session()
            session.execute("SELECT 1")
            session.close()
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("Please ensure PostgreSQL is running and database exists")
    
    def get_session(self):
        return self.Session()
    
    def save_company(self, company_data: dict):
        """Save or update company data"""
        session = self.get_session()
        try:
            url = company_data.get('url')
            if not url:
                raise ValueError("URL is required")
            
            # Check if company exists
            company = session.query(Company).filter_by(url=url).first()
            
            if company:
                # Update existing company
                company.name = company_data.get('company_name', company.name)
                company.founded_year = company_data.get('founded_year', company.founded_year)
                company.about = company_data.get('about', company.about)
                company.industry = company_data.get('industry', company.industry)
                company.team_size = company_data.get('team_size', {}).get('count', company.team_size)
                company.updated_at = datetime.now()
            else:
                # Create new company
                company = Company(
                    name=company_data.get('company_name', 'Unknown'),
                    url=url,
                    founded_year=company_data.get('founded_year', 'Unknown'),
                    about=company_data.get('about', ''),
                    industry=company_data.get('industry', []),
                    team_size=company_data.get('team_size', {}).get('count', 0),
                    location=company_data.get('location', '')
                )
                session.add(company)
                session.flush()
            
            # Save services
            session.query(Service).filter_by(company_id=company.id).delete()
            for service_name in company_data.get('services', []):
                if service_name and len(str(service_name).strip()) > 2:
                    service = Service(
                        company_id=company.id,
                        name=str(service_name)[:200]
                    )
                    session.add(service)
            
            # Save tech stack
            session.query(TechStack).filter_by(company_id=company.id).delete()
            for tech in company_data.get('tech_stack', []):
                if tech and len(str(tech).strip()) > 1:
                    tech_item = TechStack(
                        company_id=company.id,
                        technology=str(tech)[:100]
                    )
                    session.add(tech_item)
            
            # Save clients
            session.query(Client).filter_by(company_id=company.id).delete()
            clients = company_data.get('clients', {})
            if isinstance(clients, dict):
                client_names = clients.get('names', [])
            else:
                client_names = clients if isinstance(clients, list) else []
            
            for client_name in client_names:
                if client_name and len(str(client_name).strip()) > 2:
                    client = Client(
                        company_id=company.id,
                        name=str(client_name)[:200]
                    )
                    session.add(client)
            
            # Save projects
            session.query(Project).filter_by(company_id=company.id).delete()
            for project in company_data.get('projects', []):
                if isinstance(project, dict):
                    p = Project(
                        company_id=company.id,
                        name=str(project.get('name', ''))[:200],
                        description=str(project.get('description', ''))[:500],
                        client=str(project.get('client', ''))[:200]
                    )
                    session.add(p)
                elif isinstance(project, str) and len(project) > 5:
                    p = Project(
                        company_id=company.id,
                        name=project[:200],
                        description=project[:500]
                    )
                    session.add(p)
            
            session.commit()
            return company
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def save_report(self, company_id: int, report_data: dict, report_type: str = 'analysis'):
        """Save analysis report"""
        session = self.get_session()
        try:
            summary = ""
            if report_type == 'analysis':
                summary = report_data.get('executive_summary', {}).get('overview', '')
            else:
                summary = report_data.get('comparison', {}).get('summary', '')
            
            report = Report(
                company_id=company_id,
                report_type=report_type,
                data=report_data,
                summary=str(summary)[:500] if summary else "Analysis completed"
            )
            session.add(report)
            session.commit()
            return report
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def save_comparison_report(self, target_company_id: int, competitor_ids: list, report_data: dict):
        """Save comparison report"""
        session = self.get_session()
        try:
            report = ComparisonReport(
                target_company_id=target_company_id,
                competitor_ids=competitor_ids,
                report_data=report_data
            )
            session.add(report)
            session.commit()
            return report
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_company(self, company_id: int):
        """Get company by ID"""
        session = self.get_session()
        try:
            return session.query(Company).filter_by(id=company_id).first()
        finally:
            session.close()
    
    def get_company_by_url(self, url: str):
        """Get company by URL"""
        session = self.get_session()
        try:
            return session.query(Company).filter_by(url=url).first()
        finally:
            session.close()
    
    def get_all_companies(self):
        """Get all companies"""
        session = self.get_session()
        try:
            return session.query(Company).order_by(Company.name).all()
        finally:
            session.close()
    
    def get_reports(self, company_id: int = None):
        """Get reports"""
        session = self.get_session()
        try:
            query = session.query(Report)
            if company_id:
                query = query.filter_by(company_id=company_id)
            return query.order_by(Report.generated_at.desc()).all()
        finally:
            session.close()
    
    def get_comparison_reports(self):
        """Get all comparison reports"""
        session = self.get_session()
        try:
            return session.query(ComparisonReport).order_by(
                ComparisonReport.generated_at.desc()
            ).all()
        finally:
            session.close()
    
    def delete_company(self, company_id: int):
        """Delete company and all related data"""
        session = self.get_session()
        try:
            company = session.query(Company).filter_by(id=company_id).first()
            if company:
                session.delete(company)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def search_companies(self, query: str):
        """Search companies by name or URL"""
        session = self.get_session()
        try:
            search_term = f"%{query}%"
            return session.query(Company).filter(
                (Company.name.ilike(search_term)) | 
                (Company.url.ilike(search_term))
            ).limit(20).all()
        finally:
            session.close()

# Create singleton instance
db_manager = DatabaseManager()
