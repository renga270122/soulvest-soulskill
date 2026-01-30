# ai_assistant.py
# AI-Powered Resume Assistant using Google Gemini (Free API)

import os
import json
import re
from typing import Dict, List, Optional

# We'll use Google Gemini API (free tier) instead of OpenAI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIResumeAssistant:
    """AI-powered resume assistant for content generation and optimization"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if self.api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.enabled = True
        else:
            self.enabled = False
    
    def generate_professional_summary(self, profile_data: Dict) -> str:
        """Generate AI-powered professional summary"""
        if not self.enabled:
            return self._generate_fallback_summary(profile_data)
        
        try:
            profile_type = profile_data.get('profile_type', 'experienced')
            name = profile_data.get('full_name', 'Candidate')
            job_title = profile_data.get('job_title_target', 'Professional')
            industry = profile_data.get('industry', 'Technology')
            skills = profile_data.get('tech_skills', '') + ' ' + profile_data.get('soft_skills', '')
            
            prompt = f"""
            Generate a compelling professional summary for a {profile_type} professional's resume.
            
            Profile Details:
            - Target Role: {job_title}
            - Industry: {industry}
            - Key Skills: {skills}
            - Profile Type: {profile_type}
            
            Requirements:
            - 3-4 sentences maximum
            - ATS-friendly with relevant keywords
            - Highlight key strengths and career goals
            - Professional tone
            - For freshers: Focus on education, skills, and enthusiasm
            - For experienced: Focus on achievements and expertise
            
            Generate ONLY the summary text, no additional explanations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_summary(profile_data)
    
    def enhance_work_description(self, role: str, company: str, description: str) -> str:
        """Enhance work description with AI"""
        if not self.enabled:
            return description
        
        try:
            prompt = f"""
            Enhance this work experience description to be more impactful and ATS-friendly.
            
            Role: {role}
            Company: {company}
            Current Description: {description}
            
            Requirements:
            - Use action verbs (Led, Developed, Implemented, Managed, etc.)
            - Quantify achievements where possible
            - Make it concise and impactful
            - Include relevant industry keywords
            - Format as bullet points (3-5 points)
            - Each point should start with a strong action verb
            
            Generate ONLY the enhanced bullet points, no additional explanations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            return description
    
    def suggest_skills(self, job_title: str, industry: str, current_skills: str) -> List[str]:
        """Suggest relevant skills based on role and industry"""
        if not self.enabled:
            return []
        
        try:
            prompt = f"""
            Suggest 10 relevant technical and soft skills for this role that are commonly found in job descriptions.
            
            Job Title: {job_title}
            Industry: {industry}
            Current Skills: {current_skills}
            
            Requirements:
            - Mix of technical and soft skills
            - Industry-relevant keywords
            - ATS-friendly terms
            - Avoid skills already mentioned in current skills
            
            Provide ONLY a comma-separated list of skills, no explanations.
            """
            
            response = self.model.generate_content(prompt)
            skills_text = response.text.strip()
            skills = [s.strip() for s in skills_text.split(',')]
            return skills[:10]
        
        except Exception as e:
            return []
    
    def analyze_job_description(self, job_description: str) -> Dict:
        """Analyze job description and extract key information"""
        if not self.enabled:
            return self._basic_job_analysis(job_description)
        
        try:
            prompt = f"""
            Analyze this job description and extract key information.
            
            Job Description:
            {job_description}
            
            Extract and return in JSON format:
            {{
                "required_skills": ["skill1", "skill2", ...],
                "preferred_skills": ["skill1", "skill2", ...],
                "key_responsibilities": ["resp1", "resp2", ...],
                "experience_required": "X years",
                "education_required": "degree",
                "keywords": ["keyword1", "keyword2", ...]
            }}
            
            Return ONLY the JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            return result
        
        except Exception as e:
            return self._basic_job_analysis(job_description)
    
    def calculate_ats_score(self, resume_text: str, job_description: str) -> Dict:
        """Calculate ATS compatibility score"""
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        try:
            # Text similarity score
            vectorizer = CountVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform([job_description.lower(), resume_text.lower()])
            similarity = cosine_similarity(vectors)[0][1]
            
            # Extract keywords from job description
            job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower()))
            resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))
            
            # Common important words
            common_keywords = job_words & resume_words
            missing_keywords = job_words - resume_words
            
            # Filter to get most relevant missing keywords (longer words, technical terms)
            important_missing = [w for w in missing_keywords if len(w) > 4][:15]
            
            # Calculate detailed scores
            keyword_match = len(common_keywords) / len(job_words) if job_words else 0
            
            # Overall ATS score (weighted)
            ats_score = int((similarity * 0.6 + keyword_match * 0.4) * 100)
            
            # Check for ATS-friendly formatting
            formatting_issues = []
            if '<table>' in resume_text.lower():
                formatting_issues.append("Avoid complex tables")
            if len(resume_text) < 200:
                formatting_issues.append("Resume content too short")
            
            return {
                'score': ats_score,
                'similarity': round(similarity * 100, 1),
                'keyword_match': round(keyword_match * 100, 1),
                'matched_keywords': len(common_keywords),
                'total_job_keywords': len(job_words),
                'missing_keywords': important_missing,
                'formatting_issues': formatting_issues,
                'recommendation': self._get_score_recommendation(ats_score)
            }
        
        except Exception as e:
            return {
                'score': 0,
                'error': str(e),
                'recommendation': 'Unable to calculate score'
            }
    
    def _get_score_recommendation(self, score: int) -> str:
        """Get recommendation based on ATS score"""
        if score >= 80:
            return "Excellent! Your resume is highly ATS-compatible."
        elif score >= 60:
            return "Good match! Consider adding more relevant keywords."
        elif score >= 40:
            return "Fair match. Add more job-specific keywords and skills."
        else:
            return "Low match. Significantly revise to include job requirements."
    
    def _generate_fallback_summary(self, profile_data: Dict) -> str:
        """Generate basic summary without AI"""
        profile_type = profile_data.get('profile_type', 'experienced')
        job_title = profile_data.get('job_title_target', 'Professional')
        industry = profile_data.get('industry', 'Technology')
        
        if profile_type == 'fresher':
            return f"Motivated and enthusiastic {job_title} seeking to begin a career in {industry}. Strong academic background with hands-on experience in relevant technologies and eagerness to contribute to organizational success while developing professional skills."
        else:
            return f"Experienced {job_title} with proven expertise in {industry}. Demonstrated track record of delivering results through technical proficiency and strong problem-solving abilities. Seeking to leverage skills and experience to drive organizational growth."
    
    def _basic_job_analysis(self, job_description: str) -> Dict:
        """Basic keyword extraction without AI"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower())
        common_words = {'required', 'experience', 'skills', 'knowledge', 'ability', 'work', 'team', 'years'}
        keywords = [w for w in set(words) if w not in common_words][:20]
        
        return {
            'keywords': keywords,
            'required_skills': keywords[:10],
            'preferred_skills': [],
            'key_responsibilities': [],
            'experience_required': 'Not specified',
            'education_required': 'Not specified'
        }


class ATSOptimizer:
    """ATS Optimization helper"""
    
    @staticmethod
    def check_format_compatibility(resume_text: str) -> Dict:
        """Check if resume format is ATS-friendly"""
        issues = []
        recommendations = []
        
        # Check for problematic elements
        if '<table>' in resume_text:
            issues.append("Complex tables detected")
            recommendations.append("Use simple lists instead of tables")
        
        if 'text-align: center' in resume_text:
            issues.append("Centered text may confuse ATS")
            recommendations.append("Use left-aligned text for better parsing")
        
        # Check for good practices
        has_headings = bool(re.search(r'<h[1-6]>', resume_text))
        if not has_headings:
            issues.append("No proper heading structure")
            recommendations.append("Use clear section headings (Experience, Education, Skills)")
        
        # Check content length
        text_only = re.sub(r'<[^>]+>', '', resume_text)
        word_count = len(text_only.split())
        
        if word_count < 150:
            issues.append("Resume content too brief")
            recommendations.append("Add more details about your experience and skills")
        elif word_count > 1000:
            issues.append("Resume might be too lengthy")
            recommendations.append("Keep it concise - aim for 400-800 words")
        
        compatibility_score = max(0, 100 - (len(issues) * 15))
        
        return {
            'score': compatibility_score,
            'issues': issues,
            'recommendations': recommendations,
            'word_count': word_count,
            'status': 'Excellent' if compatibility_score >= 80 else 'Good' if compatibility_score >= 60 else 'Needs Improvement'
        }
    
    @staticmethod
    def suggest_section_names() -> Dict[str, List[str]]:
        """Standard ATS-friendly section names"""
        return {
            'professional_summary': ['Professional Summary', 'Summary', 'Profile', 'Career Objective'],
            'experience': ['Work Experience', 'Professional Experience', 'Experience', 'Employment History'],
            'education': ['Education', 'Academic Background', 'Qualifications'],
            'skills': ['Skills', 'Technical Skills', 'Core Competencies', 'Key Skills'],
            'certifications': ['Certifications', 'Professional Certifications', 'Licenses'],
            'projects': ['Projects', 'Key Projects', 'Notable Projects'],
            'achievements': ['Achievements', 'Accomplishments', 'Awards']
        }
    
    @staticmethod
    def get_action_verbs() -> List[str]:
        """Return ATS-friendly action verbs"""
        return [
            'Achieved', 'Administered', 'Analyzed', 'Collaborated', 'Conducted',
            'Coordinated', 'Created', 'Delivered', 'Designed', 'Developed',
            'Directed', 'Established', 'Executed', 'Facilitated', 'Generated',
            'Implemented', 'Improved', 'Increased', 'Initiated', 'Led',
            'Managed', 'Optimized', 'Organized', 'Performed', 'Planned',
            'Produced', 'Reduced', 'Resolved', 'Streamlined', 'Supervised'
        ]
