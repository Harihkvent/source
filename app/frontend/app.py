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
    
    # Check if we need to force a specific page based on user actions
    if "page" in st.session_state:
        current_page = st.session_state.page
        # Clear the page state so we don't get stuck
        del st.session_state.page
    else:
        current_page = "Resume Parser"
    
    # Check if we already have a profile parsed - if so, show the navigation sidebar
    if "profile" in st.session_state:
        # Sidebar
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Select a page:", 
                              ["Resume Parser", "Job Recommendations", "Skill Roadmap"],
                              index=["Resume Parser", "Job Recommendations", "Skill Roadmap"].index(current_page))
        
        # Pages
        if page == "Resume Parser":
            display_resume_parser()
        elif page == "Job Recommendations":
            display_job_recommendations()
        elif page == "Skill Roadmap":
            display_skill_roadmap()
    else:
        # If no profile is parsed yet, only show the resume parser
        display_resume_parser()

def display_resume_parser():
    # Check if we're showing a previously parsed profile or a new upload
    if "profile" in st.session_state and not st.sidebar.button("Upload New Resume"):
        st.header("Extracted Resume Information")
        st.info("Your resume has been successfully parsed. You can view recommendations in the sidebar navigation or upload a new resume.")
        
        # Add a download button for the extracted profile as JSON
        profile_json = json.dumps(st.session_state.profile, indent=2)
        st.download_button(
            label="Download Profile Data (JSON)",
            data=profile_json,
            file_name="my_profile.json",
            mime="application/json"
        )
        
        # Display the parsed profile information prominently
        display_profile(st.session_state.profile)
        
        # Add buttons for next steps
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Get Job Recommendations"):
                st.session_state.page = "Job Recommendations"
                st.experimental_rerun()
        with col2:
            if st.button("Upload Different Resume"):
                del st.session_state.profile
                st.experimental_rerun()
    else:
        # New upload flow
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
                            st.balloons()  # Add a fun effect for successful parsing
                            
                            # Display extracted information prominently
                            display_profile(profile_data)
                            
                            # Add a button to proceed to recommendations
                            if st.button("View Job Recommendations"):
                                st.session_state.page = "Job Recommendations"
                                st.experimental_rerun()
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
    """Display the parsed profile information in a simple, direct format"""
    st.header("Extracted Content from Resume")
    
    # Display the raw text of the resume first
    st.subheader("Full Resume Text")
    if profile.get('raw_text'):
        st.text_area("Resume Content:", profile.get('raw_text'), height=300)
    else:
        st.write("No raw text content available")
    
    st.subheader("Extracted Information")
    
    # Personal Information - simple text display
    st.write("### Personal Details")
    st.write(f"Name: {profile.get('name', 'Not detected')}")
    st.write(f"Email: {profile.get('email', 'Not detected')}")
    st.write(f"Phone: {profile.get('phone', 'Not detected')}")
    if profile.get('address'):
        st.write(f"Address: {profile.get('address')}")
    
    # Skills - simple list
    st.write("### Skills Detected")
    if profile.get('skills'):
        for skill in profile.get('skills', []):
            st.write(f"- {skill}")
    else:
        st.write("No skills were detected in the resume")
    
    # Education - simple text without formatting
    if profile.get('education'):
        st.write("### Education")
        for edu in profile.get('education', []):
            st.write(f"Degree: {edu.get('degree', 'Not specified')}")
            st.write(f"Institution: {edu.get('institution', 'Not specified')}")
            if edu.get('start_date'):
                st.write(f"Start Date: {edu.get('start_date')}")
            if edu.get('end_date'):
                st.write(f"End Date: {edu.get('end_date')}")
            if edu.get('description'):
                st.write(f"Description: {edu.get('description')}")
            st.write("---")
    
    # Experience - simple text without formatting
    if profile.get('experience'):
        st.write("### Work Experience")
        for exp in profile.get('experience', []):
            st.write(f"Role: {exp.get('role', 'Not specified')}")
            st.write(f"Company: {exp.get('company', 'Not specified')}")
            if exp.get('start_date'):
                st.write(f"Start Date: {exp.get('start_date')}")
            if exp.get('end_date'):
                st.write(f"End Date: {exp.get('end_date')}")
            if exp.get('description'):
                st.write(f"Description: {exp.get('description')}")
            st.write("---")
    
    # Projects - simple text without formatting
    if profile.get('projects'):
        st.write("### Projects")
        for proj in profile.get('projects', []):
            st.write(f"Name: {proj.get('name', 'Not specified')}")
            if proj.get('technologies'):
                st.write(f"Technologies: {', '.join(proj.get('technologies', []))}")
            if proj.get('description'):
                st.write(f"Description: {proj.get('description')}")
            st.write("---")
    
    # Display the full JSON for developers
    with st.expander("View Full Extracted JSON Data"):
        st.json(profile)

if __name__ == "__main__":
    main()