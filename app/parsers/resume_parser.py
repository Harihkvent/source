import os
import re
import pytesseract
from pdf2image import convert_from_path
import spacy
from spacy.matcher import PhraseMatcher
import docx
from PyPDF2 import PdfReader

from app.models.profile import Profile, Education, Experience, Project

class ResumeParser:
    """
    A class to parse resumes in different formats (PDF, DOCX, image)
    and extract structured information using Tesseract OCR and spaCy.
    """
    
    def __init__(self, file_path):
        """
        Initialize with a file path to the resume
        """
        self.file_path = file_path
        self.file_ext = os.path.splitext(file_path)[1].lower()
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model is not downloaded, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], 
                           capture_output=True)
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize skill matcher
        self.skill_list = self._load_skills()
        self.skill_matcher = self._create_skill_matcher()
    
    def _load_skills(self):
        """Load a list of common skills from a predefined list"""
        # This is a simple list of skills for demonstration
        # In a real implementation, this would be loaded from a JSON file or database
        return [
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin",
            "sql", "mysql", "postgresql", "mongodb", "oracle", "nosql", "firebase",
            "react", "angular", "vue", "svelte", "jquery", "node.js", "express.js", "django", "flask",
            "fastapi", "spring boot", "laravel", "rails", "asp.net",
            "html", "css", "sass", "less", "bootstrap", "tailwind", "material ui",
            "docker", "kubernetes", "aws", "azure", "gcp", "heroku", "digitalocean", "terraform",
            "git", "github", "gitlab", "bitbucket", "ci/cd", "jenkins", "travis ci", "github actions",
            "machine learning", "deep learning", "data science", "natural language processing", 
            "computer vision", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib",
            "tableau", "power bi", "excel", "powerpoint", "word", "outlook", "office365",
            "agile", "scrum", "kanban", "jira", "confluence", "trello", "asana", "slack"
        ]
    
    def _create_skill_matcher(self):
        """Create a spaCy PhraseMatcher for skills"""
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in self.skill_list]
        matcher.add("SKILLS", patterns)
        return matcher
    
    def parse(self):
        """
        Parse the resume file and extract information into a Profile object
        """
        # Extract text from file
        text = self._extract_text()
        
        # Create an empty profile
        profile = Profile(raw_text=text)
        
        # Extract basic information
        profile.name = self._extract_name(text)
        profile.email = self._extract_email(text)
        profile.phone = self._extract_phone(text)
        
        # Extract skills
        profile.skills = self._extract_skills(text)
        
        # Extract education
        profile.education = self._extract_education(text)
        
        # Extract experience
        profile.experience = self._extract_experience(text)
        
        return profile
    
    def _extract_text(self):
        """Extract text from different file formats"""
        if self.file_ext == '.pdf':
            return self._extract_text_from_pdf()
        elif self.file_ext == '.docx':
            return self._extract_text_from_docx()
        elif self.file_ext in ['.jpg', '.jpeg', '.png']:
            return self._extract_text_from_image()
        else:
            raise ValueError(f"Unsupported file format: {self.file_ext}")
    
    def _extract_text_from_pdf(self):
        """Extract text from PDF using PyPDF2 first, then OCR if needed"""
        # Try to extract text directly from PDF
        reader = PdfReader(self.file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # If no text was extracted (scanned PDF), use OCR
        if not text.strip():
            pages = convert_from_path(self.file_path, dpi=300)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
        
        return text
    
    def _extract_text_from_docx(self):
        """Extract text from DOCX"""
        doc = docx.Document(self.file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    def _extract_text_from_image(self):
        """Extract text from image using OCR"""
        from PIL import Image
        image = Image.open(self.file_path)
        return pytesseract.image_to_string(image)
    
    def _extract_name(self, text):
        """Extract candidate name from text"""
        # This is a simple extraction method
        # In a real implementation, use more sophisticated NER
        lines = text.split('\n')
        # Assume the name is in the first few lines and is capitalized
        for i in range(min(5, len(lines))):
            line = lines[i].strip()
            if line and line == line.upper() or (len(line.split()) <= 3 and all(word[0].isupper() for word in line.split() if word)):
                return line
        return None
    
    def _extract_email(self, text):
        """Extract email using regex"""
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def _extract_phone(self, text):
        """Extract phone number using regex"""
        # Match different phone number formats
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def _extract_skills(self, text):
        """Extract skills using spaCy matcher"""
        doc = self.nlp(text)
        matches = self.skill_matcher(doc)
        skills = []
        for match_id, start, end in matches:
            skill = doc[start:end].text.lower()
            if skill not in skills:
                skills.append(skill)
        return skills
    
    def _extract_education(self, text):
        """Extract education information"""
        # In a real implementation, this would be more sophisticated
        # Simple implementation for demonstration purposes
        education_sections = self._find_sections(text, ["EDUCATION", "ACADEMIC BACKGROUND"])
        if not education_sections:
            return []
        
        education_list = []
        # Very basic extraction logic for demonstration
        lines = education_sections.split('\n')
        current_edu = None
        
        for line in lines:
            if "degree" in line.lower() or "bachelor" in line.lower() or "master" in line.lower() or "phd" in line.lower():
                if current_edu:
                    education_list.append(current_edu)
                current_edu = Education(degree=line.strip(), institution="")
            elif current_edu and not current_edu.institution and line.strip():
                current_edu.institution = line.strip()
        
        if current_edu:
            education_list.append(current_edu)
        
        return education_list
    
    def _extract_experience(self, text):
        """Extract work experience information"""
        # Simple implementation for demonstration
        experience_sections = self._find_sections(text, ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT"])
        if not experience_sections:
            return []
        
        experience_list = []
        # This is a placeholder for demonstration
        # A real implementation would be more sophisticated
        
        return experience_list
    
    def _find_sections(self, text, section_headers):
        """Find sections in text based on common headers"""
        text_lower = text.lower()
        section_text = ""
        
        for header in section_headers:
            header_lower = header.lower()
            if header_lower in text_lower:
                # Find the start of the section
                start_idx = text_lower.find(header_lower)
                
                # Find the end of the section (start of the next section)
                end_idx = len(text)
                common_headers = ["education", "experience", "skills", "projects", 
                                 "employment", "work", "academic", "certification", 
                                 "awards", "publications", "languages"]
                
                for next_header in common_headers:
                    next_idx = text_lower.find(next_header, start_idx + len(header_lower))
                    if next_idx > start_idx and next_idx < end_idx:
                        end_idx = next_idx
                
                section_text = text[start_idx:end_idx].strip()
                break
        
        return section_text