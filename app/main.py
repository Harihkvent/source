from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
from typing import List

from app.parsers.resume_parser import ResumeParser
from app.models.profile import Profile

app = FastAPI(title="Practical Career Navigator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Career Navigator API"}

@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse a resume file (PDF, DOCX) and extract structured information
    """
    # Create a temporary file to store the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        # Write content to the temporary file
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        # Parse the resume
        parser = ResumeParser(tmp_path)
        profile = parser.parse()
        
        # Remove the temporary file
        os.unlink(tmp_path)
        
        # Return the parsed profile
        return profile.dict()
    except Exception as e:
        # Remove the temporary file in case of error
        os.unlink(tmp_path)
        return {"error": str(e)}

@app.post("/recommend-jobs/")
async def recommend_jobs(profile_id: str = Form(...), limit: int = Form(5)):
    """
    Recommend jobs based on a parsed profile
    """
    # For demonstration purposes, return placeholder data
    return {
        "profile_id": profile_id,
        "recommendations": [
            {
                "job_id": "1",
                "title": "Software Engineer",
                "company": "Tech Co",
                "match_score": 0.85,
                "skills_matched": ["python", "fastapi", "sql"],
                "skills_missing": ["docker"]
            },
            {
                "job_id": "2",
                "title": "Data Analyst",
                "company": "Data Insights Inc",
                "match_score": 0.72,
                "skills_matched": ["python", "sql"],
                "skills_missing": ["tableau", "powerbi"]
            }
        ]
    }

@app.get("/roadmap/{profile_id}/{job_id}")
def generate_roadmap(profile_id: str, job_id: str):
    """
    Generate a skill roadmap for a specific profile and job
    """
    # Placeholder roadmap data
    return {
        "profile_id": profile_id,
        "job_id": job_id,
        "roadmap": [
            {
                "skill": "Docker",
                "priority": "high",
                "time_estimate": "2 weeks",
                "resources": [
                    {"title": "Docker Documentation", "url": "https://docs.docker.com/"},
                    {"title": "Docker for Beginners", "url": "https://docker-curriculum.com/"}
                ]
            },
            {
                "skill": "FastAPI",
                "priority": "medium",
                "time_estimate": "1 week",
                "resources": [
                    {"title": "FastAPI Documentation", "url": "https://fastapi.tiangolo.com/"}
                ]
            }
        ]
    }