# ai_advanced.py
# Advanced AI Features - Competing with Kickresume, Rezi, Novoresume
# Features: Cover Letters, Career Advice, Job Matching, LinkedIn Optimization

import os
import re
from typing import Dict, List, Optional, Tuple
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AdvancedAIAssistant:
    """Advanced AI features matching top resume builders in 2026"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.enabled = False  # Default to False
        
        try:
            if self.api_key and GEMINI_AVAILABLE:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.enabled = True
        except Exception:
            self.enabled = False
    
    def generate_cover_letter(self, resume_data: Dict, job_description: str, company_name: str = "") -> str:
        """Generate personalized cover letter matching job description"""
        if not self.enabled:
            return self._generate_fallback_cover_letter(resume_data, company_name)
        
        try:
            name = resume_data.get('full_name', 'Your Name')
            target_role = resume_data.get('job_title_target', 'the position')
            experience = resume_data.get('work_history', [])
            skills = resume_data.get('tech_skills', '') + ' ' + resume_data.get('soft_skills', '')
            
            prompt = f"""
            Generate a compelling cover letter that sounds natural and personalized, not robotic.
            
            Candidate Info:
            - Name: {name}
            - Target Role: {target_role}
            - Skills: {skills}
            - Company: {company_name or 'the company'}
            
            Job Description:
            {job_description[:1500]}
            
            Requirements:
            - 3-4 paragraphs maximum
            - Start with genuine enthusiasm about the role/company
            - Highlight 2-3 relevant achievements or skills that match the job
            - Show personality while maintaining professionalism
            - End with a confident call to action
            - Sound human, not AI-generated
            - Use active voice and strong action verbs
            - Avoid clichés like "I am writing to express my interest"
            - Make it ATS-friendly with relevant keywords
            
            Format: Professional business letter style
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return self._generate_fallback_cover_letter(resume_data, company_name)
    
    def get_career_advice(self, profile_data: Dict, career_goal: str) -> Dict[str, any]:
        """Provide AI-driven career advice and roadmap"""
        if not self.enabled:
            return self._generate_fallback_career_advice(profile_data, career_goal)
        
        try:
            current_role = profile_data.get('job_title_target', 'Professional')
            industry = profile_data.get('industry', 'Technology')
            experience_years = len(profile_data.get('work_history', []))
            skills = profile_data.get('tech_skills', '') + ' ' + profile_data.get('soft_skills', '')
            
            prompt = f"""
            Provide strategic career advice for a professional looking to advance their career.
            
            Current Profile:
            - Current/Target Role: {current_role}
            - Industry: {industry}
            - Years of Experience: {experience_years}
            - Skills: {skills}
            - Career Goal: {career_goal}
            
            Provide detailed advice in JSON format:
            {{
                "next_roles": ["3-5 realistic next career steps"],
                "skills_to_develop": ["5-7 in-demand skills they should learn"],
                "certifications": ["3-4 relevant certifications"],
                "timeline": "Realistic timeline for career transition (e.g., 6-12 months)",
                "action_plan": ["5 concrete steps to take"],
                "market_trends": "Brief analysis of industry trends",
                "salary_range": "Expected salary range for target role",
                "networking_tips": ["3 networking strategies"]
            }}
            
            Be specific, actionable, and realistic.
            """
            
            response = self.model.generate_content(prompt)
            # Try to parse JSON from response
            try:
                advice = json.loads(response.text.strip())
            except:
                # If JSON parsing fails, return structured fallback
                advice = self._parse_career_advice_text(response.text)
            
            return advice
            
        except Exception as e:
            return self._generate_fallback_career_advice(profile_data, career_goal)
    
    def match_job_description(self, resume_data: Dict, job_description: str) -> Dict[str, any]:
        """Match resume against job description and provide detailed analysis"""
        if not self.enabled:
            return self._generate_fallback_job_match(resume_data, job_description)
        
        try:
            prompt = f"""
            Analyze how well this candidate matches the job requirements.
            
            Candidate Profile:
            - Role: {resume_data.get('job_title_target', 'N/A')}
            - Skills: {resume_data.get('tech_skills', '')} {resume_data.get('soft_skills', '')}
            - Experience: {len(resume_data.get('work_history', []))} positions
            
            Job Description:
            {job_description[:2000]}
            
            Provide detailed analysis in JSON format:
            {{
                "overall_match_score": 85,
                "match_level": "Excellent Match / Good Match / Moderate Match / Weak Match",
                "strengths": ["3-5 strong matching points"],
                "gaps": ["2-4 areas where candidate doesn't match"],
                "missing_keywords": ["5-10 important keywords not in resume"],
                "recommended_additions": ["3-5 specific things to add to resume"],
                "interview_prep_tips": ["3 tips for interview based on job requirements"],
                "resume_improvements": ["3-5 specific resume improvements to make"],
                "confidence_assessment": "How confident should candidate be applying (High/Medium/Low)"
            }}
            
            Be honest and constructive.
            """
            
            response = self.model.generate_content(prompt)
            try:
                analysis = json.loads(response.text.strip())
            except:
                analysis = self._parse_job_match_text(response.text)
            
            return analysis
            
        except Exception as e:
            return self._generate_fallback_job_match(resume_data, job_description)
    
    def optimize_linkedin_profile(self, resume_data: Dict) -> Dict[str, str]:
        """Generate LinkedIn profile optimization suggestions"""
        if not self.enabled:
            return self._generate_fallback_linkedin_tips(resume_data)
        
        try:
            prompt = f"""
            Generate LinkedIn profile optimization content for this professional.
            
            Profile:
            - Name: {resume_data.get('full_name', 'Candidate')}
            - Role: {resume_data.get('job_title_target', 'Professional')}
            - Industry: {resume_data.get('industry', 'Technology')}
            - Skills: {resume_data.get('tech_skills', '')} {resume_data.get('soft_skills', '')}
            
            Provide in JSON format:
            {{
                "headline": "Compelling LinkedIn headline (120 chars max)",
                "about_section": "Engaging About section that tells a story (2-3 paragraphs)",
                "featured_skills": ["10 skills to feature prominently"],
                "custom_url_suggestion": "linkedin.com/in/suggested-url",
                "post_ideas": ["5 LinkedIn post ideas to build visibility"],
                "profile_optimization_tips": ["5 specific tips to optimize profile"],
                "keywords_to_include": ["10 SEO keywords for LinkedIn search"]
            }}
            
            Make it professional yet personable, optimized for LinkedIn algorithm.
            """
            
            response = self.model.generate_content(prompt)
            try:
                linkedin_content = json.loads(response.text.strip())
            except:
                linkedin_content = self._parse_linkedin_text(response.text)
            
            return linkedin_content
            
        except Exception as e:
            return self._generate_fallback_linkedin_tips(resume_data)
    
    def generate_interview_prep(self, job_description: str, resume_data: Dict) -> Dict[str, List[str]]:
        """Generate interview preparation materials"""
        if not self.enabled:
            return self._generate_fallback_interview_prep(job_description)
        
        try:
            prompt = f"""
            Generate interview preparation materials for this job.
            
            Job Description:
            {job_description[:1500]}
            
            Candidate Background:
            - Role: {resume_data.get('job_title_target', 'N/A')}
            - Industry: {resume_data.get('industry', 'N/A')}
            
            Provide in JSON format:
            {{
                "common_questions": ["10 likely interview questions for this role"],
                "star_story_prompts": ["5 situations to prepare STAR stories for"],
                "technical_topics": ["5-7 technical topics to review"],
                "questions_to_ask": ["5 smart questions candidate should ask interviewer"],
                "red_flags_to_avoid": ["3-4 common mistakes to avoid"],
                "key_talking_points": ["5 key achievements or skills to emphasize"]
            }}
            
            Be specific to the role and industry.
            """
            
            response = self.model.generate_content(prompt)
            try:
                prep_materials = json.loads(response.text.strip())
            except:
                prep_materials = self._parse_interview_prep_text(response.text)
            
            return prep_materials
            
        except Exception as e:
            return self._generate_fallback_interview_prep(job_description)
    
    def analyze_resume_competitiveness(self, resume_data: Dict, target_industry: str) -> Dict[str, any]:
        """Analyze resume against industry standards (Kickresume/Rezi-style analysis)"""
        if not self.enabled:
            return self._generate_fallback_competitiveness_analysis(resume_data)
        
        try:
            prompt = f"""
            Analyze this resume's competitiveness in the {target_industry} industry.
            Compare against industry best practices and top performers.
            
            Resume Data:
            - Experience: {len(resume_data.get('work_history', []))} positions
            - Skills: {resume_data.get('tech_skills', '')} {resume_data.get('soft_skills', '')}
            - Education: {len(resume_data.get('education', []))} degrees
            - Projects: {len(resume_data.get('projects', []))} projects
            
            Provide competitive analysis in JSON format:
            {{
                "overall_score": 78,
                "grade": "A / B+ / B / C+ / C / D",
                "content_quality_score": 80,
                "ats_readiness_score": 85,
                "visual_appeal_score": 75,
                "keyword_optimization_score": 70,
                "impact_score": 82,
                "strengths": ["3-5 competitive advantages"],
                "weaknesses": ["3-5 areas below industry standard"],
                "comparison_to_top_candidates": "How this stacks up against top 10% candidates",
                "quick_wins": ["3 changes that would improve score significantly"],
                "industry_benchmarks": {{"average_experience_years": 5, "key_skills_match": 80}},
                "recommendation": "Detailed recommendation for improvement"
            }}
            
            Be honest and data-driven.
            """
            
            response = self.model.generate_content(prompt)
            try:
                analysis = json.loads(response.text.strip())
            except:
                analysis = self._parse_competitiveness_text(response.text)
            
            return analysis
            
        except Exception as e:
            return self._generate_fallback_competitiveness_analysis(resume_data)
    
    # Fallback methods when AI is not available
    def _generate_fallback_cover_letter(self, resume_data: Dict, company_name: str) -> str:
        name = resume_data.get('full_name', 'Your Name')
        role = resume_data.get('job_title_target', 'the position')
        company = company_name or 'your company'
        
        return f"""Dear Hiring Manager,

I am excited to apply for the {role} position at {company}. With my background in {resume_data.get('industry', 'the industry')}, I am confident I can contribute meaningfully to your team.

Throughout my career, I have developed expertise in {resume_data.get('tech_skills', 'various technologies')[:100]}, which aligns well with your requirements. I am particularly drawn to this opportunity because of {company}'s reputation for excellence and innovation.

I would welcome the opportunity to discuss how my skills and experience can benefit your organization. Thank you for considering my application.

Best regards,
{name}"""
    
    def _generate_fallback_career_advice(self, profile_data: Dict, career_goal: str) -> Dict:
        return {
            "next_roles": ["Senior " + profile_data.get('job_title_target', 'Professional'), 
                          "Lead " + profile_data.get('job_title_target', 'Professional'),
                          "Manager - " + profile_data.get('industry', 'Your Industry')],
            "skills_to_develop": ["Leadership", "Strategic Planning", "Advanced Technical Skills", 
                                 "Project Management", "Communication"],
            "certifications": ["Industry-relevant certification", "Leadership certification", 
                              "Technical specialization"],
            "timeline": "12-18 months with focused effort",
            "action_plan": ["Update skills regularly", "Network in industry", "Take on leadership projects",
                           "Pursue certification", "Mentor others"],
            "market_trends": f"The {profile_data.get('industry', 'industry')} continues to evolve with technology and innovation.",
            "salary_range": "Research on Glassdoor or Payscale for your region",
            "networking_tips": ["Attend industry events", "Connect on LinkedIn", "Join professional groups"]
        }
    
    def _generate_fallback_job_match(self, resume_data: Dict, job_description: str) -> Dict:
        return {
            "overall_match_score": 75,
            "match_level": "Good Match",
            "strengths": ["Relevant experience", "Key skills present", "Industry knowledge"],
            "gaps": ["Review job description for specific requirements", "Update skills section"],
            "missing_keywords": ["Review job posting for specific keywords"],
            "recommended_additions": ["Quantify achievements", "Add relevant projects", "Update skills"],
            "interview_prep_tips": ["Research company", "Prepare STAR stories", "Review technical concepts"],
            "resume_improvements": ["Tailor resume to job", "Add metrics", "Highlight relevant experience"],
            "confidence_assessment": "Medium - good foundation with room for optimization"
        }
    
    def _generate_fallback_linkedin_tips(self, resume_data: Dict) -> Dict:
        name = resume_data.get('full_name', 'Your Name')
        role = resume_data.get('job_title_target', 'Professional')
        
        return {
            "headline": f"{role} | {resume_data.get('industry', 'Industry')} Expert | Problem Solver",
            "about_section": f"Experienced {role} passionate about driving results. Skilled in {resume_data.get('tech_skills', 'various technologies')[:100]}...",
            "featured_skills": ["Communication", "Leadership", "Problem Solving"] + resume_data.get('tech_skills', '').split(',')[:7],
            "custom_url_suggestion": f"linkedin.com/in/{name.lower().replace(' ', '-')}",
            "post_ideas": ["Share industry insights", "Comment on trends", "Showcase projects", "Share learnings", "Engage with content"],
            "profile_optimization_tips": ["Professional photo", "Complete all sections", "Get recommendations", "Regular updates", "Engage actively"],
            "keywords_to_include": [role, resume_data.get('industry', 'Industry'), "Leadership", "Innovation"]
        }
    
    def _generate_fallback_interview_prep(self, job_description: str) -> Dict:
        return {
            "common_questions": [
                "Tell me about yourself",
                "Why this role?",
                "What are your strengths?",
                "Describe a challenge you overcame",
                "Where do you see yourself in 5 years?",
                "Why should we hire you?",
                "Tell me about a time you failed",
                "How do you handle stress?",
                "Describe your work style",
                "What questions do you have for us?"
            ],
            "star_story_prompts": [
                "Leading a successful project",
                "Overcoming a difficult challenge",
                "Working with a difficult team member",
                "Meeting a tight deadline",
                "Implementing an improvement"
            ],
            "technical_topics": ["Role-specific technical concepts", "Industry best practices", "Tools and technologies", "Problem-solving approaches"],
            "questions_to_ask": [
                "What does success look like in this role?",
                "What are the biggest challenges facing the team?",
                "What's the team culture like?",
                "What are opportunities for growth?",
                "What's next in the interview process?"
            ],
            "red_flags_to_avoid": ["Speaking negatively about past employers", "Being unprepared", "Focusing only on salary", "Not asking questions"],
            "key_talking_points": ["Relevant achievements", "Technical expertise", "Problem-solving skills", "Team collaboration", "Results driven"]
        }
    
    def _generate_fallback_competitiveness_analysis(self, resume_data: Dict) -> Dict:
        return {
            "overall_score": 70,
            "grade": "B",
            "content_quality_score": 72,
            "ats_readiness_score": 75,
            "visual_appeal_score": 68,
            "keyword_optimization_score": 65,
            "impact_score": 70,
            "strengths": ["Clear structure", "Relevant experience", "Industry knowledge"],
            "weaknesses": ["Could use more quantifiable achievements", "Keywords could be optimized", "Consider adding more projects"],
            "comparison_to_top_candidates": "Good foundation. Top candidates typically have more metrics and quantified impact.",
            "quick_wins": ["Add numbers to achievements", "Optimize keywords", "Improve summary statement"],
            "industry_benchmarks": {"average_experience_years": 3, "key_skills_match": 75},
            "recommendation": "Focus on quantifying your impact and optimizing for ATS systems."
        }
    
    # Helper parsing methods
    def _parse_career_advice_text(self, text: str) -> Dict:
        # Simple parsing fallback
        return self._generate_fallback_career_advice({}, "")
    
    def _parse_job_match_text(self, text: str) -> Dict:
        return self._generate_fallback_job_match({}, "")
    
    def _parse_linkedin_text(self, text: str) -> Dict:
        return self._generate_fallback_linkedin_tips({})
    
    def _parse_interview_prep_text(self, text: str) -> Dict:
        return self._generate_fallback_interview_prep("")
    
    def _parse_competitiveness_text(self, text: str) -> Dict:
        return self._generate_fallback_competitiveness_analysis({})


class ResumeScoring:
    """Comprehensive resume scoring system matching top builders"""
    
    @staticmethod
    def calculate_comprehensive_score(resume_data: Dict, job_description: str = "") -> Dict[str, any]:
        """Calculate detailed resume score (0-100) with breakdowns"""
        scores = {
            "overall_score": 0,
            "content_quality": 0,
            "ats_compatibility": 0,
            "keyword_optimization": 0,
            "formatting": 0,
            "impact_statements": 0,
            "completeness": 0,
            "grade": "",
            "detailed_feedback": []
        }
        
        # Content Quality (0-100)
        content_score = 0
        if resume_data.get('summary'):
            content_score += 20
        if len(resume_data.get('work_history', [])) > 0:
            content_score += 30
        if resume_data.get('tech_skills') or resume_data.get('soft_skills'):
            content_score += 25
        if len(resume_data.get('education', [])) > 0:
            content_score += 15
        if len(resume_data.get('projects', [])) > 0:
            content_score += 10
        scores["content_quality"] = min(100, content_score)
        
        # ATS Compatibility (0-100)
        ats_score = 85  # Base score for using ATS-friendly format
        if not resume_data.get('photo'):  # No photo is ATS-friendly
            ats_score += 5
        if resume_data.get('phone') and resume_data.get('email'):
            ats_score += 10
        scores["ats_compatibility"] = min(100, ats_score)
        
        # Keyword Optimization (0-100)
        keyword_score = 60  # Base score
        if job_description:
            # Count keyword matches
            jd_keywords = set(job_description.lower().split())
            resume_text = json.dumps(resume_data).lower()
            matches = sum(1 for kw in jd_keywords if kw in resume_text and len(kw) > 4)
            keyword_score = min(100, 60 + matches * 2)
        scores["keyword_optimization"] = keyword_score
        
        # Formatting (0-100)
        formatting_score = 90  # Our templates are well-formatted
        scores["formatting"] = formatting_score
        
        # Impact Statements (0-100)
        impact_score = 50
        work_history = resume_data.get('work_history', [])
        for job in work_history:
            desc = job.get('description', '')
            # Check for action verbs and quantifiable results
            if any(verb in desc.lower() for verb in ['led', 'managed', 'developed', 'increased', 'reduced', 'achieved']):
                impact_score += 10
            if any(char.isdigit() for char in desc):  # Has numbers
                impact_score += 10
        scores["impact_statements"] = min(100, impact_score)
        
        # Completeness (0-100)
        completeness_score = 0
        required_fields = ['full_name', 'email', 'phone', 'summary', 'work_history', 'education']
        for field in required_fields:
            if resume_data.get(field):
                completeness_score += 100 / len(required_fields)
        scores["completeness"] = int(completeness_score)
        
        # Calculate overall score (weighted average)
        scores["overall_score"] = int(
            scores["content_quality"] * 0.25 +
            scores["ats_compatibility"] * 0.20 +
            scores["keyword_optimization"] * 0.20 +
            scores["formatting"] * 0.15 +
            scores["impact_statements"] * 0.15 +
            scores["completeness"] * 0.05
        )
        
        # Assign grade
        if scores["overall_score"] >= 90:
            scores["grade"] = "A+"
        elif scores["overall_score"] >= 85:
            scores["grade"] = "A"
        elif scores["overall_score"] >= 80:
            scores["grade"] = "B+"
        elif scores["overall_score"] >= 75:
            scores["grade"] = "B"
        elif scores["overall_score"] >= 70:
            scores["grade"] = "C+"
        elif scores["overall_score"] >= 65:
            scores["grade"] = "C"
        else:
            scores["grade"] = "D"
        
        # Generate feedback
        feedback = []
        if scores["content_quality"] < 80:
            feedback.append("⚠️ Add more content sections (projects, certifications, achievements)")
        if scores["keyword_optimization"] < 70:
            feedback.append("⚠️ Optimize keywords to match job description better")
        if scores["impact_statements"] < 70:
            feedback.append("⚠️ Use more action verbs and quantify your achievements with numbers")
        if scores["completeness"] < 90:
            feedback.append("⚠️ Complete all required fields for a stronger resume")
        if scores["overall_score"] >= 85:
            feedback.append("✅ Excellent resume! Ready to impress recruiters")
        
        scores["detailed_feedback"] = feedback
        
        return scores
