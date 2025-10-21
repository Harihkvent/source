from typing import List, Dict, Any

class RoadmapGenerator:
    """
    A simple class to generate skill roadmaps for career development
    """
    
    def __init__(self):
        # Initialize with skill resources database
        self.skill_resources = self._load_skill_resources()
        
    def _load_skill_resources(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Load skill resources database
        In a real implementation, this would come from a database or file
        """
        return {
            "python": [
                {"title": "Python Documentation", "url": "https://docs.python.org/3/"},
                {"title": "Learn Python - Codecademy", "url": "https://www.codecademy.com/learn/learn-python-3"}
            ],
            "sql": [
                {"title": "SQL Tutorial - W3Schools", "url": "https://www.w3schools.com/sql/"},
                {"title": "SQL for Data Analysis - Udacity", "url": "https://www.udacity.com/course/sql-for-data-analysis--ud198"}
            ],
            "docker": [
                {"title": "Docker Documentation", "url": "https://docs.docker.com/"},
                {"title": "Docker for Beginners", "url": "https://docker-curriculum.com/"}
            ],
            "fastapi": [
                {"title": "FastAPI Documentation", "url": "https://fastapi.tiangolo.com/"},
                {"title": "Building APIs with FastAPI - Real Python", "url": "https://realpython.com/fastapi-python-web-apis/"}
            ],
            "react": [
                {"title": "React Documentation", "url": "https://reactjs.org/docs/getting-started.html"},
                {"title": "React Tutorial - W3Schools", "url": "https://www.w3schools.com/react/"}
            ],
            "javascript": [
                {"title": "JavaScript Documentation - MDN", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"},
                {"title": "JavaScript Tutorial - W3Schools", "url": "https://www.w3schools.com/js/"}
            ],
            "tableau": [
                {"title": "Tableau Learning", "url": "https://www.tableau.com/learn"},
                {"title": "Tableau Tutorial - Tutorialspoint", "url": "https://www.tutorialspoint.com/tableau/"}
            ],
            "powerbi": [
                {"title": "Power BI Documentation", "url": "https://docs.microsoft.com/en-us/power-bi/"},
                {"title": "Power BI Training", "url": "https://powerbi.microsoft.com/en-us/learning/"}
            ]
        }
    
    def generate(self, profile: Dict[str, Any], job: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate a skill roadmap for a profile and job
        
        Args:
            profile: User profile data
            job: Job posting data
            
        Returns:
            List of roadmap items with skills to learn and resources
        """
        roadmap = []
        
        # Get profile skills
        profile_skills = [skill.lower() for skill in profile.get('skills', [])]
        
        # Get missing skills from job
        for skill in job.get('skills_missing', []):
            skill_lower = skill.lower()
            
            # Skip if the person already has this skill
            if skill_lower in profile_skills:
                continue
            
            # Determine priority based on how common the skill is in job requirements
            # In a real implementation, this would use more sophisticated scoring
            priority = "high" if skill_lower in ["python", "sql", "javascript"] else "medium"
            
            # Estimate time to learn based on complexity
            # In a real implementation, this would be more data-driven
            time_estimates = {
                "python": "4 weeks",
                "sql": "3 weeks",
                "javascript": "4 weeks",
                "react": "3 weeks",
                "docker": "2 weeks",
                "fastapi": "1 week",
                "tableau": "2 weeks",
                "powerbi": "2 weeks"
            }
            time_estimate = time_estimates.get(skill_lower, "2 weeks")
            
            # Find resources for this skill
            resources = self.skill_resources.get(skill_lower, [
                {"title": f"Search for {skill} tutorials", "url": f"https://www.google.com/search?q={skill}+tutorials"}
            ])
            
            # Add to roadmap
            roadmap.append({
                "skill": skill,
                "priority": priority,
                "time_estimate": time_estimate,
                "resources": resources
            })
        
        # Sort roadmap by priority (high to low)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        roadmap.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return roadmap