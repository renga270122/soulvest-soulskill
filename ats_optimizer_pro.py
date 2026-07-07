# ats_optimizer_pro.py
# Enterprise-Grade ATS Optimization - Matching Rezi, Kickresume, Enhancv Standards
# Advanced keyword analysis, formatting checks, and competitive benchmarking

import re
from typing import Dict, List, Tuple, Set
from collections import Counter
import json

class EnterpriseATSOptimizer:
    """Advanced ATS Optimizer matching top 2026 resume builders"""
    
    # Industry-specific ATS keywords database
    INDUSTRY_KEYWORDS = {
        "Technology": ["agile", "scrum", "devops", "ci/cd", "cloud", "aws", "azure", "kubernetes", 
                      "docker", "microservices", "api", "rest", "graphql", "sql", "nosql", "python",
                      "java", "javascript", "react", "angular", "vue", "node", "machine learning",
                      "data science", "ai", "automation", "testing", "git", "jira"],
        "Finance": ["financial analysis", "budgeting", "forecasting", "gaap", "sox", "audit",
                   "compliance", "risk management", "portfolio management", "excel", "quickbooks",
                   "bloomberg", "derivatives", "equity", "debt", "treasury", "accounting"],
        "Healthcare": ["hipaa", "patient care", "ehr", "emr", "epic", "cerner", "clinical",
                      "diagnosis", "treatment", "medical coding", "icd", "cpt", "medicare",
                      "medicaid", "quality assurance", "infection control"],
        "Marketing": ["seo", "sem", "ppc", "social media", "content marketing", "email marketing",
                     "google analytics", "hubspot", "salesforce", "campaign management", "brand",
                     "roi", "conversion rate", "a/b testing", "copywriting", "market research"],
        "Sales": ["crm", "salesforce", "pipeline management", "lead generation", "b2b", "b2c",
                 "cold calling", "negotiation", "closing", "quota", "revenue", "account management",
                 "business development", "prospecting", "presentations"],
        "Engineering": ["cad", "autocad", "solidworks", "fea", "ansys", "matlab", "plc", "scada",
                       "lean manufacturing", "six sigma", "iso", "quality control", "r&d",
                       "prototyping", "testing", "validation"],
        "Education": ["curriculum development", "lesson planning", "classroom management", "assessment",
                     "differentiation", "special education", "iep", "common core", "pbis", "stem",
                     "student engagement", "learning outcomes", "pedagogy"],
        "Legal": ["litigation", "contract", "compliance", "due diligence", "legal research",
                 "westlaw", "lexisnexis", "discovery", "deposition", "trial", "brief writing",
                 "regulatory", "ip", "patent", "trademark"],
        "Business": ["strategic planning", "operations management", "process improvement", "kpi",
                    "stakeholder management", "change management", "business analysis", "reporting",
                    "budgeting", "p&l", "supply chain", "logistics", "vendor management"]
    }
    
    # ATS-friendly vs ATS-problematic words
    POWER_WORDS = [
        "achieved", "accelerated", "accomplished", "advanced", "analyzed", "architected",
        "automated", "built", "championed", "delivered", "designed", "developed", "directed",
        "drove", "elevated", "engineered", "enhanced", "established", "exceeded", "executed",
        "expanded", "generated", "grew", "implemented", "improved", "increased", "initiated",
        "innovated", "launched", "led", "managed", "optimized", "orchestrated", "outperformed",
        "pioneered", "produced", "reduced", "resolved", "restructured", "revamped", "scaled",
        "spearheaded", "streamlined", "strengthened", "transformed", "upgraded"
    ]
    
    WEAK_WORDS = [
        "responsible for", "duties included", "worked on", "helped with", "assisted",
        "participated in", "involved in", "tried to", "attempted to", "tasked with"
    ]
    
    @classmethod
    def comprehensive_ats_analysis(cls, resume_data: Dict, job_description: str = "") -> Dict:
        """Comprehensive ATS analysis matching Rezi/Kickresume quality"""
        
        analysis = {
            "overall_ats_score": 0,
            "keyword_optimization": {},
            "formatting_analysis": {},
            "content_strength": {},
            "competitive_benchmark": {},
            "actionable_improvements": [],
            "industry_specific_feedback": [],
            "detailed_scores": {}
        }
        
        # 1. Keyword Optimization Analysis
        analysis["keyword_optimization"] = cls._analyze_keywords(resume_data, job_description)
        
        # 2. Formatting Analysis
        analysis["formatting_analysis"] = cls._analyze_formatting(resume_data)
        
        # 3. Content Strength Analysis
        analysis["content_strength"] = cls._analyze_content_strength(resume_data)
        
        # 4. Competitive Benchmarking
        analysis["competitive_benchmark"] = cls._competitive_benchmarking(resume_data, job_description)
        
        # 5. Calculate detailed scores
        analysis["detailed_scores"] = {
            "keyword_density": analysis["keyword_optimization"].get("score", 0),
            "formatting_score": analysis["formatting_analysis"].get("score", 0),
            "content_quality": analysis["content_strength"].get("score", 0),
            "ats_compatibility": cls._calculate_ats_compatibility(resume_data),
            "impact_factor": analysis["content_strength"].get("impact_score", 0)
        }
        
        # 6. Overall ATS Score (weighted average)
        scores = analysis["detailed_scores"]
        analysis["overall_ats_score"] = int(
            scores["keyword_density"] * 0.25 +
            scores["formatting_score"] * 0.20 +
            scores["content_quality"] * 0.25 +
            scores["ats_compatibility"] * 0.20 +
            scores["impact_factor"] * 0.10
        )
        
        # 7. Generate Actionable Improvements
        analysis["actionable_improvements"] = cls._generate_improvements(analysis)
        
        # 8. Industry-Specific Feedback
        industry = resume_data.get("industry", "")
        analysis["industry_specific_feedback"] = cls._industry_feedback(resume_data, industry)
        
        return analysis
    
    @classmethod
    def _analyze_keywords(cls, resume_data: Dict, job_description: str) -> Dict:
        """Advanced keyword analysis with density calculation"""
        resume_text = json.dumps(resume_data).lower()
        jd_lower = job_description.lower()
        
        # Extract keywords from job description
        jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', jd_lower))
        
        # Remove common stop words
        stop_words = {'and', 'the', 'for', 'with', 'are', 'you', 'will', 'have', 'this', 
                     'that', 'from', 'they', 'been', 'their', 'your', 'can', 'has', 'had'}
        jd_keywords = jd_words - stop_words
        
        # Count keyword occurrences in resume
        keyword_matches = {}
        for keyword in jd_keywords:
            if len(keyword) > 3:  # Only meaningful keywords
                count = resume_text.count(keyword)
                if count > 0:
                    keyword_matches[keyword] = count
        
        # Identify missing critical keywords (appear multiple times in JD)
        jd_word_freq = Counter(re.findall(r'\b[a-zA-Z]{4,}\b', jd_lower))
        critical_keywords = {word: freq for word, freq in jd_word_freq.most_common(30) 
                           if word not in stop_words}
        
        missing_critical = []
        for keyword, freq in critical_keywords.items():
            if freq >= 3 and keyword not in resume_text:  # Appears 3+ times in JD but not in resume
                missing_critical.append({"keyword": keyword, "frequency_in_jd": freq})
        
        # Calculate keyword density
        total_resume_words = len(resume_text.split())
        keyword_density = len(keyword_matches) / len(jd_keywords) * 100 if jd_keywords else 0
        
        # Calculate optimal density (should be 60-80%)
        density_score = 100 if 60 <= keyword_density <= 80 else max(0, 100 - abs(keyword_density - 70))
        
        # Industry-specific keyword check
        industry = resume_data.get("industry", "")
        industry_keywords = cls.INDUSTRY_KEYWORDS.get(industry, [])
        industry_matches = sum(1 for kw in industry_keywords if kw in resume_text)
        industry_score = (industry_matches / len(industry_keywords) * 100) if industry_keywords else 70
        
        # Overall keyword score
        score = int((density_score * 0.6 + industry_score * 0.4))
        
        return {
            "score": score,
            "keyword_density_percent": round(keyword_density, 1),
            "matched_keywords": len(keyword_matches),
            "total_jd_keywords": len(jd_keywords),
            "missing_critical_keywords": missing_critical[:10],
            "industry_keyword_match": f"{industry_matches}/{len(industry_keywords)}",
            "top_matched_keywords": dict(sorted(keyword_matches.items(), key=lambda x: x[1], reverse=True)[:15]),
            "recommendation": cls._get_keyword_recommendation(score, keyword_density)
        }
    
    @classmethod
    def _analyze_formatting(cls, resume_data: Dict) -> Dict:
        """Analyze resume formatting for ATS compatibility"""
        issues = []
        warnings = []
        strengths = []
        score = 100
        
        # Check required sections
        required_sections = ['full_name', 'email', 'phone', 'summary', 'work_history', 'education']
        missing_sections = [s for s in required_sections if not resume_data.get(s)]
        
        if missing_sections:
            issues.append(f"Missing required sections: {', '.join(missing_sections)}")
            score -= len(missing_sections) * 10
        else:
            strengths.append("All required sections present")
        
        # Check contact information format
        email = resume_data.get('email', '')
        if email and '@' in email:
            strengths.append("Valid email format")
        else:
            issues.append("Email format may be invalid")
            score -= 10
        
        phone = resume_data.get('phone', '')
        if phone and any(char.isdigit() for char in phone):
            strengths.append("Phone number present")
        else:
            warnings.append("Phone number should be clearly formatted")
            score -= 5
        
        # Check work history quality
        work_history = resume_data.get('work_history', [])
        if len(work_history) > 0:
            strengths.append(f"{len(work_history)} work experience entries")
            
            # Check for dates
            has_dates = all('start_date' in job for job in work_history)
            if has_dates:
                strengths.append("Work experience includes dates")
            else:
                warnings.append("Add dates to all work experience")
                score -= 5
            
            # Check for descriptions
            has_descriptions = all(job.get('description') for job in work_history)
            if has_descriptions:
                strengths.append("Work experience includes descriptions")
            else:
                issues.append("Add descriptions to all work experience")
                score -= 15
        else:
            issues.append("No work experience listed")
            score -= 20
        
        # Check education section
        education = resume_data.get('education', [])
        if len(education) > 0:
            strengths.append(f"{len(education)} education entries")
        else:
            warnings.append("Consider adding education section")
            score -= 10
        
        # Check for skills section
        if resume_data.get('tech_skills') or resume_data.get('soft_skills'):
            strengths.append("Skills section present")
        else:
            issues.append("Add a skills section - critical for ATS")
            score -= 15
        
        # Check summary length (should be 3-5 sentences)
        summary = resume_data.get('summary', '')
        if summary:
            sentences = len(re.findall(r'[.!?]+', summary))
            if 3 <= sentences <= 5:
                strengths.append("Professional summary is optimal length")
            elif sentences < 3:
                warnings.append("Professional summary is too short")
                score -= 5
            else:
                warnings.append("Professional summary is too long")
                score -= 5
        
        # Check for quantifiable achievements (numbers)
        resume_text = json.dumps(work_history)
        numbers_count = len(re.findall(r'\b\d+[%\w]*\b', resume_text))
        if numbers_count >= 5:
            strengths.append(f"Good use of metrics ({numbers_count} quantifiable results)")
        else:
            warnings.append(f"Add more numbers/metrics (found {numbers_count}, aim for 5+)")
            score -= 10
        
        score = max(0, min(100, score))
        
        return {
            "score": score,
            "issues": issues,
            "warnings": warnings,
            "strengths": strengths,
            "grade": cls._get_grade(score),
            "recommendation": cls._get_formatting_recommendation(score)
        }
    
    @classmethod
    def _analyze_content_strength(cls, resume_data: Dict) -> Dict:
        """Analyze content quality and impact"""
        work_history = resume_data.get('work_history', [])
        
        power_verb_count = 0
        weak_phrase_count = 0
        impact_score = 50
        
        for job in work_history:
            description = job.get('description', '').lower()
            
            # Count power words
            power_verb_count += sum(1 for word in cls.POWER_WORDS if word in description)
            
            # Count weak phrases
            weak_phrase_count += sum(1 for phrase in cls.WEAK_WORDS if phrase in description)
        
        # Calculate content strength score
        if len(work_history) > 0:
            impact_score = 50 + (power_verb_count * 3) - (weak_phrase_count * 5)
            impact_score = max(0, min(100, impact_score))
        
        # Analyze bullet point quality
        bullet_analysis = cls._analyze_bullets(work_history)
        
        # Overall content score
        content_score = int((impact_score * 0.6) + (bullet_analysis["score"] * 0.4))
        
        return {
            "score": content_score,
            "impact_score": impact_score,
            "power_verbs_used": power_verb_count,
            "weak_phrases_found": weak_phrase_count,
            "bullet_analysis": bullet_analysis,
            "recommendations": cls._get_content_recommendations(power_verb_count, weak_phrase_count)
        }
    
    @classmethod
    def _analyze_bullets(cls, work_history: List[Dict]) -> Dict:
        """Analyze bullet point quality"""
        total_bullets = 0
        strong_bullets = 0
        
        for job in work_history:
            description = job.get('description', '')
            bullets = [b.strip() for b in description.split('\n') if b.strip()]
            total_bullets += len(bullets)
            
            for bullet in bullets:
                # Check if bullet starts with action verb
                first_word = bullet.split()[0].lower() if bullet.split() else ""
                if first_word in cls.POWER_WORDS:
                    strong_bullets += 1
                # Check if bullet contains metrics
                if re.search(r'\d+[%\w]*', bullet):
                    strong_bullets += 0.5
        
        score = int((strong_bullets / total_bullets * 100)) if total_bullets > 0 else 50
        
        return {
            "score": score,
            "total_bullets": total_bullets,
            "strong_bullets": int(strong_bullets),
            "recommendation": "Excellent bullet points!" if score >= 80 else 
                           "Good - add more action verbs" if score >= 60 else 
                           "Rewrite bullets to start with action verbs and include metrics"
        }
    
    @classmethod
    def _calculate_ats_compatibility(cls, resume_data: Dict) -> int:
        """Calculate ATS system compatibility score"""
        score = 85  # Base score for using structured format
        
        # Bonus for standard sections
        if resume_data.get('summary'):
            score += 3
        if resume_data.get('work_history'):
            score += 5
        if resume_data.get('education'):
            score += 3
        if resume_data.get('tech_skills') or resume_data.get('soft_skills'):
            score += 4
        
        return min(100, score)
    
    @classmethod
    def _competitive_benchmarking(cls, resume_data: Dict, job_description: str) -> Dict:
        """Benchmark against top candidates (Rezi/Kickresume style)"""
        
        # Calculate various metrics
        work_history = resume_data.get('work_history', [])
        education = resume_data.get('education', [])
        projects = resume_data.get('projects', [])
        
        metrics = {
            "years_experience": len(work_history),
            "education_level": len(education),
            "projects": len(projects),
            "skills_count": len((resume_data.get('tech_skills', '') + resume_data.get('soft_skills', '')).split(','))
        }
        
        # Industry benchmarks (simulated - in production would be from database)
        benchmarks = {
            "top_10_percent": {"years_experience": 7, "education_level": 2, "projects": 5, "skills_count": 20},
            "top_25_percent": {"years_experience": 5, "education_level": 1, "projects": 3, "skills_count": 15},
            "average": {"years_experience": 3, "education_level": 1, "projects": 2, "skills_count": 10}
        }
        
        # Compare against benchmarks
        comparison = {}
        for key in metrics:
            if metrics[key] >= benchmarks["top_10_percent"][key]:
                comparison[key] = "Top 10%"
            elif metrics[key] >= benchmarks["top_25_percent"][key]:
                comparison[key] = "Top 25%"
            elif metrics[key] >= benchmarks["average"][key]:
                comparison[key] = "Average"
            else:
                comparison[key] = "Below Average"
        
        # Overall competitive rating
        top_10_count = sum(1 for v in comparison.values() if v == "Top 10%")
        if top_10_count >= 3:
            overall_rating = "Highly Competitive"
        elif top_10_count >= 2:
            overall_rating = "Competitive"
        else:
            overall_rating = "Developing"
        
        return {
            "overall_rating": overall_rating,
            "metrics": metrics,
            "benchmarks": benchmarks,
            "comparison": comparison,
            "competitive_score": cls._calculate_competitive_score(comparison)
        }
    
    @classmethod
    def _calculate_competitive_score(cls, comparison: Dict) -> int:
        """Calculate competitive score from comparison"""
        score_map = {"Top 10%": 100, "Top 25%": 80, "Average": 60, "Below Average": 40}
        scores = [score_map.get(v, 50) for v in comparison.values()]
        return int(sum(scores) / len(scores)) if scores else 50
    
    @classmethod
    def _generate_improvements(cls, analysis: Dict) -> List[str]:
        """Generate actionable improvement suggestions"""
        improvements = []
        
        # Keyword improvements
        keyword_score = analysis["keyword_optimization"].get("score", 0)
        if keyword_score < 70:
            missing = analysis["keyword_optimization"].get("missing_critical_keywords", [])
            if missing:
                top_missing = [k["keyword"] for k in missing[:5]]
                improvements.append(f"🎯 Add these critical keywords: {', '.join(top_missing)}")
        
        # Formatting improvements
        formatting_issues = analysis["formatting_analysis"].get("issues", [])
        for issue in formatting_issues[:3]:
            improvements.append(f"📝 {issue}")
        
        # Content improvements
        content = analysis["content_strength"]
        if content.get("weak_phrases_found", 0) > 0:
            improvements.append(f"💪 Replace {content['weak_phrases_found']} weak phrases with action verbs")
        if content.get("power_verbs_used", 0) < 10:
            improvements.append("💪 Add more power verbs to strengthen impact")
        
        # Competitive improvements
        comp = analysis["competitive_benchmark"]
        if comp.get("overall_rating") != "Highly Competitive":
            improvements.append("🚀 Add more projects and achievements to become more competitive")
        
        return improvements[:7]  # Return top 7 improvements
    
    @classmethod
    def _industry_feedback(cls, resume_data: Dict, industry: str) -> List[str]:
        """Generate industry-specific feedback"""
        feedback = []
        resume_text = json.dumps(resume_data).lower()
        
        industry_keywords = cls.INDUSTRY_KEYWORDS.get(industry, [])
        if industry_keywords:
            matched = sum(1 for kw in industry_keywords if kw in resume_text)
            match_rate = (matched / len(industry_keywords)) * 100
            
            if match_rate < 40:
                feedback.append(f"⚠️ Low {industry} keyword coverage ({match_rate:.0f}%). Add industry-specific terms.")
                feedback.append(f"💡 Consider adding: {', '.join(industry_keywords[:10])}")
            elif match_rate < 70:
                feedback.append(f"✓ Moderate {industry} keyword coverage ({match_rate:.0f}%). Room for improvement.")
            else:
                feedback.append(f"✅ Excellent {industry} keyword coverage ({match_rate:.0f}%)!")
        
        return feedback
    
    @staticmethod
    def _get_keyword_recommendation(score: int, density: float) -> str:
        if score >= 80:
            return "Excellent keyword optimization! Resume is well-aligned with job requirements."
        elif score >= 60:
            return f"Good keyword coverage ({density:.1f}%). Add more job-specific keywords for better matching."
        else:
            return f"Low keyword density ({density:.1f}%). Significantly improve by adding relevant keywords from job description."
    
    @staticmethod
    def _get_formatting_recommendation(score: int) -> str:
        if score >= 90:
            return "Excellent formatting! ATS systems will parse your resume perfectly."
        elif score >= 75:
            return "Good formatting with minor issues. Address warnings to optimize."
        elif score >= 60:
            return "Fair formatting. Fix issues to improve ATS compatibility."
        else:
            return "Poor formatting. Address all issues immediately - ATS systems may reject resume."
    
    @staticmethod
    def _get_content_recommendations(power_verbs: int, weak_phrases: int) -> List[str]:
        recommendations = []
        if power_verbs < 10:
            recommendations.append("Add more action verbs (aim for 15-20 power verbs)")
        if weak_phrases > 3:
            recommendations.append(f"Remove {weak_phrases} weak phrases and replace with strong action statements")
        if power_verbs >= 15 and weak_phrases == 0:
            recommendations.append("Excellent use of powerful language!")
        return recommendations
    
    @staticmethod
    def _get_grade(score: int) -> str:
        if score >= 95: return "A+"
        elif score >= 90: return "A"
        elif score >= 85: return "A-"
        elif score >= 80: return "B+"
        elif score >= 75: return "B"
        elif score >= 70: return "B-"
        elif score >= 65: return "C+"
        elif score >= 60: return "C"
        else: return "D"
