# advanced_features.py
# Additional Premium Features for Competitive Advantage
# QR Codes, Resume Import, Spell Check, Version Control, Email Templates

import re
from typing import Dict, List, Optional
import json
from datetime import datetime

class ResumeImporter:
    """Import and parse existing resumes (PDF, DOCX, TXT)"""
    
    @staticmethod
    def parse_text_resume(text: str) -> Dict:
        """Parse resume text and extract structured data"""
        resume_data = {
            "full_name": "",
            "email": "",
            "phone": "",
            "summary": "",
            "work_history": [],
            "education": [],
            "skills": [],
            "parsed_successfully": False
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            resume_data["email"] = emails[0]
        
        # Extract phone
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        if phones:
            resume_data["phone"] = phones[0]
        
        # Extract name (usually first line or after name: label)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # First substantial line is usually name
            for line in lines[:5]:
                if len(line.split()) <= 4 and len(line) > 3 and not '@' in line:
                    resume_data["full_name"] = line
                    break
        
        # Simple section detection
        sections = {
            "experience": ["experience", "work history", "employment", "professional experience"],
            "education": ["education", "academic", "qualifications"],
            "skills": ["skills", "technical skills", "competencies"],
            "summary": ["summary", "profile", "objective", "about"]
        }
        
        # Mark as successfully parsed if we got basic info
        if resume_data["email"] or resume_data["phone"]:
            resume_data["parsed_successfully"] = True
        
        return resume_data
    
    @staticmethod
    def suggest_improvements(parsed_data: Dict) -> List[str]:
        """Suggest improvements to imported resume"""
        suggestions = []
        
        if not parsed_data.get("summary"):
            suggestions.append("📝 Add a professional summary to make a strong first impression")
        
        if not parsed_data.get("skills"):
            suggestions.append("🎯 Add a skills section with industry keywords")
        
        if len(parsed_data.get("work_history", [])) == 0:
            suggestions.append("💼 Add your work experience with quantifiable achievements")
        
        return suggestions


class QRCodeGenerator:
    """Generate QR codes for contact information"""
    
    @staticmethod
    def generate_contact_qr_data(resume_data: Dict) -> str:
        """Generate vCard data for QR code"""
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{resume_data.get('full_name', '')}
TEL:{resume_data.get('phone', '')}
EMAIL:{resume_data.get('email', '')}
URL:{resume_data.get('linkedin', '')}
END:VCARD"""
        return vcard
    
    @staticmethod
    def get_qr_code_url(data: str) -> str:
        """Generate QR code URL using API"""
        import urllib.parse
        encoded_data = urllib.parse.quote(data)
        # Using Google Charts API for QR code generation
        return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_data}"


class SpellChecker:
    """Basic spell and grammar checking"""
    
    COMMON_MISTAKES = {
        "recieve": "receive",
        "occured": "occurred",
        "seperate": "separate",
        "definately": "definitely",
        "managment": "management",
        "sucessful": "successful",
        "expereince": "experience",
        "responsabilities": "responsibilities",
        "acheivement": "achievement",
        "enviroment": "environment"
    }
    
    RESUME_SPECIFIC_CHECKS = [
        {
            "pattern": r"\bi\b",
            "message": "Avoid using first person 'I' in resume bullet points",
            "suggestion": "Start with action verbs instead"
        },
        {
            "pattern": r"\bresponsible for\b",
            "message": "Weak phrase: 'responsible for'",
            "suggestion": "Use strong action verbs like 'Led', 'Managed', 'Developed'"
        },
        {
            "pattern": r"\bhelped with\b",
            "message": "Weak phrase: 'helped with'",
            "suggestion": "Use 'Contributed to', 'Facilitated', 'Supported'"
        }
    ]
    
    @classmethod
    def check_text(cls, text: str) -> List[Dict]:
        """Check text for common mistakes"""
        issues = []
        
        # Check spelling
        words = text.lower().split()
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in cls.COMMON_MISTAKES:
                issues.append({
                    "type": "spelling",
                    "word": clean_word,
                    "suggestion": cls.COMMON_MISTAKES[clean_word],
                    "message": f"Possible spelling error: '{clean_word}' → '{cls.COMMON_MISTAKES[clean_word]}'"
                })
        
        # Check resume-specific issues
        for check in cls.RESUME_SPECIFIC_CHECKS:
            if re.search(check["pattern"], text, re.IGNORECASE):
                issues.append({
                    "type": "style",
                    "message": check["message"],
                    "suggestion": check["suggestion"]
                })
        
        return issues


class ResumeVersionControl:
    """Manage multiple versions of resume"""
    
    @staticmethod
    def save_version(resume_data: Dict, version_name: str = "") -> Dict:
        """Save a version of the resume"""
        version = {
            "version_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "version_name": version_name or f"Version {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "created_at": datetime.now().isoformat(),
            "data": resume_data.copy(),
            "stats": {
                "word_count": len(json.dumps(resume_data).split()),
                "sections": len([k for k in resume_data.keys() if resume_data[k]]),
                "completeness": ResumeVersionControl._calculate_completeness(resume_data)
            }
        }
        return version
    
    @staticmethod
    def _calculate_completeness(data: Dict) -> int:
        """Calculate resume completeness percentage"""
        required_fields = ['full_name', 'email', 'phone', 'summary', 'work_history', 'education', 'tech_skills']
        completed = sum(1 for field in required_fields if data.get(field))
        return int((completed / len(required_fields)) * 100)
    
    @staticmethod
    def compare_versions(version1: Dict, version2: Dict) -> Dict:
        """Compare two resume versions"""
        comparison = {
            "changes": [],
            "improvements": [],
            "stats_comparison": {}
        }
        
        # Compare stats
        for key in ['word_count', 'sections', 'completeness']:
            v1_stat = version1['stats'].get(key, 0)
            v2_stat = version2['stats'].get(key, 0)
            diff = v2_stat - v1_stat
            comparison['stats_comparison'][key] = {
                "old": v1_stat,
                "new": v2_stat,
                "change": diff,
                "improved": diff > 0
            }
        
        return comparison


class EmailTemplates:
    """Professional email templates for job applications"""
    
    TEMPLATES = {
        "application": {
            "name": "Job Application Email",
            "subject": "Application for {position} - {your_name}",
            "body": """Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With {years} years of experience in {field}, I am confident that my skills and background make me an excellent fit for this role.

{key_achievement}

I have attached my resume for your review. I would welcome the opportunity to discuss how my experience and skills can contribute to {company}'s success.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
{your_name}
{phone}
{email}"""
        },
        
        "follow_up": {
            "name": "Interview Follow-up",
            "subject": "Thank You - {position} Interview",
            "body": """Dear {interviewer_name},

Thank you for taking the time to meet with me regarding the {position} position. I enjoyed learning more about {company} and the exciting projects your team is working on.

Our conversation reinforced my enthusiasm for this opportunity. I am particularly excited about {specific_topic_discussed} and believe my experience in {relevant_skill} would allow me to contribute effectively to your team.

Please don't hesitate to contact me if you need any additional information. I look forward to hearing about the next steps.

Best regards,
{your_name}"""
        },
        
        "networking": {
            "name": "Professional Networking",
            "subject": "Connecting - {your_name}",
            "body": """Hello {contact_name},

I hope this message finds you well. I came across your profile while researching {industry/company} and was impressed by your work in {specific_area}.

I am currently {your_situation} and would greatly appreciate the opportunity to learn from your experience. Would you be open to a brief 15-20 minute call to discuss {specific_topic}?

Thank you for considering my request. I look forward to potentially connecting with you.

Best regards,
{your_name}
{linkedin_url}"""
        },
        
        "job_inquiry": {
            "name": "Job Inquiry Email",
            "subject": "Inquiry About Opportunities in {department}",
            "body": """Dear {contact_name},

I hope this email finds you well. I am reaching out to inquire about potential opportunities in {department} at {company}.

With {years} years of experience in {field} and a proven track record in {key_skills}, I am very interested in contributing to {company}'s mission of {company_mission}.

I have attached my resume for your reference. I would appreciate any guidance on current or upcoming opportunities that align with my background.

Thank you for your time and consideration.

Best regards,
{your_name}"""
        },
        
        "status_check": {
            "name": "Application Status Check",
            "subject": "Following Up on {position} Application",
            "body": """Dear {hiring_manager},

I hope this email finds you well. I applied for the {position} position on {application_date} and wanted to follow up on the status of my application.

I remain very interested in this opportunity and believe my {key_qualification} makes me a strong candidate for the role. I would welcome the chance to discuss how I can contribute to your team.

Thank you for your time, and I look forward to hearing from you.

Best regards,
{your_name}
{phone}"""
        }
    }
    
    @classmethod
    def get_template(cls, template_type: str) -> Dict:
        """Get email template by type"""
        return cls.TEMPLATES.get(template_type, cls.TEMPLATES["application"])
    
    @classmethod
    def fill_template(cls, template_type: str, data: Dict) -> Dict:
        """Fill template with user data"""
        template = cls.get_template(template_type)
        
        filled = {
            "subject": template["subject"],
            "body": template["body"]
        }
        
        # Replace placeholders
        for key, value in filled.items():
            for placeholder, replacement in data.items():
                value = value.replace(f"{{{placeholder}}}", str(replacement))
            filled[key] = value
        
        return filled
    
    @classmethod
    def get_all_templates(cls) -> List[Dict]:
        """Get list of all available templates"""
        return [
            {
                "type": key,
                "name": value["name"],
                "description": f"Professional {value['name'].lower()} template"
            }
            for key, value in cls.TEMPLATES.items()
        ]


class KeywordHighlighter:
    """Highlight ATS keywords in resume text"""
    
    @staticmethod
    def highlight_keywords(resume_text: str, job_description: str) -> Dict:
        """Identify and highlight matching keywords"""
        # Extract keywords from job description
        jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower()))
        
        # Common stop words
        stop_words = {'this', 'that', 'with', 'from', 'have', 'will', 'been', 
                     'they', 'their', 'your', 'should', 'would', 'could', 'about'}
        jd_keywords = jd_words - stop_words
        
        # Find matching keywords in resume
        resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
        
        matched = resume_words & jd_keywords
        missing = jd_keywords - resume_words
        
        # Calculate keyword density
        total_keywords = len(jd_keywords)
        matched_count = len(matched)
        density = (matched_count / total_keywords * 100) if total_keywords > 0 else 0
        
        return {
            "matched_keywords": sorted(list(matched)),
            "missing_keywords": sorted(list(missing))[:20],
            "keyword_density": round(density, 1),
            "total_jd_keywords": total_keywords,
            "matched_count": matched_count,
            "status": "Excellent" if density >= 70 else "Good" if density >= 50 else "Needs Improvement"
        }


class ResumeLengthOptimizer:
    """Optimize resume length and suggest what to keep/remove"""
    
    @staticmethod
    def analyze_length(resume_data: Dict, target_pages: int = 1) -> Dict:
        """Analyze resume length and provide recommendations"""
        # Calculate approximate word count
        word_count = 0
        sections = []
        
        if resume_data.get('summary'):
            words = len(resume_data['summary'].split())
            word_count += words
            sections.append({"name": "Summary", "words": words, "essential": True})
        
        for job in resume_data.get('work_history', []):
            desc = job.get('description', '')
            words = len(desc.split())
            word_count += words
            sections.append({"name": f"Work: {job.get('company', 'Company')}", "words": words, "essential": True})
        
        for proj in resume_data.get('projects', []):
            desc = proj.get('description', '')
            words = len(desc.split())
            word_count += words
            sections.append({"name": f"Project: {proj.get('title', 'Project')}", "words": words, "essential": False})
        
        for edu in resume_data.get('education', []):
            words = 20  # Approximate
            word_count += words
            sections.append({"name": "Education", "words": words, "essential": True})
        
        # Target: ~450-600 words per page
        target_words = target_pages * 500
        
        analysis = {
            "total_words": word_count,
            "target_words": target_words,
            "estimated_pages": round(word_count / 500, 1),
            "target_pages": target_pages,
            "status": "",
            "recommendations": []
        }
        
        if word_count > target_words + 100:
            analysis["status"] = "Too Long"
            analysis["recommendations"].append(f"⚠️ Resume is {word_count - target_words} words over target")
            analysis["recommendations"].append("💡 Consider removing less relevant projects or older experiences")
            analysis["recommendations"].append("✂️ Condense bullet points to focus on key achievements")
        elif word_count < target_words - 100:
            analysis["status"] = "Too Short"
            analysis["recommendations"].append(f"📝 Add {target_words - word_count} more words to fill the page effectively")
            analysis["recommendations"].append("💡 Expand on achievements with quantifiable results")
            analysis["recommendations"].append("➕ Add relevant projects or certifications")
        else:
            analysis["status"] = "Perfect Length"
            analysis["recommendations"].append("✅ Resume length is optimal for ATS and human readers")
        
        analysis["sections"] = sections
        
        return analysis
