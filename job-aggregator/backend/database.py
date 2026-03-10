from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    description = Column(Text)
    url = Column(String, unique=True)
    posted_date = Column(String)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    source = Column(String, default="sample")  # "sample", "linkedin", "greenhouse", "lever"
    experience_level = Column(String, nullable=True)  # "entry", "mid", "senior", "lead", "principal"
    scraped_at = Column(DateTime, default=datetime.utcnow)

import os

# Ensure database directory exists
db_path = os.path.join(os.path.dirname(__file__), "jobs.db")
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
