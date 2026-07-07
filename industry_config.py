# industry_config.py
# Industry-specific configurations for Indian job market

INDUSTRY_OPTIONS = [
    "Information Technology (IT)",
    "Software Development",
    "Healthcare & Medical",
    "Finance & Banking",
    "Education & Training",
    "Manufacturing & Production",
    "E-commerce & Retail",
    "Telecommunications",
    "Consulting & Advisory",
    "Marketing & Advertising",
    "Human Resources",
    "Hospitality & Tourism",
    "Real Estate & Construction",
    "Media & Entertainment",
    "Logistics & Supply Chain",
    "Agriculture & Food Processing",
    "Automobile & Auto Components",
    "Pharmaceuticals & Biotech",
    "Government & Public Sector",
    "NGO & Social Services",
    "Legal Services",
    "Architecture & Design",
    "Sales & Business Development",
    "Customer Service & Support",
    "Data Science & Analytics"
]

# Industry-specific keywords to help candidates
INDUSTRY_KEYWORDS = {
    "Information Technology (IT)": [
        "Software Development", "Agile", "DevOps", "Cloud Computing", "Cybersecurity",
        "System Administration", "Network Management", "IT Infrastructure", "ITIL",
        "Project Management", "Technical Support", "Database Management"
    ],
    "Software Development": [
        "Python", "Java", "JavaScript", "React", "Node.js", "Angular", "SQL",
        "Git", "REST API", "Microservices", "CI/CD", "Docker", "Kubernetes",
        "AWS", "Azure", "Agile/Scrum", "Test-Driven Development", "Full Stack"
    ],
    "Healthcare & Medical": [
        "Patient Care", "Medical Records", "Healthcare Management", "Clinical Research",
        "HIPAA Compliance", "Electronic Health Records (EHR)", "Medical Billing",
        "Healthcare IT", "Pharmaceutical Knowledge", "Clinical Trials", "Lab Management"
    ],
    "Finance & Banking": [
        "Financial Analysis", "Risk Management", "Portfolio Management", "Investment Banking",
        "Corporate Finance", "Excel", "Financial Modeling", "Compliance", "Audit",
        "Accounting", "Tax Planning", "Treasury Management", "Credit Analysis", "KYC"
    ],
    "Education & Training": [
        "Curriculum Development", "Lesson Planning", "Classroom Management",
        "Student Assessment", "Educational Technology", "E-learning", "Mentoring",
        "Training Delivery", "Learning Management Systems (LMS)", "CBSE/ICSE", "Pedagogy"
    ],
    "Manufacturing & Production": [
        "Lean Manufacturing", "Six Sigma", "Quality Control", "Production Planning",
        "Supply Chain Management", "ISO Standards", "Kaizen", "5S", "TPM",
        "Process Optimization", "Inventory Management", "Safety Compliance"
    ],
    "E-commerce & Retail": [
        "Customer Service", "Inventory Management", "Visual Merchandising",
        "Sales Strategy", "E-commerce Platforms", "Digital Marketing", "CRM",
        "Logistics", "Point of Sale (POS)", "Product Management", "Category Management"
    ],
    "Marketing & Advertising": [
        "Digital Marketing", "SEO", "SEM", "Social Media Marketing", "Content Marketing",
        "Brand Management", "Market Research", "Campaign Management", "Google Analytics",
        "Marketing Automation", "Email Marketing", "Influencer Marketing", "Copywriting"
    ],
    "Data Science & Analytics": [
        "Python", "R", "Machine Learning", "Deep Learning", "SQL", "Statistics",
        "Data Visualization", "Tableau", "Power BI", "Big Data", "Hadoop", "Spark",
        "NLP", "TensorFlow", "PyTorch", "Predictive Modeling", "A/B Testing"
    ],
    "Human Resources": [
        "Recruitment", "Talent Acquisition", "Employee Relations", "Performance Management",
        "HR Analytics", "Compensation & Benefits", "HRIS", "Training & Development",
        "Labor Laws", "Organizational Development", "Payroll Management"
    ],
    "Consulting & Advisory": [
        "Business Strategy", "Management Consulting", "Process Improvement",
        "Change Management", "Stakeholder Management", "Client Relationship",
        "Problem Solving", "Presentation Skills", "Industry Analysis", "Market Entry"
    ],
    "Telecommunications": [
        "Network Operations", "Telecom Infrastructure", "RF Engineering", "OSS/BSS",
        "4G/5G Technology", "VoIP", "Network Security", "Fiber Optics", "Bandwidth Management"
    ],
    "Real Estate & Construction": [
        "Project Management", "Site Supervision", "AutoCAD", "Cost Estimation",
        "Quality Assurance", "Contract Management", "Building Codes", "Structural Analysis",
        "Real Estate Valuation", "Property Management", "RERA Compliance"
    ],
    "Logistics & Supply Chain": [
        "Supply Chain Management", "Warehouse Management", "Transportation Management",
        "Inventory Optimization", "ERP (SAP)", "Demand Planning", "Vendor Management",
        "Last Mile Delivery", "Cold Chain", "Customs Clearance", "Freight Forwarding"
    ],
    "Hospitality & Tourism": [
        "Guest Services", "Hotel Management", "Food & Beverage", "Event Management",
        "Front Office Operations", "Housekeeping Management", "Revenue Management",
        "Tour Planning", "Customer Relations", "Hospitality Software"
    ],
    "Pharmaceuticals & Biotech": [
        "Drug Development", "Clinical Trials", "Regulatory Affairs", "Quality Assurance",
        "GMP Compliance", "Pharmacovigilance", "Medical Writing", "R&D",
        "Pharmaceutical Manufacturing", "FDA Regulations", "Analytical Chemistry"
    ],
    "Legal Services": [
        "Contract Law", "Corporate Law", "Litigation", "Legal Research",
        "Compliance", "Intellectual Property", "Labour Law", "Legal Documentation",
        "Due Diligence", "Arbitration", "Legal Advisory"
    ],
    "Sales & Business Development": [
        "B2B Sales", "B2C Sales", "Lead Generation", "Client Acquisition",
        "Account Management", "Sales Strategy", "CRM (Salesforce)", "Negotiation",
        "Market Expansion", "Revenue Growth", "Partnership Development"
    ],
    "Customer Service & Support": [
        "Customer Relationship Management", "Issue Resolution", "Call Center Operations",
        "Ticketing Systems", "Customer Satisfaction", "Communication Skills",
        "Problem Solving", "Multi-channel Support", "CRM Software", "Service Excellence"
    ]
}

# Location data for Indian job market
MAJOR_INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune",
    "Ahmedabad", "Jaipur", "Lucknow", "Surat", "Kanpur", "Nagpur", "Indore",
    "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara",
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot",
    "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai",
    "Allahabad", "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada",
    "Jodhpur", "Madurai", "Raipur", "Kota", "Chandigarh", "Guwahati", "Noida"
]

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]
