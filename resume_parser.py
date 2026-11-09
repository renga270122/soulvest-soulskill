"""
Resume Parser - Extract data from PDF/DOCX resumes
"""
import re
import json
from typing import Dict, List, Optional

try:
    import PyPDF2
except ImportError:
    try:
        import pypdf2 as PyPDF2
    except ImportError:
        PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class ResumeParser:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
    
    def extract_text_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        if PyPDF2 is None:
            raise Exception("PyPDF2 is not installed. Please install it to parse PDF files.")
        
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
        if Document is None:
            raise Exception("python-docx is not installed. Please install it to parse DOCX files.")
        
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
        if genai is None:
            print("Google Generative AI not available, falling back to regex")
            return self._parse_with_regex(text)
        
        if not self.api_key:
            return self._parse_with_regex(text)
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            You are an expert resume parser. Extract the following information from this resume and return it as a JSON object.
            If any field is not found, use an empty string or empty array.
            
            CRITICAL INSTRUCTIONS FOR NAME EXTRACTION:
            - The "full_name" should be the PERSON'S ACTUAL NAME (e.g., "John Smith", "Karthik Gowda")
            - DO NOT use section headers like "Career Summary", "Professional Summary", "Resume", "CV"
            - DO NOT use location information like "Bengaluru, Karnataka"
            - DO NOT use job titles or company names
            - The name is usually at the very top of the resume, often on the first line
            - Look for a line with 2-4 capitalized words that are names, not headings
            
            For "city" field:
            - Extract ONLY the city name where the person is located
            - Example: "Bengaluru" or "New York" (just the city, not full address)
            
            Resume text:
            {text}
            
            Return JSON with this exact structure:
            {{
                "full_name": "Person's actual name (e.g., John Smith, NOT section headers)",
                "email": "Email address",
                "phone": "Phone number",
                "city": "City name only",
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
            
            Return ONLY valid JSON, no other text. Double-check that full_name is a person's name, not a heading.
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
        
        # Extract name - improved logic
        # Common resume section headers to avoid
        section_headers = [
            'resume', 'cv', 'curriculum vitae', 'profile', 'summary', 'objective',
            'career summary', 'professional summary', 'about', 'about me',
            'contact', 'contact information', 'personal information', 'details',
            'experience', 'work experience', 'employment', 'education',
            'skills', 'technical skills', 'core competencies', 'expertise',
            'projects', 'certifications', 'achievements', 'awards',
            'references', 'hobbies', 'interests', 'languages'
        ]
        
        location_keywords = ['location', 'address', 'city', 'state', 'country', 
                           'pin', 'zip', 'postal', ':', 'email', 'phone', 
                           'linkedin', 'github', 'portfolio', 'website']
        
        lines = text.split('\n')
        name_candidates = []
        
        # Strategy 1: Look for name near contact info (within first 15 lines)
        email_line_idx = -1
        phone_line_idx = -1
        
        for idx, line in enumerate(lines[:15]):
            if email_match and email_match.group() in line:
                email_line_idx = idx
            if phone_match and phone_match.group() in line:
                phone_line_idx = idx
        
        # Check lines around contact info
        contact_range = set()
        if email_line_idx >= 0:
            contact_range.update(range(max(0, email_line_idx - 3), min(len(lines), email_line_idx + 2)))
        if phone_line_idx >= 0:
            contact_range.update(range(max(0, phone_line_idx - 3), min(len(lines), phone_line_idx + 2)))
        
        # Strategy 2: Check first 20 lines for name-like patterns
        for idx, line in enumerate(lines[:20]):
            line = line.strip()
            
            # Skip empty or very short/long lines
            if len(line) < 3 or len(line) > 50:
                continue
            
            line_lower = line.lower()
            
            # Skip section headers - exact match
            if any(header == line_lower for header in section_headers):
                continue
            
            # Skip partial matches of section headers
            if any(header in line_lower for header in section_headers):
                continue
            
            # Skip lines with common section header patterns
            if line.endswith(':') or line.startswith('-') or line.startswith('•'):
                continue
            
            # Skip lines with location keywords or contact patterns
            if any(keyword in line_lower for keyword in location_keywords):
                continue
            
            # Skip lines with email or phone
            if '@' in line or re.search(r'\d{3}[-.\s]\d{3}[-.\s]\d{4}|\+\d{2}[-.\s]\d{10}', line):
                continue
            
            # Skip lines with URLs
            if 'http' in line_lower or 'www.' in line_lower or '.com' in line_lower:
                continue
            
            # Check if it looks like a name
            words = line.split()
            
            # Names typically have 2-4 words
            if 2 <= len(words) <= 4:
                # Additional check: skip if any word is a common resume keyword
                resume_keywords = ['career', 'professional', 'work', 'technical', 'personal', 
                                 'contact', 'academic', 'project', 'key', 'core']
                if any(word.lower() in resume_keywords for word in words):
                    continue
                
                # All words should start with capital and be mostly alphabetic
                valid_name = True
                for word in words:
                    # Remove common punctuation
                    word_clean = word.strip('.,')
                    if not word_clean:
                        continue
                    # First letter should be uppercase
                    if not word_clean[0].isupper():
                        valid_name = False
                        break
                    # Should be mostly letters (allow apostrophes)
                    alpha_chars = sum(c.isalpha() or c == "'" for c in word_clean)
                    if alpha_chars < len(word_clean) * 0.8:
                        valid_name = False
                        break
                
                if valid_name:
                    # Calculate score based on position and context
                    score = 100 - idx  # Prefer earlier lines
                    
                    # Bonus if near contact info
                    if idx in contact_range:
                        score += 50
                    
                    # Bonus if it's one of the first 3 lines
                    if idx < 3:
                        score += 30
                    
                    # Penalty if it contains numbers
                    if any(c.isdigit() for c in line):
                        score -= 30
                    
                    name_candidates.append((score, line, idx))
        
        # Select best candidate
        if name_candidates:
            name_candidates.sort(reverse=True)
            data['full_name'] = name_candidates[0][1]
        
        # Extract city/location
        city_pattern = r'(?:Location|City|Address)[:\s]+([A-Za-z\s,]+?)(?:\n|$)'
        city_match = re.search(city_pattern, text, re.IGNORECASE)
        if city_match:
            city_text = city_match.group(1).strip()
            # Get just the city name (first part before comma)
            data['city'] = city_text.split(',')[0].strip()
        
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
        
        # Extract common experience and education sections heuristically when AI parsing is unavailable.
        def section_text(patterns):
            heading = r'(?:' + '|'.join(patterns) + r')'
            match = re.search(heading + r'\\s*[:\\-]?\\s*(.*?)(?=\\n\\s*(?:EDUCATION|ACADEMIC|QUALIFICATION|SKILLS|TECHNICAL SKILLS|PROJECTS|CERTIFICATIONS|ACHIEVEMENTS|AWARDS|LANGUAGES|PERSONAL DETAILS)\\b|\\Z)', text, re.IGNORECASE | re.DOTALL)
            return match.group(1).strip() if match else ''

        experience_text = section_text(['WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE', 'EMPLOYMENT HISTORY', 'EXPERIENCE'])
        if experience_text:
            blocks = [block.strip() for block in re.split(r'\\n\\s*\\n', experience_text) if block.strip()]
            for block in blocks[:12]:
                lines = [re.sub(r'^[•▪▫●*\\-]+\\s*', '', line).strip() for line in block.splitlines() if line.strip()]
                if not lines:
                    continue
                title = lines[0][:120]
                company = lines[1][:120] if len(lines) > 1 else ''
                responsibilities = '\\n'.join(lines[2:] if len(lines) > 2 else lines[1:])
                if title or company or responsibilities:
                    data['work_entries'].append({
                        'title': title, 'company': company,
                        'start_date': '', 'end_date': '',
                        'responsibilities': responsibilities[:2000]
                    })

        education_text = section_text(['EDUCATION', 'ACADEMIC QUALIFICATIONS', 'QUALIFICATIONS'])
        if education_text:
            blocks = [block.strip() for block in re.split(r'\\n\\s*\\n', education_text) if block.strip()]
            for block in blocks[:10]:
                lines = [line.strip() for line in block.splitlines() if line.strip()]
                if not lines:
                    continue
                data['education_entries'].append({
                    'degree': lines[0][:160],
                    'institution': lines[1][:160] if len(lines) > 1 else '',
                    'year': lines[2][:40] if len(lines) > 2 else ''
                })

        projects_text = section_text(['PROJECTS', 'PERSONAL PROJECTS', 'KEY PROJECTS'])
        if projects_text:
            for block in [b.strip() for b in re.split(r'\\n\\s*\\n', projects_text) if b.strip()][:10]:
                lines = [line.strip() for line in block.splitlines() if line.strip()]
                if lines:
                    data.setdefault('projects', []).append({
                        'name': lines[0][:160],
                        'description': '\\n'.join(lines[1:])[:1500],
                        'technologies': ''
                    })

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
