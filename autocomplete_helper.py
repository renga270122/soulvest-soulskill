"""
Autocomplete Helper for Text Inputs
Provides suggestions while typing
"""
import streamlit as st
from typing import List

# Common job titles across industries
JOB_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Lead Software Engineer",
    "Full Stack Developer", "Frontend Developer", "Backend Developer",
    "Data Scientist", "Data Analyst", "Data Engineer",
    "Product Manager", "Project Manager", "Program Manager",
    "Business Analyst", "Systems Analyst", "QA Engineer",
    "DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer",
    "UI/UX Designer", "Graphic Designer", "Product Designer",
    "Marketing Manager", "Digital Marketing Specialist", "Content Writer",
    "Sales Manager", "Account Manager", "Business Development Manager",
    "HR Manager", "Recruiter", "Talent Acquisition Specialist",
    "Financial Analyst", "Accountant", "Finance Manager",
    "Operations Manager", "Supply Chain Manager", "Logistics Coordinator",
    "Mechanical Engineer", "Electrical Engineer", "Civil Engineer",
    "Teacher", "Professor", "Training Specialist",
    "Nurse", "Doctor", "Healthcare Administrator",
    "Customer Success Manager", "Support Engineer", "Technical Support"
]

# Popular technical skills
TECHNICAL_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "PHP", "Ruby",
    "Swift", "Kotlin", "R", "MATLAB", "Scala", "Perl", "Shell Scripting", "SQL",
    
    # Web Technologies
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
    "FastAPI", "Spring Boot", "ASP.NET", "jQuery", "Bootstrap", "Tailwind CSS",
    
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQL Server", "Redis", "Cassandra",
    "DynamoDB", "Firebase", "Elasticsearch",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud Platform", "Docker", "Kubernetes", "Jenkins", "GitLab CI",
    "GitHub Actions", "Terraform", "Ansible", "CircleCI",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas",
    "NumPy", "Jupyter", "Tableau", "Power BI", "Apache Spark", "Hadoop",
    
    # Other Tools
    "Git", "Linux", "Agile", "Scrum", "Jira", "Confluence", "REST API", "GraphQL",
    "Microservices", "CI/CD", "Unit Testing", "Integration Testing"
]

# Common companies (Indian and Global)
COMPANIES = [
    # Indian IT Companies
    "TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "L&T Infotech",
    "Mindtree", "Mphasis", "Capgemini India", "Accenture India",
    
    # Global Tech Giants
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "IBM", "Oracle", "SAP", "Adobe",
    "Salesforce", "Intel", "NVIDIA", "Cisco", "Dell", "HP",
    
    # Startups & Unicorns
    "Flipkart", "Paytm", "Zomato", "Swiggy", "Ola", "Byju's", "Razorpay", "PhonePe",
    "Freshworks", "Zoho", "InMobi", "ShareChat", "Meesho",
    
    # Consulting
    "Deloitte", "PwC", "EY", "KPMG", "McKinsey", "BCG", "Bain & Company",
    
    # Banks & Finance
    "HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Kotak Mahindra", "JP Morgan", "Goldman Sachs"
]

# Indian cities
CITIES = [
    "Bangalore", "Bengaluru", "Mumbai", "Delhi", "New Delhi", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Kochi",
    "Indore", "Coimbatore", "Nagpur", "Visakhapatnam", "Bhopal", "Gurgaon", "Noida",
    "Ghaziabad", "Mysore", "Surat", "Vadodara", "Rajkot", "Bhubaneswar", "Thiruvananthapuram"
]

def create_autocomplete_text_input(label: str, suggestions: List[str], key: str, 
                                   value: str = "", placeholder: str = "", 
                                   help_text: str = None) -> str:
    """
    Create a text input with autocomplete suggestions
    
    Args:
        label: Label for the input field
        suggestions: List of suggestions to show
        key: Unique key for the input
        value: Default value
        placeholder: Placeholder text
        help_text: Help text to display
    
    Returns:
        The input value
    """
    # Create a unique ID for the datalist
    datalist_id = f"datalist_{key}"
    
    # Inject HTML for datalist
    datalist_html = f"""
    <datalist id="{datalist_id}">
        {''.join([f'<option value="{item}">' for item in suggestions])}
    </datalist>
    """
    
    # Create the input with autocomplete
    col1, col2 = st.columns([4, 1])
    with col1:
        # Render datalist
        st.markdown(datalist_html, unsafe_allow_html=True)
        
        # Create text input
        user_input = st.text_input(
            label, 
            value=value, 
            placeholder=placeholder or f"Type to see suggestions...",
            key=key,
            help=help_text
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💡", key=f"suggest_{key}", help="Show suggestions"):
            st.info(f"**Popular choices:**\n" + "\n".join([f"• {s}" for s in suggestions[:5]]))
    
    return user_input


def get_skill_suggestions(current_skills: str, job_title: str = "") -> List[str]:
    """Get relevant skill suggestions based on current skills and job title"""
    current_skills_lower = current_skills.lower()
    job_title_lower = job_title.lower()
    
    # Filter skills that aren't already added
    available_skills = [s for s in TECHNICAL_SKILLS 
                       if s.lower() not in current_skills_lower]
    
    # Prioritize skills related to job title
    if any(word in job_title_lower for word in ["data", "analyst", "scientist"]):
        priority_skills = ["Python", "SQL", "Pandas", "NumPy", "Tableau", "Power BI", "Excel"]
    elif any(word in job_title_lower for word in ["frontend", "ui", "ux"]):
        priority_skills = ["React", "Angular", "Vue.js", "JavaScript", "TypeScript", "CSS", "HTML"]
    elif any(word in job_title_lower for word in ["backend", "api"]):
        priority_skills = ["Python", "Java", "Node.js", "SQL", "REST API", "Docker", "Kubernetes"]
    elif any(word in job_title_lower for word in ["devops", "cloud", "sre"]):
        priority_skills = ["AWS", "Docker", "Kubernetes", "Jenkins", "Terraform", "Linux", "CI/CD"]
    elif any(word in job_title_lower for word in ["full", "stack"]):
        priority_skills = ["React", "Node.js", "Python", "JavaScript", "SQL", "Docker", "Git"]
    else:
        priority_skills = []
    
    # Combine priority skills with general skills
    suggested = []
    for skill in priority_skills:
        if skill in available_skills:
            suggested.append(skill)
            available_skills.remove(skill)
    
    # Add remaining skills
    suggested.extend(available_skills[:10])
    
    return suggested[:15]
