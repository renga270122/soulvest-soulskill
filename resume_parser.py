"""
Resume Parser - Extract data from PDF/DOCX resumes
"""
import re
import json
from typing import Dict, List, Optional
import PyPDF2
from docx import Document
import google.generativeai as genai

class ResumeParser:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
    
    def extract_text_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_text_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def extract_text_from_txt(self, file) -> str:
        """Extract text from TXT file"""
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def parse_resume(self, file) -> Dict:
        """
        Parse resume file and extract structured data
        
        Returns:
            Dict with keys: full_name, email, phone, city, linkedin,
                          summary, tech_skills, work_entries, education_entries
        """
        # Determine file type and extract text
        file_name = file.name.lower()
        
        if file_name.endswith('.pdf'):
            text = self.extract_text_from_pdf(file)
        elif file_name.endswith('.docx'):
            text = self.extract_text_from_docx(file)
        elif file_name.endswith('.txt'):
            text = self.extract_text_from_txt(file)
        else:
            raise Exception("Unsupported file format. Please upload PDF, DOCX, or TXT.")
        
        # Parse with AI if available, otherwise use regex
        if self.api_key:
            return self._parse_with_ai(text)
        else:
            return self._parse_with_regex(text)
    
    def _parse_with_ai(self, text: str) -> Dict:
        """Use AI to extract structured data from resume text"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Extract the following information from this resume and return it as a JSON object.
            If any field is not found, use an empty string or empty array.
            
            Resume text:
            {text}
            
            Return JSON with this exact structure:
            {{
                "full_name": "Full name",
                "email": "Email address",
                "phone": "Phone number",
                "city": "City/Location",
                "linkedin": "LinkedIn profile URL",
                "github": "GitHub profile URL",
                "portfolio": "Portfolio website URL",
                "summary": "Professional summary or objective (2-3 sentences)",
                "tech_skills": "Comma-separated list of technical skills",
                "work_entries": [
                    {{
                        "title": "Job Title",
                        "company": "Company Name",
                        "start_date": "Start date (MM/YYYY)",
                        "end_date": "End date (MM/YYYY or 'Present')",
                        "responsibilities": "Key responsibilities and achievements (separated by newlines)"
                    }}
                ],
                "education_entries": [
                    {{
                        "degree": "Degree name",
                        "institution": "Institution name",
                        "year": "Graduation year (YYYY)"
                    }}
                ],
                "certifications": "Comma-separated list of certifications",
                "languages": "Comma-separated list of languages"
            }}
            
            Return ONLY valid JSON, no other text.
            """
            
            response = model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up response - remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = re.sub(r'^```json?\s*', '', result_text)
                result_text = re.sub(r'\s*```$', '', result_text)
            
            parsed_data = json.loads(result_text)
            return parsed_data
            
        except Exception as e:
            print(f"AI parsing failed: {str(e)}")
            # Fallback to regex parsing
            return self._parse_with_regex(text)
    
    def _parse_with_regex(self, text: str) -> Dict:
        """Fallback: Parse resume using regex patterns"""
        data = {
            'full_name': '',
            'email': '',
            'phone': '',
            'city': '',
            'linkedin': '',
            'github': '',
            'portfolio': '',
            'summary': '',
            'tech_skills': '',
            'work_entries': [],
            'education_entries': [],
            'certifications': '',
            'languages': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            data['email'] = email_match.group()
        
        # Extract phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            data['phone'] = phone_match.group()
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            data['linkedin'] = f"https://{linkedin_match.group()}"
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            data['github'] = f"https://{github_match.group()}"
        
        # Extract name (first line or first capitalized words)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line) > 3 and len(line) < 50:
                # Check if it looks like a name (2-4 capitalized words)
                words = line.split()
                if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                    data['full_name'] = line
                    break
        
        # Try to extract skills section
        skills_section = re.search(r'(?:Skills?|Technical Skills?|Expertise)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)', 
                                  text, re.IGNORECASE | re.DOTALL)
        if skills_section:
            skills_text = skills_section.group(1).strip()
            # Remove bullets and clean up
            skills_text = re.sub(r'[•▪▫■●]', '', skills_text)
            skills_text = re.sub(r'\n+', ', ', skills_text)
            data['tech_skills'] = skills_text[:500]  # Limit length
        
        # Try to extract summary/objective
        summary_section = re.search(r'(?:Summary|Objective|Profile|About)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)', 
                                   text, re.IGNORECASE | re.DOTALL)
        if summary_section:
            data['summary'] = summary_section.group(1).strip()[:500]
        
        return data
    
    def auto_fill_session_state(self, parsed_data: Dict, session_state) -> None:
        """Fill streamlit session state with parsed data"""
        
        # Basic info
        if parsed_data.get('full_name'):
            session_state.full_name = parsed_data['full_name']
        if parsed_data.get('email'):
            session_state.email = parsed_data['email']
        if parsed_data.get('phone'):
            session_state.phone = parsed_data['phone']
        if parsed_data.get('city'):
            session_state.city = parsed_data['city']
        
        # Social links
        if parsed_data.get('linkedin'):
            session_state.linkedin = parsed_data['linkedin']
        if parsed_data.get('github'):
            session_state.github = parsed_data['github']
        if parsed_data.get('portfolio'):
            session_state.portfolio = parsed_data['portfolio']
        
        # Professional info
        if parsed_data.get('summary'):
            session_state.summary = parsed_data['summary']
        if parsed_data.get('tech_skills'):
            session_state.tech_skills = parsed_data['tech_skills']
        
        # Work experience
        if parsed_data.get('work_entries'):
            session_state.work_entries = parsed_data['work_entries']
        
        # Education
        if parsed_data.get('education_entries'):
            session_state.education_entries = parsed_data['education_entries']
        
        # Additional fields
        if parsed_data.get('certifications'):
            session_state.certifications = parsed_data['certifications']
        if parsed_data.get('languages'):
            session_state.languages = parsed_data['languages']


def parse_uploaded_resume(uploaded_file, api_key: Optional[str] = None) -> Dict:
    """
    Convenience function to parse an uploaded resume file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        api_key: Optional Gemini API key for AI parsing
    
    Returns:
        Dict with parsed resume data
    """
    parser = ResumeParser(api_key=api_key)
    return parser.parse_resume(uploaded_file)
