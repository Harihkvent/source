from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Float, DateTime, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    profiles = relationship("Profile", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    raw_text = Column(Text)
    skills = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="profiles")
    educations = relationship("Education", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile")
    projects = relationship("Project", back_populates="profile")


class Education(Base):
    __tablename__ = "educations"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    degree = Column(String)
    institution = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(Text)
    
    profile = relationship("Profile", back_populates="educations")


class Experience(Base):
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    role = Column(String)
    company = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(Text)
    
    profile = relationship("Profile", back_populates="experiences")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    name = Column(String)
    description = Column(Text)
    technologies = Column(JSON)
    start_date = Column(String)
    end_date = Column(String)
    
    profile = relationship("Profile", back_populates="projects")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    required_skills = Column(JSON)
    preferred_skills = Column(JSON)
    min_experience = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    aliases = Column(JSON)
    category = Column(String)
    popularity = Column(Integer)


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    match_score = Column(Float)
    skills_matched = Column(JSON)
    skills_missing = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    roadmap_items = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Create the database and tables
def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    return engine