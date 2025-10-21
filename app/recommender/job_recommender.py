from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class JobRecommender:
    """
    A simple job recommender using TF-IDF and Nearest Neighbors
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            stop_words='english'
        )
        self.jobs = []
        self.job_vecs = None
        self.nn_model = None
    
    def load_jobs(self, jobs: List[Dict[str, Any]]):
        """Load job data into the recommender"""
        self.jobs = jobs
        
        # Create job texts for vectorization
        job_texts = []
        for job in self.jobs:
            # Combine relevant job fields into a single text
            text = f"{job['title']} {job['company']} {job['description']} {' '.join(job['required_skills'])}"
            job_texts.append(text)
        
        # Vectorize job texts
        self.job_vecs = self.vectorizer.fit_transform(job_texts)
        
        # Fit nearest neighbors model
        self.nn_model = NearestNeighbors(
            n_neighbors=min(50, len(self.jobs)),
            metric='cosine'
        ).fit(self.job_vecs)
    
    def recommend(self, profile: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend jobs for a given profile
        
        Args:
            profile: A parsed user profile
            limit: Maximum number of recommendations to return
        
        Returns:
            A list of recommended jobs with match scores
        """
        if not self.jobs or self.nn_model is None:
            return []
        
        # Create profile text
        profile_text = f"{' '.join(profile['skills'])} {' '.join([edu['degree'] for edu in profile['education']])}"
        for exp in profile['experience']:
            profile_text += f" {exp['role']} {exp['company']}"
        
        # Vectorize profile text
        profile_vec = self.vectorizer.transform([profile_text])
        
        # Find nearest neighbors
        distances, indices = self.nn_model.kneighbors(profile_vec)
        
        # Convert distances to scores (1 - distance, since cosine distance is used)
        scores = 1 - distances.flatten()
        
        # Create recommendations list
        recommendations = []
        for i, idx in enumerate(indices.flatten()):
            if i >= limit:
                break
            
            job = self.jobs[idx]
            
            # Determine matched and missing skills
            matched_skills = []
            missing_skills = []
            
            profile_skills = [skill.lower() for skill in profile['skills']]
            for skill in job['required_skills']:
                if skill.lower() in profile_skills:
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)
            
            # Add to recommendations list
            recommendations.append({
                'job_id': job['id'],
                'title': job['title'],
                'company': job['company'],
                'match_score': float(scores[i]),
                'skills_matched': matched_skills,
                'skills_missing': missing_skills
            })
        
        return recommendations

# Sample code to load and use the recommender
def get_sample_jobs():
    """Get sample job data for demonstration"""
    return [
        {
            'id': '1',
            'title': 'Software Engineer',
            'company': 'Tech Co',
            'description': 'Build and maintain backend systems using Python and FastAPI.',
            'required_skills': ['python', 'fastapi', 'sql', 'docker']
        },
        {
            'id': '2',
            'title': 'Data Analyst',
            'company': 'Data Insights Inc',
            'description': 'Analyze data and create visualizations using Python and BI tools.',
            'required_skills': ['python', 'sql', 'tableau', 'powerbi']
        },
        {
            'id': '3',
            'title': 'Frontend Developer',
            'company': 'WebDev Solutions',
            'description': 'Create responsive web applications using React and TypeScript.',
            'required_skills': ['javascript', 'typescript', 'react', 'css']
        }
    ]

# Usage example
if __name__ == "__main__":
    recommender = JobRecommender()
    recommender.load_jobs(get_sample_jobs())
    
    sample_profile = {
        'name': 'John Doe',
        'skills': ['python', 'sql', 'javascript'],
        'education': [{'degree': 'Computer Science', 'institution': 'Example University'}],
        'experience': [{'role': 'Junior Developer', 'company': 'Small Tech Inc'}]
    }
    
    recommendations = recommender.recommend(sample_profile)
    print(recommendations)