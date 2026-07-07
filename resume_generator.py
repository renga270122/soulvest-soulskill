# resume_generator.py
# Resume HTML generation module

def generate_resume_html(session_data, template_config):
    """Generate HTML resume based on session data and template"""
    
    name = session_data.get('full_name', 'Your Name')
    email = session_data.get('email', '')
    phone = session_data.get('phone', '')
    city = session_data.get('city', '')
    state = session_data.get('state', '')
    summary = session_data.get('summary', '')
    tech_skills = session_data.get('tech_skills', '')
    soft_skills = session_data.get('soft_skills', '')
    layout = session_data.get('layout', 'Single Column')
    
    font = template_config.get('font', 'Arial')
    color = template_config.get('color', '#333')
    
    # Profile photo
    photo_html = ""
    if session_data.get('profile_photo_base64'):
        photo_html = f"<img src='data:image/png;base64,{session_data['profile_photo_base64']}' style='width:120px;height:120px;border-radius:50%;object-fit:cover;border:3px solid {color};margin-bottom:15px;'/>"
    
    # Contact info
    contact_html = f"""
    <div style='margin:10px 0;'>
        <p style='margin:3px 0;'><strong>\ud83d\udce7</strong> {email}</p>
        <p style='margin:3px 0;'><strong>\ud83d\udcf1</strong> {phone}</p>
        <p style='margin:3px 0;'><strong>\ud83d\udccd</strong> {city}, {state}</p>
    </div>
    """
    
    # Languages
    lang_html = ""
    if session_data.get('language_entries'):
        lang_html = "<h3 style='color:" + color + ";border-bottom:2px solid " + color + ";padding-bottom:5px;'>Languages</h3>"
        for lang in session_data['language_entries']:
            lang_html += f"<p style='margin:5px 0;'>\u2022 {lang['language']} - {lang['proficiency']}</p>"
    
    # Work Experience
    work_html = ""
    if session_data.get('work_entries'):
        work_html = "<h3 style='color:" + color + ";border-bottom:2px solid " + color + ";padding-bottom:5px;margin-top:20px;'>Work Experience</h3>"
        for work in session_data['work_entries']:
            work_html += f"""
            <div style='margin:15px 0;'>
                <p style='margin:5px 0;'><strong>{work['title']}</strong></p>
                <p style='margin:5px 0;color:#666;'>{work['company']} | {work['duration']}</p>
                <p style='margin:5px 0;'>{work['responsibilities']}</p>
            </div>
            """
    
    # Projects
    project_html = ""
    if session_data.get('project_entries'):
        project_html = "<h3 style='color:" + color + ";border-bottom:2px solid " + color + ";padding-bottom:5px;margin-top:20px;'>Projects</h3>"
        for proj in session_data['project_entries']:
            project_html += f"""
            <div style='margin:15px 0;'>
                <p style='margin:5px 0;'><strong>{proj['name']}</strong></p>
                <p style='margin:5px 0;color:#666;'>{proj.get('duration', '')}</p>
                <p style='margin:5px 0;'>{proj['description']}</p>
                {f"<p style='margin:5px 0;'><strong>Technologies:</strong> {proj.get('technologies', '')}</p>" if proj.get('technologies') else ""}
            </div>
            """
    
    # Education
    edu_html = ""
    if session_data.get('education_entries'):
        edu_html = "<h3 style='color:" + color + ";border-bottom:2px solid " + color + ";padding-bottom:5px;margin-top:20px;'>Education</h3>"
        for edu in session_data['education_entries']:
            edu_html += f"""
            <div style='margin:15px 0;'>
                <p style='margin:5px 0;'><strong>{edu['degree']} in {edu['stream']}</strong></p>
                <p style='margin:5px 0;color:#666;'>{edu['institution']}, {edu.get('university', '')}</p>
                <p style='margin:5px 0;'>{edu.get('year', '')} {' | ' + edu.get('grade', '') if edu.get('grade') else ''}</p>
            </div>
            """
    
    # Certifications
    cert_html = ""
    if session_data.get('certification_entries'):
        cert_html = "<h3 style='color:" + color + ";border-bottom:2px solid " + color + ";padding-bottom:5px;margin-top:20px;'>Certifications</h3>"
        for cert in session_data['certification_entries']:
            cert_html += f"<p style='margin:8px 0;'>\u2022 {cert['name']} - {cert.get('issuer', '')} ({cert.get('year', '')})</p>"
    
    # Social Links
    social_html = ""
    if session_data.get('linkedin') or session_data.get('github') or session_data.get('portfolio'):
        social_html = "<h3 style='color:" + color + ";border-bottom:2px solid " + color + ";padding-bottom:5px;margin-top:20px;'>Links</h3>"
        if session_data.get('linkedin'):
            social_html += f"<p style='margin:5px 0;'>\ud83d\udd17 <a href='{session_data['linkedin']}' style='color:{color};'>LinkedIn</a></p>"
        if session_data.get('github'):
            social_html += f"<p style='margin:5px 0;'>\ud83d\udd17 <a href='{session_data['github']}' style='color:{color};'>GitHub</a></p>"
        if session_data.get('portfolio'):
            social_html += f"<p style='margin:5px 0;'>\ud83d\udd17 <a href='{session_data['portfolio']}' style='color:{color};'>Portfolio</a></p>"
    
    # Skills section
    skills_html = ""
    if tech_skills or soft_skills:
        skills_html = f"<h3 style='color:{color};border-bottom:2px solid {color};padding-bottom:5px;margin-top:20px;'>Skills</h3>"
        if tech_skills:
            skills_html += f"<p style='margin:8px 0;'><strong>Technical:</strong> {tech_skills}</p>"
        if soft_skills:
            skills_html += f"<p style='margin:8px 0;'><strong>Soft Skills:</strong> {soft_skills}</p>"
    
    # Generate based on layout
    if layout == "Two Column":
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: '{font}', sans-serif;
                    color: #333;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    display: flex;
                    gap: 30px;
                }}
                .left-column {{
                    width: 35%;
                    background: #f8f9fa;
                    padding: 25px;
                    border-radius: 10px;
                }}
                .right-column {{
                    width: 65%;
                }}
                h2 {{
                    color: {color};
                    margin: 0 0 10px 0;
                    font-size: 2rem;
                }}
                h3 {{
                    color: {color};
                    border-bottom: 2px solid {color};
                    padding-bottom: 5px;
                    margin-top: 20px;
                }}
                @media print {{
                    body {{ padding: 0; }}
                    .container {{ max-width: 100%; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="left-column">
                    <div style="text-align:center;">
                        {photo_html}
                    </div>
                    {contact_html}
                    {lang_html}
                    {social_html}
                    {skills_html}
                </div>
                <div class="right-column">
                    <h2>{name}</h2>
                    <p style="font-size:1.2rem;color:#666;margin:5px 0 20px 0;"><strong>{session_data.get('job_title_target', '')}</strong></p>
                    <h3 style="color:{color};">Professional Summary</h3>
                    <p>{summary}</p>
                    {work_html}
                    {project_html}
                    {edu_html}
                    {cert_html}
                </div>
            </div>
            <div style="text-align:center;margin-top:30px;color:#999;font-size:0.9rem;">
                <p>Created with SoulvestAI Resume Builder ✨</p>
            </div>
        </body>
        </html>
        """
    else:  # Single Column
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: '{font}', sans-serif;
                    color: #333;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    max-width: 800px;
                    margin: 0 auto;
                }}
                h2 {{
                    color: {color};
                    margin: 0 0 5px 0;
                    font-size: 2rem;
                }}
                h3 {{
                    color: {color};
                    border-bottom: 2px solid {color};
                    padding-bottom: 5px;
                    margin-top: 25px;
                }}
                @media print {{
                    body {{ padding: 10px; }}
                }}
            </style>
        </head>
        <body>
            <div style="text-align:center;">
                {photo_html}
            </div>
            <h2 style="text-align:center;">{name}</h2>
            <p style="text-align:center;font-size:1.2rem;color:#666;margin:5px 0;"><strong>{session_data.get('job_title_target', '')}</strong></p>
            {contact_html}
            <h3 style="color:{color};">Professional Summary</h3>
            <p>{summary}</p>
            {skills_html}
            {work_html}
            {project_html}
            {edu_html}
            {cert_html}
            {lang_html}
            {social_html}
            <div style="text-align:center;margin-top:30px;color:#999;font-size:0.9rem;">
                <p>Created with SoulvestAI Resume Builder ✨</p>
            </div>
        </body>
        </html>
        """
    
    return html
