# export_manager.py
# Multi-format Export System - PDF, DOCX, TXT, JSON
# ATS-optimized exports for different systems

import json
from typing import Dict, Optional
import base64
from datetime import datetime

class ExportManager:
    """Multi-format resume export manager"""
    
    @staticmethod
    def export_to_json(resume_data: Dict, include_metadata: bool = True) -> str:
        """Export resume as JSON"""
        export_data = resume_data.copy()
        
        if include_metadata:
            export_data["_metadata"] = {
                "exported_at": datetime.now().isoformat(),
                "format_version": "2.0",
                "platform": "Soulvest AI Resume Builder"
            }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_to_plain_text(resume_data: Dict) -> str:
        """Export resume as plain text (ATS-friendly)"""
        text_parts = []
        
        # Header
        text_parts.append("=" * 80)
        text_parts.append(resume_data.get('full_name', '').upper())
        text_parts.append("=" * 80)
        text_parts.append("")
        
        # Contact Information
        text_parts.append("CONTACT INFORMATION")
        text_parts.append("-" * 80)
        if resume_data.get('email'):
            text_parts.append(f"Email: {resume_data['email']}")
        if resume_data.get('phone'):
            text_parts.append(f"Phone: {resume_data['phone']}")
        if resume_data.get('linkedin'):
            text_parts.append(f"LinkedIn: {resume_data['linkedin']}")
        if resume_data.get('github'):
            text_parts.append(f"GitHub: {resume_data['github']}")
        if resume_data.get('portfolio'):
            text_parts.append(f"Portfolio: {resume_data['portfolio']}")
        
        location_parts = []
        if resume_data.get('city'):
            location_parts.append(resume_data['city'])
        if resume_data.get('state'):
            location_parts.append(resume_data['state'])
        if location_parts:
            text_parts.append(f"Location: {', '.join(location_parts)}")
        text_parts.append("")
        
        # Professional Summary
        if resume_data.get('summary'):
            text_parts.append("PROFESSIONAL SUMMARY")
            text_parts.append("-" * 80)
            text_parts.append(resume_data['summary'])
            text_parts.append("")
        
        # Skills
        skills = []
        if resume_data.get('tech_skills'):
            skills.append(f"Technical Skills: {resume_data['tech_skills']}")
        if resume_data.get('soft_skills'):
            skills.append(f"Soft Skills: {resume_data['soft_skills']}")
        if resume_data.get('languages'):
            skills.append(f"Languages: {resume_data['languages']}")
        
        if skills:
            text_parts.append("SKILLS")
            text_parts.append("-" * 80)
            for skill_section in skills:
                text_parts.append(skill_section)
            text_parts.append("")
        
        # Work Experience
        work_history = resume_data.get('work_history', [])
        if work_history:
            text_parts.append("WORK EXPERIENCE")
            text_parts.append("-" * 80)
            for job in work_history:
                title = job.get('job_title', 'Position')
                company = job.get('company', '')
                start = job.get('start_date', '')
                end = job.get('end_date', 'Present')
                
                text_parts.append(f"{title} | {company}")
                text_parts.append(f"{start} - {end}")
                
                if job.get('location'):
                    text_parts.append(f"Location: {job['location']}")
                
                if job.get('description'):
                    text_parts.append("")
                    descriptions = [d.strip() for d in job['description'].split('\n') if d.strip()]
                    for desc in descriptions:
                        text_parts.append(f"  • {desc}")
                
                text_parts.append("")
            text_parts.append("")
        
        # Projects
        projects = resume_data.get('projects', [])
        if projects:
            text_parts.append("PROJECTS")
            text_parts.append("-" * 80)
            for project in projects:
                title = project.get('title', 'Project')
                text_parts.append(title)
                
                if project.get('technologies'):
                    text_parts.append(f"Technologies: {project['technologies']}")
                if project.get('description'):
                    text_parts.append(project['description'])
                if project.get('link'):
                    text_parts.append(f"Link: {project['link']}")
                
                text_parts.append("")
            text_parts.append("")
        
        # Education
        education = resume_data.get('education', [])
        if education:
            text_parts.append("EDUCATION")
            text_parts.append("-" * 80)
            for edu in education:
                degree = edu.get('degree', '')
                institution = edu.get('institution', '')
                year = edu.get('year', '')
                
                text_parts.append(f"{degree}")
                text_parts.append(f"{institution}")
                if year:
                    text_parts.append(f"Graduated: {year}")
                if edu.get('grade'):
                    text_parts.append(f"Grade: {edu['grade']}")
                
                text_parts.append("")
            text_parts.append("")
        
        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            text_parts.append("CERTIFICATIONS")
            text_parts.append("-" * 80)
            for cert in certifications:
                if isinstance(cert, dict):
                    text_parts.append(f"  • {cert.get('name', '')} - {cert.get('issuer', '')} ({cert.get('year', '')})")
                else:
                    text_parts.append(f"  • {cert}")
            text_parts.append("")
        
        # Achievements
        achievements = resume_data.get('achievements', [])
        if achievements:
            text_parts.append("ACHIEVEMENTS")
            text_parts.append("-" * 80)
            for achievement in achievements:
                text_parts.append(f"  • {achievement}")
            text_parts.append("")
        
        # Footer
        text_parts.append("=" * 80)
        text_parts.append("Generated by Soulvest AI Resume Builder")
        text_parts.append(f"Export Date: {datetime.now().strftime('%Y-%m-%d')}")
        text_parts.append("=" * 80)
        
        return "\n".join(text_parts)
    
    @staticmethod
    def export_to_markdown(resume_data: Dict) -> str:
        """Export resume as Markdown"""
        md_parts = []
        
        # Header
        md_parts.append(f"# {resume_data.get('full_name', 'Your Name')}")
        md_parts.append("")
        
        # Contact Information
        contact_items = []
        if resume_data.get('email'):
            contact_items.append(f"✉️ {resume_data['email']}")
        if resume_data.get('phone'):
            contact_items.append(f"📱 {resume_data['phone']}")
        if resume_data.get('linkedin'):
            contact_items.append(f"[LinkedIn]({resume_data['linkedin']})")
        if resume_data.get('github'):
            contact_items.append(f"[GitHub]({resume_data['github']})")
        if resume_data.get('city') and resume_data.get('state'):
            contact_items.append(f"📍 {resume_data['city']}, {resume_data['state']}")
        
        if contact_items:
            md_parts.append(" | ".join(contact_items))
            md_parts.append("")
        
        # Professional Summary
        if resume_data.get('summary'):
            md_parts.append("## Professional Summary")
            md_parts.append("")
            md_parts.append(resume_data['summary'])
            md_parts.append("")
        
        # Skills
        if resume_data.get('tech_skills') or resume_data.get('soft_skills'):
            md_parts.append("## Skills")
            md_parts.append("")
            if resume_data.get('tech_skills'):
                md_parts.append(f"**Technical:** {resume_data['tech_skills']}")
            if resume_data.get('soft_skills'):
                md_parts.append(f"**Soft Skills:** {resume_data['soft_skills']}")
            md_parts.append("")
        
        # Work Experience
        work_history = resume_data.get('work_history', [])
        if work_history:
            md_parts.append("## Work Experience")
            md_parts.append("")
            for job in work_history:
                md_parts.append(f"### {job.get('job_title', 'Position')} | {job.get('company', '')}")
                md_parts.append(f"*{job.get('start_date', '')} - {job.get('end_date', 'Present')}*")
                md_parts.append("")
                
                if job.get('description'):
                    descriptions = [d.strip() for d in job['description'].split('\n') if d.strip()]
                    for desc in descriptions:
                        md_parts.append(f"- {desc}")
                md_parts.append("")
        
        # Projects
        projects = resume_data.get('projects', [])
        if projects:
            md_parts.append("## Projects")
            md_parts.append("")
            for project in projects:
                title = project.get('title', 'Project')
                if project.get('link'):
                    md_parts.append(f"### [{title}]({project['link']})")
                else:
                    md_parts.append(f"### {title}")
                
                if project.get('technologies'):
                    md_parts.append(f"**Technologies:** {project['technologies']}")
                if project.get('description'):
                    md_parts.append(f"{project['description']}")
                md_parts.append("")
        
        # Education
        education = resume_data.get('education', [])
        if education:
            md_parts.append("## Education")
            md_parts.append("")
            for edu in education:
                md_parts.append(f"### {edu.get('degree', '')}")
                md_parts.append(f"**{edu.get('institution', '')}** | {edu.get('year', '')}")
                if edu.get('grade'):
                    md_parts.append(f"Grade: {edu['grade']}")
                md_parts.append("")
        
        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            md_parts.append("## Certifications")
            md_parts.append("")
            for cert in certifications:
                if isinstance(cert, dict):
                    md_parts.append(f"- **{cert.get('name', '')}** - {cert.get('issuer', '')} ({cert.get('year', '')})")
                else:
                    md_parts.append(f"- {cert}")
            md_parts.append("")
        
        md_parts.append("---")
        md_parts.append(f"*Generated by Soulvest AI Resume Builder on {datetime.now().strftime('%Y-%m-%d')}*")
        
        return "\n".join(md_parts)
    
    @staticmethod
    def get_ats_optimized_html(resume_data: Dict, template_style: str = "minimal") -> str:
        """Generate highly ATS-optimized HTML (parseable by all ATS systems)"""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_data.get('full_name', 'Resume')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #000;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
            background: white;
        }}
        h1 {{
            font-size: 20pt;
            margin: 0 0 5px 0;
            font-weight: bold;
        }}
        h2 {{
            font-size: 14pt;
            margin: 15px 0 5px 0;
            padding-bottom: 2px;
            border-bottom: 2px solid #333;
            font-weight: bold;
        }}
        h3 {{
            font-size: 12pt;
            margin: 10px 0 3px 0;
            font-weight: bold;
        }}
        p {{
            margin: 5px 0;
        }}
        ul {{
            margin: 5px 0 10px 20px;
            padding: 0;
        }}
        li {{
            margin: 3px 0;
        }}
        .contact {{
            margin: 5px 0 15px 0;
            font-size: 10pt;
        }}
        .date {{
            font-style: italic;
            color: #555;
        }}
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}
        @media print {{
            body {{
                padding: 0;
            }}
        }}
    </style>
</head>
<body>
"""
        
        # Header
        html += f"    <h1>{resume_data.get('full_name', '')}</h1>\n"
        
        # Contact
        contact_parts = []
        if resume_data.get('email'):
            contact_parts.append(resume_data['email'])
        if resume_data.get('phone'):
            contact_parts.append(resume_data['phone'])
        if resume_data.get('city') and resume_data.get('state'):
            contact_parts.append(f"{resume_data['city']}, {resume_data['state']}")
        if resume_data.get('linkedin'):
            contact_parts.append(resume_data['linkedin'])
        
        if contact_parts:
            html += f"    <p class='contact'>{' | '.join(contact_parts)}</p>\n"
        
        # Professional Summary
        if resume_data.get('summary'):
            html += "    <h2>Professional Summary</h2>\n"
            html += f"    <p>{resume_data['summary']}</p>\n"
        
        # Skills
        if resume_data.get('tech_skills') or resume_data.get('soft_skills'):
            html += "    <h2>Skills</h2>\n"
            if resume_data.get('tech_skills'):
                html += f"    <p><strong>Technical Skills:</strong> {resume_data['tech_skills']}</p>\n"
            if resume_data.get('soft_skills'):
                html += f"    <p><strong>Soft Skills:</strong> {resume_data['soft_skills']}</p>\n"
        
        # Work Experience
        work_history = resume_data.get('work_history', [])
        if work_history:
            html += "    <h2>Work Experience</h2>\n"
            for job in work_history:
                html += f"    <h3>{job.get('job_title', '')} | {job.get('company', '')}</h3>\n"
                html += f"    <p class='date'>{job.get('start_date', '')} - {job.get('end_date', 'Present')}</p>\n"
                
                if job.get('description'):
                    html += "    <ul>\n"
                    descriptions = [d.strip() for d in job['description'].split('\n') if d.strip()]
                    for desc in descriptions:
                        html += f"        <li>{desc}</li>\n"
                    html += "    </ul>\n"
        
        # Projects
        projects = resume_data.get('projects', [])
        if projects:
            html += "    <h2>Projects</h2>\n"
            for project in projects:
                html += f"    <h3>{project.get('title', '')}</h3>\n"
                if project.get('technologies'):
                    html += f"    <p><strong>Technologies:</strong> {project['technologies']}</p>\n"
                if project.get('description'):
                    html += f"    <p>{project['description']}</p>\n"
        
        # Education
        education = resume_data.get('education', [])
        if education:
            html += "    <h2>Education</h2>\n"
            for edu in education:
                html += f"    <h3>{edu.get('degree', '')}</h3>\n"
                html += f"    <p>{edu.get('institution', '')} | {edu.get('year', '')}</p>\n"
                if edu.get('grade'):
                    html += f"    <p>Grade: {edu['grade']}</p>\n"
        
        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            html += "    <h2>Certifications</h2>\n"
            html += "    <ul>\n"
            for cert in certifications:
                if isinstance(cert, dict):
                    html += f"        <li>{cert.get('name', '')} - {cert.get('issuer', '')} ({cert.get('year', '')})</li>\n"
                else:
                    html += f"        <li>{cert}</li>\n"
            html += "    </ul>\n"
        
        html += "</body>\n</html>"
        
        return html
    
    @staticmethod
    def create_download_link(content: str, filename: str, mime_type: str = "text/plain") -> str:
        """Create a download link for Streamlit"""
        b64 = base64.b64encode(content.encode()).decode()
        return f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {filename}</a>'
