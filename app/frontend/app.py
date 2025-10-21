import streamlit as st
import requests
import json
import pandas as pd
import os
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="Career Navigator",
    page_icon="📝",
    layout="wide"
)

# Define the API endpoint
API_URL = "http://localhost:8000"

def main():
    st.title("Practical Career Navigator")
    st.write("Upload your resume and get personalized job recommendations and a skill roadmap.")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Resume Parser", "Job Recommendations", "Skill Roadmap"])
    
    # Pages
    if page == "Resume Parser":
        display_resume_parser()
    elif page == "Job Recommendations":
        display_job_recommendations()
    elif page == "Skill Roadmap":
        display_skill_roadmap()

def display_resume_parser():
    st.header("Resume Parser")
    st.write("Upload your resume to extract information.")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded file
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.2f} KB"}
        st.write(file_details)
        
        # Parse button
        if st.button("Parse Resume"):
            with st.spinner("Parsing resume..."):
                try:
                    # Submit file to API
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/parse-resume/", files=files)
                    
                    if response.status_code == 200:
                        profile_data = response.json()
                        st.session_state.profile = profile_data
                        
                        # Display parsed information
                        st.success("Resume parsed successfully!")
                        display_profile(profile_data)
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

def display_job_recommendations():
    st.header("Job Recommendations")
    
    if "profile" not in st.session_state:
        st.warning("Please parse your resume first in the Resume Parser tab.")
        return
    
    profile = st.session_state.profile
    
    # Display basic profile info
    st.subheader(f"Recommendations for {profile.get('name', 'you')}")
    
    with st.spinner("Getting job recommendations..."):
        try:
            # For demonstration purposes, use a mock API call
            # In a real application, you would make an actual API call
            recommendations = [
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
            
            # Display recommendations
            for job in recommendations:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"{job['title']} - {job['company']}")
                    st.write(f"**Match Score:** {job['match_score'] * 100:.1f}%")
                    st.write(f"**Matched Skills:** {', '.join(job['skills_matched'])}")
                    st.write(f"**Missing Skills:** {', '.join(job['skills_missing'])}")
                
                with col2:
                    if st.button("View Roadmap", key=f"roadmap_{job['job_id']}"):
                        st.session_state.selected_job = job
                        st.session_state.page = "Skill Roadmap"
                        st.experimental_rerun()
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def display_skill_roadmap():
    st.header("Skill Roadmap")
    
    if "profile" not in st.session_state:
        st.warning("Please parse your resume first in the Resume Parser tab.")
        return
    
    if "selected_job" not in st.session_state:
        st.warning("Please select a job recommendation first.")
        return
    
    job = st.session_state.selected_job
    
    st.subheader(f"Roadmap for {job['title']} at {job['company']}")
    
    # Mock roadmap data
    roadmap = [
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
    
    for item in roadmap:
        st.markdown(f"### {item['skill']}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"**Priority:** {item['priority'].capitalize()}")
        with col2:
            st.write(f"**Time Estimate:** {item['time_estimate']}")
        
        st.write("**Resources:**")
        for resource in item['resources']:
            st.markdown(f"- [{resource['title']}]({resource['url']})")
        
        st.write("---")

def display_profile(profile):
    """Display the parsed profile information"""
    st.subheader("Parsed Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {profile.get('name', 'N/A')}")
        st.write(f"**Email:** {profile.get('email', 'N/A')}")
        st.write(f"**Phone:** {profile.get('phone', 'N/A')}")
    
    with col2:
        if profile.get('skills'):
            st.write("**Skills:**")
            skills_df = pd.DataFrame({"Skills": profile['skills']})
            st.dataframe(skills_df)
    
    # Education
    if profile.get('education'):
        st.subheader("Education")
        for edu in profile['education']:
            st.write(f"**{edu.get('degree', 'Degree')}** - {edu.get('institution', 'Institution')}")
            if edu.get('start_date') and edu.get('end_date'):
                st.write(f"{edu['start_date']} - {edu['end_date']}")
    
    # Experience
    if profile.get('experience'):
        st.subheader("Experience")
        for exp in profile['experience']:
            st.write(f"**{exp.get('role', 'Role')}** - {exp.get('company', 'Company')}")
            if exp.get('start_date') and exp.get('end_date'):
                st.write(f"{exp['start_date']} - {exp['end_date']}")
            if exp.get('description'):
                st.write(exp['description'])
            st.write("---")

if __name__ == "__main__":
    main()