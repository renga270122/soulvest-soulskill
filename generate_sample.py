from resume_generator import generate_resume_html

# Sample resume data with correct field names
session_data = {
    'full_name': 'Priya Sharma',
    'email': 'priya.sharma@email.com',
    'phone': '+91 98765 43210',
    'city': 'Bangalore',
    'state': 'Karnataka',
    'linkedin': 'linkedin.com/in/priyasharma',
    'github': 'github.com/priyasharma',
    'summary': 'Results-driven Software Engineer with 5+ years of experience in full-stack development. Expertise in Python, React, and cloud technologies. Proven track record of delivering scalable solutions and leading cross-functional teams.',
    'tech_skills': 'Python • React • Node.js • AWS • Docker • PostgreSQL • Git • CI/CD',
    'soft_skills': 'Team Leadership • Problem Solving • Communication • Agile Methodology',
    'work_entries': [
        {
            'title': 'Software Engineer',
            'company': 'Tech Solutions India',
            'duration': 'Jan 2020 - Present',
            'responsibilities': '• Led development of microservices architecture serving 1M+ users\n• Reduced API response time by 40% through optimization\n• Mentored 3 junior developers in best practices\n• Implemented CI/CD pipeline reducing deployment time by 60%'
        },
        {
            'title': 'Junior Developer',
            'company': 'StartUp Innovations',
            'duration': 'Jun 2019 - Dec 2019',
            'responsibilities': '• Developed RESTful APIs using Django and PostgreSQL\n• Created responsive UI components with React\n• Collaborated with design team on user experience improvements'
        }
    ],
    'education_entries': [
        {
            'degree': 'Bachelor of Technology',
            'stream': 'Computer Science',
            'institution': 'Indian Institute of Technology',
            'university': 'Delhi',
            'year': '2019',
            'grade': 'CGPA: 8.5/10'
        }
    ],
    'project_entries': [
        {
            'name': 'E-Commerce Platform',
            'description': 'Built scalable e-commerce platform with React and Node.js, handling 10,000+ daily transactions',
            'technologies': 'React, Node.js, MongoDB, AWS, Docker'
        },
        {
            'name': 'Task Management API',
            'description': 'Developed RESTful API for task management with authentication and real-time updates',
            'technologies': 'Python, Django, PostgreSQL, Redis'
        }
    ],
    'certification_entries': [
        {
            'name': 'AWS Certified Solutions Architect',
            'issuer': 'Amazon Web Services',
            'year': '2022'
        },
        {
            'name': 'Professional Scrum Master I',
            'issuer': 'Scrum.org',
            'year': '2021'
        }
    ],
    'layout': 'Single Column'
}

# Template configuration
template_config = {
    'name': 'Professional',
    'font': 'Arial, sans-serif',
    'color': '#2C5AA0',
    'layout': 'Single Column'
}

# Generate HTML resume
print("Generating resume...")
html_resume = generate_resume_html(session_data, template_config)

# Save to file
output_file = 'sample_resume.html'
with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
    f.write(html_resume)

print(f"✓ SUCCESS: Sample resume generated!")
print(f"✓ Saved to: {output_file}")
print(f"✓ Resume length: {len(html_resume):,} characters")
print(f"\nOpen {output_file} in your browser to view the resume!")
