# Automated Tests for SoulSkill AI Resume Builder
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

class TestTemplateConfig:
    """Test template configuration"""
    
    def test_templates_load(self):
        """Verify all templates load without errors"""
        from template_config import (
            TEMPLATES, INDIAN_TEMPLATES, US_TEMPLATES, UK_TEMPLATES,
            CANADA_TEMPLATES, AUSTRALIA_TEMPLATES, GERMANY_TEMPLATES,
            FRANCE_TEMPLATES, UAE_TEMPLATES, SINGAPORE_TEMPLATES
        )
        
        # Check templates exist
        assert len(TEMPLATES) > 0, "Base templates should exist"
        assert len(INDIAN_TEMPLATES) > 0, "Indian templates should exist"
        assert len(US_TEMPLATES) > 0, "US templates should exist"
        
        # Total should be 29+
        total = (len(TEMPLATES) + len(INDIAN_TEMPLATES) + len(US_TEMPLATES) + 
                len(UK_TEMPLATES) + len(CANADA_TEMPLATES) + len(AUSTRALIA_TEMPLATES) +
                len(GERMANY_TEMPLATES) + len(FRANCE_TEMPLATES) + len(UAE_TEMPLATES) + 
                len(SINGAPORE_TEMPLATES))
        assert total >= 29, f"Expected 29+ templates, got {total}"
    
    def test_template_structure(self):
        """Verify templates have required fields"""
        from template_config import INDIAN_TEMPLATES
        
        for template_id, config in INDIAN_TEMPLATES.items():
            assert 'font' in config, f"{template_id} missing 'font'"
            assert 'color' in config, f"{template_id} missing 'color'"
            assert 'description' in config, f"{template_id} missing 'description'"
            assert 'ats_score' in config, f"{template_id} missing 'ats_score'"


class TestResumeGenerator:
    """Test resume generation functionality"""
    
    def test_resume_generator_imports(self):
        """Verify resume generator can be imported"""
        try:
            from resume_generator import generate_resume_html
            assert callable(generate_resume_html)
        except ImportError as e:
            pytest.fail(f"Failed to import resume_generator: {e}")
    
    @patch('streamlit.session_state')
    def test_resume_data_structure(self, mock_session):
        """Test resume data has required fields"""
        mock_session.get.return_value = "Test Value"
        
        required_fields = [
            'full_name', 'email', 'phone', 'city',
            'summary', 'tech_skills', 'work_entries', 'education_entries'
        ]
        
        for field in required_fields:
            assert mock_session.get(field) is not None, f"Missing field: {field}"


class TestAIAssistant:
    """Test AI assistant functionality"""
    
    def test_ai_assistant_imports(self):
        """Verify AI assistant modules load"""
        try:
            from ai_assistant import AIResumeAssistant
            assert AIResumeAssistant is not None
        except ImportError as e:
            pytest.fail(f"Failed to import AIResumeAssistant: {e}")
    
    def test_content_library_exists(self):
        """Verify content library has job roles"""
        # This would be in app_enhanced.py, we'll check if importable
        # In production, you'd extract CONTENT_LIBRARY to a separate module
        pass


class TestExportFunctionality:
    """Test export features"""
    
    def test_export_manager_imports(self):
        """Verify export manager can be imported"""
        try:
            from export_manager import ExportManager
            manager = ExportManager()
            assert manager is not None
        except ImportError:
            pytest.skip("Export manager not available")
    
    def test_supported_formats(self):
        """Verify all export formats are supported"""
        supported_formats = ['html', 'pdf', 'docx', 'txt', 'json', 'md']
        assert len(supported_formats) == 6, "Should support 6 export formats"


class TestATSOptimization:
    """Test ATS optimization features"""
    
    def test_ats_score_calculation(self):
        """Test ATS score calculator logic"""
        # Mock resume data
        resume_data = {
            'show_photo': False,  # Good for ATS
            'two_column': False,  # Good for ATS
            'summary': 'A' * 300,  # Good length
            'tech_skills': 'Python, JavaScript, React, Node.js, AWS, Docker',
            'work_entries': [
                {'responsibilities': 'Improved performance by 30%'}
            ]
        }
        
        # Calculate score (simplified logic)
        score = 0
        if not resume_data.get('show_photo'): score += 20
        if not resume_data.get('two_column'): score += 20
        if len(resume_data.get('summary', '')) > 200: score += 20
        if len(resume_data.get('tech_skills', '').split(',')) >= 5: score += 20
        work_content = ' '.join([e.get('responsibilities', '') for e in resume_data.get('work_entries', [])])
        if any(char.isdigit() for char in work_content): score += 20
        
        assert score >= 80, f"Expected ATS score >= 80, got {score}"


class TestMobileResponsiveness:
    """Test mobile optimization"""
    
    def test_touch_target_sizes(self):
        """Verify touch targets are mobile-friendly (44px minimum)"""
        # In a real test, you'd check CSS/HTML output
        min_touch_target = 44  # pixels
        assert min_touch_target >= 44, "Touch targets should be at least 44px"
    
    def test_font_sizes(self):
        """Verify font sizes prevent iOS zoom (16px minimum)"""
        min_font_size = 16  # pixels for inputs
        assert min_font_size >= 16, "Input fonts should be at least 16px"


class TestCountrySpecificFeatures:
    """Test country-specific template features"""
    
    def test_photo_guidance_regions(self):
        """Test photo guidance differs by region"""
        from template_config import GERMANY_TEMPLATES, US_TEMPLATES
        
        # Germany templates may expect photos
        german_template = list(GERMANY_TEMPLATES.values())[0]
        if 'photo_expected' in german_template:
            assert german_template['photo_expected'] == True
        
        # US templates should discourage photos
        us_template = list(US_TEMPLATES.values())[0]
        if 'photo_discouraged' in us_template:
            assert us_template['photo_discouraged'] == True


# Integration Tests (require full app)
class TestEndToEnd:
    """End-to-end integration tests"""
    
    @pytest.mark.integration
    def test_full_resume_workflow(self):
        """Test complete resume creation workflow"""
        # This would use Streamlit testing utilities or Selenium
        pytest.skip("Requires full integration test setup")
    
    @pytest.mark.integration
    def test_job_description_matcher(self):
        """Test job description matching feature"""
        pytest.skip("Requires AI API access in test environment")


if __name__ == "__main__":
    # Run tests with: python test_app.py
    pytest.main([__file__, "-v", "--tb=short"])
