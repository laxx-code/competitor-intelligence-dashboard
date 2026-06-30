"""
Database Models for PostgreSQL
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from sqlalchemy.pool import NullPool
import os

Base = declarative_base()

class Company(Base):
    """Company information"""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    founded_year = Column(String(10))
    about = Column(Text)
    team_size = Column(Integer)
    location = Column(String(200))
    industry = Column(JSON)  # List of industries
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    services = relationship("Service", back_populates="company", cascade="all, delete-orphan")
    tech_stack = relationship("TechStack", back_populates="company", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="company", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="company", cascade="all, delete-orphan")

class Service(Base):
    """Services offered by companies"""
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    company = relationship("Company", back_populates="services")

class TechStack(Base):
    """Technologies used by companies"""
    __tablename__ = 'tech_stack'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    technology = Column(String(100), nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    
    company = relationship("Company", back_populates="tech_stack")

class Client(Base):
    """Clients of companies"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    
    company = relationship("Company", back_populates="clients")

class Project(Base):
    """Projects of companies"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    name = Column(String(200))
    description = Column(Text)
    client = Column(String(200))
    start_date = Column(String(20))
    end_date = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    
    company = relationship("Company", back_populates="projects")

class Report(Base):
    """Analysis reports"""
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    report_type = Column(String(50))  # 'analysis', 'comparison'
    data = Column(JSON)  # Full report data
    summary = Column(Text)
    generated_at = Column(DateTime, default=datetime.now)
    
    company = relationship("Company", back_populates="reports")

class ComparisonReport(Base):
    """Competitor comparison reports"""
    __tablename__ = 'comparison_reports'
    
    id = Column(Integer, primary_key=True)
    target_company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    competitor_ids = Column(JSON)  # List of competitor company IDs
    report_data = Column(JSON)  # Full comparison data
    generated_at = Column(DateTime, default=datetime.now)
    
    target_company = relationship("Company", foreign_keys=[target_company_id])

def get_db_url():
    """Get database URL from environment or use default"""
    db_user = os.getenv('DB_USER', 'competitor_user')
    db_password = os.getenv('DB_PASSWORD', 'competitor_pass123')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'competitor_intelligence')
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def init_db(db_url: str = None):
    """Initialize database"""
    if not db_url:
        db_url = get_db_url()
    
    print(f"📡 Connecting to database: {db_url}")
    engine = create_engine(db_url, poolclass=NullPool)
    Base.metadata.create_all(engine)
    print("✅ Database tables created/verified")
    return engine
