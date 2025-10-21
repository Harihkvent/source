from pydantic import BaseModel
from typing import List, Optional, Dict

class Education(BaseModel):
    degree: str
    institution: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class Experience(BaseModel):
    role: str
    company: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Profile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: List[str] = []
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    raw_text: Optional[str] = None