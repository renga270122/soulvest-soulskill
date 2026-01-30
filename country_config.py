# country_config.py
# Global country-specific resume configurations

COUNTRIES = {
    "United States": {
        "code": "US",
        "resume_length": "1-2 pages",
        "photo": False,
        "personal_info": ["name", "phone", "email", "linkedin", "location_city_state"],
        "date_format": "MM/DD/YYYY",
        "standard_sections": ["Summary", "Experience", "Education", "Skills"],
        "tips": [
            "No photo on resume (illegal to request)",
            "No age, marital status, or personal details",
            "Focus on achievements and metrics",
            "Use action verbs and quantify results",
            "Reverse chronological order"
        ],
        "popular_formats": ["Chronological", "Functional", "Combination"]
    },
    "United Kingdom": {
        "code": "UK",
        "resume_length": "2 pages max",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "address"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Personal Statement", "Employment History", "Education", "Skills"],
        "tips": [
            "Called 'CV' (Curriculum Vitae)",
            "Photo optional but increasingly common",
            "Include detailed employment history",
            "Education typically before experience",
            "Professional tone, clear structure"
        ],
        "popular_formats": ["Chronological", "Skills-based"]
    },
    "Canada": {
        "code": "CA",
        "resume_length": "1-2 pages",
        "photo": False,
        "personal_info": ["name", "phone", "email", "linkedin", "city_province"],
        "date_format": "YYYY-MM-DD",
        "standard_sections": ["Professional Summary", "Work Experience", "Education", "Skills"],
        "tips": [
            "Similar to US format",
            "No photo, age, or marital status",
            "Bilingual resumes (English/French) for Quebec",
            "Focus on accomplishments",
            "Clear and concise"
        ],
        "popular_formats": ["Chronological", "Functional"]
    },
    "Australia": {
        "code": "AU",
        "resume_length": "2-3 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "location"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Career Summary", "Key Skills", "Professional Experience", "Education"],
        "tips": [
            "Photo optional",
            "Can include referees",
            "Detailed work history acceptable",
            "Professional and comprehensive",
            "Include volunteer work if relevant"
        ],
        "popular_formats": ["Chronological", "Functional"]
    },
    "Germany": {
        "code": "DE",
        "resume_length": "2-3 pages",
        "photo": "Expected",
        "personal_info": ["name", "address", "phone", "email", "date_of_birth", "nationality"],
        "date_format": "DD.MM.YYYY",
        "standard_sections": ["Persönliche Daten", "Berufserfahrung", "Ausbildung", "Kenntnisse"],
        "tips": [
            "Professional photo required",
            "Include date of birth and marital status",
            "Detailed and formal",
            "Include all certificates and qualifications",
            "Sign and date the CV"
        ],
        "popular_formats": ["Chronological", "Europass"]
    },
    "France": {
        "code": "FR",
        "resume_length": "1-2 pages",
        "photo": "Recommended",
        "personal_info": ["name", "address", "phone", "email", "age", "marital_status"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Profil", "Expérience Professionnelle", "Formation", "Compétences"],
        "tips": [
            "Photo highly recommended",
            "Include age and marital status",
            "Formal and structured",
            "Chronological order preferred",
            "Include language proficiency levels"
        ],
        "popular_formats": ["Chronological", "Europass"]
    },
    "Singapore": {
        "code": "SG",
        "resume_length": "2 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "nationality", "age"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Career Summary", "Work Experience", "Education", "Skills"],
        "tips": [
            "Include nationality and age",
            "Photo optional but common",
            "Highlight multilingual abilities",
            "Include expected salary if requested",
            "Professional and concise"
        ],
        "popular_formats": ["Chronological", "Functional"]
    },
    "United Arab Emirates": {
        "code": "AE",
        "resume_length": "2-3 pages",
        "photo": "Recommended",
        "personal_info": ["name", "phone", "email", "nationality", "visa_status", "age"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Professional Summary", "Professional Experience", "Education", "Skills"],
        "tips": [
            "Include nationality and visa status",
            "Photo recommended",
            "List expected salary",
            "Include references",
            "Highlight international experience"
        ],
        "popular_formats": ["Chronological"]
    },
    "India": {
        "code": "IN",
        "resume_length": "1-2 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "city", "state"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Career Objective", "Professional Experience", "Education", "Skills"],
        "tips": [
            "Photo optional",
            "Include age, marital status often requested",
            "Detailed educational background",
            "Include languages known",
            "Father's name sometimes included"
        ],
        "popular_formats": ["Chronological", "Functional"]
    },
    "China": {
        "code": "CN",
        "resume_length": "1-2 pages",
        "photo": "Required",
        "personal_info": ["name", "phone", "email", "age", "gender", "marital_status", "hukou"],
        "date_format": "YYYY-MM-DD",
        "standard_sections": ["个人信息", "工作经历", "教育背景", "技能"],
        "tips": [
            "Professional photo required",
            "Include age, gender, marital status",
            "List political affiliation if applicable",
            "Include hukou (household registration)",
            "Detailed and formal"
        ],
        "popular_formats": ["Chronological"]
    },
    "Japan": {
        "code": "JP",
        "resume_length": "Specific format",
        "photo": "Required",
        "personal_info": ["name", "address", "phone", "email", "age", "gender"],
        "date_format": "YYYY/MM/DD",
        "standard_sections": ["学歴", "職歴", "資格", "志望動機"],
        "tips": [
            "Use Rirekisho format (履歴書)",
            "Professional photo required",
            "Handwritten sometimes preferred",
            "Include family composition",
            "Very formal and structured"
        ],
        "popular_formats": ["Rirekisho Standard"]
    },
    "Brazil": {
        "code": "BR",
        "resume_length": "1-2 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "city", "state"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Objetivo", "Experiência", "Formação", "Habilidades"],
        "tips": [
            "Photo optional",
            "Include objective statement",
            "Portuguese language",
            "Professional and direct",
            "Highlight education prominently"
        ],
        "popular_formats": ["Chronological", "Functional"]
    },
    "Netherlands": {
        "code": "NL",
        "resume_length": "2 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "city"],
        "date_format": "DD-MM-YYYY",
        "standard_sections": ["Profiel", "Werkervaring", "Opleiding", "Vaardigheden"],
        "tips": [
            "Photo optional",
            "Clear and concise",
            "English increasingly accepted",
            "Include motivation letter",
            "Highlight language skills"
        ],
        "popular_formats": ["Chronological", "Europass"]
    },
    "Sweden": {
        "code": "SE",
        "resume_length": "2-3 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "city"],
        "date_format": "YYYY-MM-DD",
        "standard_sections": ["Profil", "Arbetslivserfarenhet", "Utbildning", "Kompetenser"],
        "tips": [
            "Photo optional but becoming common",
            "Personal number not required",
            "Can be detailed",
            "Highlight teamwork and collaboration",
            "Include references"
        ],
        "popular_formats": ["Chronological"]
    },
    "South Africa": {
        "code": "ZA",
        "resume_length": "2-3 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "linkedin", "city"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Profile", "Work Experience", "Education", "Skills"],
        "tips": [
            "Photo optional",
            "Race and ID number previously common (now discouraged)",
            "Include driver's license if relevant",
            "List languages spoken",
            "Professional references expected"
        ],
        "popular_formats": ["Chronological", "Functional"]
    },
    "Mexico": {
        "code": "MX",
        "resume_length": "1-2 pages",
        "photo": "Optional",
        "personal_info": ["name", "phone", "email", "city", "state"],
        "date_format": "DD/MM/YYYY",
        "standard_sections": ["Objetivo", "Experiencia Laboral", "Educación", "Habilidades"],
        "tips": [
            "Photo optional but common",
            "Spanish language",
            "Include objective statement",
            "Professional tone",
            "Highlight education and certifications"
        ],
        "popular_formats": ["Chronological"]
    },
    "South Korea": {
        "code": "KR",
        "resume_length": "1-2 pages",
        "photo": "Required",
        "personal_info": ["name", "age", "gender", "phone", "email", "address"],
        "date_format": "YYYY.MM.DD",
        "standard_sections": ["학력", "경력", "자격증", "기타"],
        "tips": [
            "Professional photo required",
            "Include age, gender, marital status",
            "Family background often included",
            "Very formal structure",
            "Include military service for men"
        ],
        "popular_formats": ["Standard Korean format"]
    }
}

# Global major cities database
GLOBAL_CITIES = {
    "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", "Newcastle", "Sheffield", "Bristol", "Edinburgh"],
    "Canada": ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Canberra", "Newcastle", "Wollongong", "Hobart"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig"],
    "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"],
    "Singapore": ["Singapore"],
    "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"],
    "India": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"],
    "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Hangzhou", "Wuhan", "Nanjing", "Tianjin", "Xi'an"],
    "Japan": ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto", "Kawasaki", "Saitama"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", "Tilburg", "Groningen", "Almere", "Breda", "Nijmegen"],
    "Sweden": ["Stockholm", "Gothenburg", "Malmö", "Uppsala", "Västerås", "Örebro", "Linköping", "Helsingborg", "Jönköping", "Norrköping"],
    "South Africa": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth", "Bloemfontein", "East London", "Polokwane", "Pietermaritzburg", "Nelspruit"],
    "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "León", "Juárez", "Zapopan", "Mérida", "San Luis Potosí"],
    "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Suwon", "Ulsan", "Changwon", "Goyang"]
}

def get_country_guidelines(country):
    """Get resume guidelines for specific country"""
    return COUNTRIES.get(country, COUNTRIES["United States"])

def should_include_photo(country):
    """Check if photo should be included based on country"""
    country_info = COUNTRIES.get(country, {})
    photo_policy = country_info.get("photo", False)
    return photo_policy in [True, "Required", "Recommended", "Expected"]
