# template_config.py

TEMPLATES = {
    "Classic": {"font": "Georgia", "color": "#333"},
    "Modern": {"font": "Verdana", "color": "#2c3e50"},
    "Soulful": {"font": "Helvetica", "color": "#4b0082"},
    "Minimalist": {"font": "Arial", "color": "#000"}
}

# Indian-specific professional templates
INDIAN_TEMPLATES = {
    "Professional Blue": {
        "font": "Calibri",
        "color": "#003366",
        "theme": "corporate",
        "description": "Ideal for IT, Banking, Corporate (NO photo - India standard)",
        "ats_score": 95,
        "photo_discouraged": True
    },
    "Creative Gradient": {
        "font": "Montserrat",
        "color": "#667eea",
        "theme": "creative",
        "description": "Perfect for Marketing, Design, and Media roles",
        "ats_score": 88
    },
    "Traditional Formal": {
        "font": "Times New Roman",
        "color": "#1a1a1a",
        "theme": "formal",
        "description": "Best for Government, Legal, and Academic positions",
        "ats_score": 92
    },
    "Tech Innovator": {
        "font": "Roboto",
        "color": "#00796b",
        "theme": "tech",
        "description": "Suited for Software Development and Tech startups",
        "ats_score": 94
    },
    "Healthcare Pro": {
        "font": "Arial",
        "color": "#004d40",
        "theme": "medical",
        "description": "Designed for Healthcare and Medical professionals",
        "ats_score": 90
    },
    "Executive Style": {
        "font": "Garamond",
        "color": "#2c1810",
        "theme": "executive",
        "description": "For Senior Management and C-level positions",
        "ats_score": 93
    }
}

# US-specific templates
US_TEMPLATES = {
    "Harvard Business": {
        "font": "Times New Roman",
        "color": "#000000",
        "theme": "academic",
        "description": "Traditional US format (NO photo - reduces ATS score)",
        "ats_score": 96,
        "photo_discouraged": True
    },
    "Silicon Valley Tech": {
        "font": "Helvetica",
        "color": "#0066cc",
        "theme": "tech",
        "description": "Clean, modern format for tech companies and startups",
        "ats_score": 94
    },
    "Wall Street Executive": {
        "font": "Garamond",
        "color": "#1a1a2e",
        "theme": "finance",
        "description": "Professional format for finance and banking sectors",
        "ats_score": 95
    },
    "Creative LA": {
        "font": "Avenir",
        "color": "#e63946",
        "theme": "creative",
        "description": "Bold design for entertainment, media, and creative industries",
        "ats_score": 85
    }
}

# UK-specific templates
UK_TEMPLATES = {
    "British Standard": {
        "font": "Arial",
        "color": "#0f0f0f",
        "theme": "formal",
        "description": "Traditional UK CV (NO photo - UK standard practice)",
        "ats_score": 93,
        "photo_discouraged": True
    },
    "London Financial": {
        "font": "Calibri",
        "color": "#003366",
        "theme": "finance",
        "description": "Professional format for City of London firms",
        "ats_score": 95
    },
    "Cambridge Academic": {
        "font": "Times New Roman",
        "color": "#641e16",
        "theme": "academic",
        "description": "Academic CV format for universities and research",
        "ats_score": 94
    }
}

# Canada-specific templates
CANADA_TEMPLATES = {
    "Canadian Professional": {
        "font": "Arial",
        "color": "#003d82",
        "theme": "corporate",
        "description": "Bilingual-friendly format for Canadian market",
        "ats_score": 94
    },
    "Toronto Tech": {
        "font": "Verdana",
        "color": "#00695c",
        "theme": "tech",
        "description": "Modern format for Canadian tech hubs",
        "ats_score": 93
    }
}

# Australia-specific templates
AUSTRALIA_TEMPLATES = {
    "Aussie Standard": {
        "font": "Arial",
        "color": "#004d00",
        "theme": "corporate",
        "description": "Standard Australian resume format",
        "ats_score": 92
    },
    "Sydney Professional": {
        "font": "Calibri",
        "color": "#01579b",
        "theme": "professional",
        "description": "Modern format for Australian corporate sector",
        "ats_score": 94
    }
}

# Germany-specific templates (Lebenslauf)
GERMANY_TEMPLATES = {
    "German Lebenslauf": {
        "font": "Arial",
        "color": "#000000",
        "theme": "formal",
        "description": "Traditional German CV (photo often expected in Germany)",
        "ats_score": 95,
        "photo_expected": True
    },
    "Berlin Tech": {
        "font": "Helvetica",
        "color": "#263238",
        "theme": "tech",
        "description": "Modern format for German tech startups",
        "ats_score": 91
    }
}

# France-specific templates
FRANCE_TEMPLATES = {
    "French CV": {
        "font": "Arial",
        "color": "#0055a4",
        "theme": "formal",
        "description": "Standard French CV (photo sometimes expected)",
        "ats_score": 93,
        "photo_expected": True
    },
    "Paris Creative": {
        "font": "Verdana",
        "color": "#8b1538",
        "theme": "creative",
        "description": "Elegant format for creative industries (photo may be required)",
        "ats_score": 87
    }
}

# UAE/Middle East-specific templates
UAE_TEMPLATES = {
    "Dubai Professional": {
        "font": "Arial",
        "color": "#b8860b",
        "theme": "corporate",
        "description": "Professional format for UAE and Middle East markets",
        "ats_score": 94
    },
    "Gulf Executive": {
        "font": "Calibri",
        "color": "#1a237e",
        "theme": "executive",
        "description": "Executive format for senior positions in Gulf countries",
        "ats_score": 95
    }
}

# Singapore-specific templates
SINGAPORE_TEMPLATES = {
    "Singapore Standard": {
        "font": "Arial",
        "color": "#ed1c24",
        "theme": "corporate",
        "description": "Standard format for Singapore job market",
        "ats_score": 94
    },
    "Asia-Pacific Tech": {
        "font": "Verdana",
        "color": "#00838f",
        "theme": "tech",
        "description": "Modern format for tech roles in Asia-Pacific",
        "ats_score": 93
    }
}
