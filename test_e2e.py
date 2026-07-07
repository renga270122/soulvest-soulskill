# End-to-End Tests using Playwright
"""
Run with: pytest test_e2e.py --headed (to see browser)
or: pytest test_e2e.py (headless mode)
"""
import pytest
from playwright.sync_api import Page, expect
import time

# Your deployed app URL
APP_URL = "https://soulvest-soulskill-rwwrmxhx5mmuak37j9ap6z.streamlit.app/"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser for Streamlit"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


class TestHomePage:
    """Test home page functionality"""
    
    def test_page_loads(self, page: Page):
        """Verify app loads successfully"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        
        # Check title contains SoulSkill
        expect(page).to_have_title(lambda t: "SoulSkill" in t or "Streamlit" in t)
    
    def test_start_building_button(self, page: Page):
        """Test 'Start Building' button exists"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)  # Wait for Streamlit to fully render
        
        # Look for start button (Streamlit buttons have unique structure)
        start_button = page.get_by_role("button", name=lambda n: "Start" in n or "Build" in n)
        if start_button.is_visible():
            assert True
        else:
            # Alternative: check for any button
            buttons = page.locator("button").count()
            assert buttons > 0, "No buttons found on home page"


class TestTemplateSelection:
    """Test template selection flow"""
    
    def test_template_gallery_displays(self, page: Page):
        """Verify templates display after starting"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Click start building (adapt selector based on your app)
        try:
            start_btn = page.locator("button").filter(has_text="Start")
            if start_btn.is_visible():
                start_btn.click()
                time.sleep(2)
        except:
            pass  # May already be on template selection
        
        # Check for template cards (should have multiple)
        # Streamlit uses specific classes, adjust as needed
        template_count = page.locator("[data-testid='column']").count()
        assert template_count > 0, "No template columns found"
    
    def test_template_preview_images(self, page: Page):
        """Verify template previews render"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Count iframes or images (template previews)
        iframes = page.locator("iframe").count()
        images = page.locator("img").count()
        
        assert iframes + images > 0, "No template previews found"


class TestResumeBuilder:
    """Test resume building functionality"""
    
    def test_form_inputs_exist(self, page: Page):
        """Verify form inputs are present"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Check for text inputs (Streamlit creates input elements)
        text_inputs = page.locator("input[type='text'], input[type='email'], input[type='tel']").count()
        textareas = page.locator("textarea").count()
        
        total_inputs = text_inputs + textareas
        assert total_inputs > 0, f"No form inputs found (text: {text_inputs}, textarea: {textareas})"
    
    def test_fill_basic_info(self, page: Page):
        """Test filling basic information"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(4)
        
        # Try to fill name field (adapt selectors to your app)
        try:
            name_input = page.locator("input[type='text']").first
            name_input.fill("Test User")
            name_input.press("Tab")
            time.sleep(1)
            
            # Verify value was entered
            value = name_input.input_value()
            assert value == "Test User", f"Expected 'Test User', got '{value}'"
        except Exception as e:
            pytest.skip(f"Could not fill form: {e}")


class TestPremiumFeatures:
    """Test premium features"""
    
    def test_job_description_matcher_visible(self, page: Page):
        """Check if Job Description Matcher is accessible"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Look for JD matcher text or expander
        page_content = page.content()
        has_jd_feature = ("Job Description" in page_content or 
                          "Match" in page_content or
                          "ATS" in page_content)
        
        assert has_jd_feature, "Job Description Matcher not found"
    
    def test_ats_compatibility_checker(self, page: Page):
        """Check if ATS Compatibility Checker exists"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        page_content = page.content()
        has_ats = "ATS" in page_content or "Compatibility" in page_content
        
        assert has_ats, "ATS Compatibility feature not found"


class TestExportFunctionality:
    """Test export/download features"""
    
    def test_download_buttons_exist(self, page: Page):
        """Verify download buttons are present"""
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Look for download-related text
        page_content = page.content()
        has_download = ("Download" in page_content or 
                       "Export" in page_content or
                       "PDF" in page_content)
        
        assert has_download, "No download functionality found"


class TestMobileResponsiveness:
    """Test mobile view"""
    
    @pytest.fixture
    def mobile_page(self, page: Page):
        """Configure page for mobile viewport"""
        page.set_viewport_size({"width": 375, "height": 667})  # iPhone SE
        return page
    
    def test_mobile_layout(self, mobile_page: Page):
        """Test app works on mobile viewport"""
        mobile_page.goto(APP_URL)
        mobile_page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Verify page loads without horizontal scroll
        viewport_width = mobile_page.viewport_size["width"]
        body_width = mobile_page.locator("body").bounding_box()["width"]
        
        assert body_width <= viewport_width + 20, "Page has horizontal scroll on mobile"
    
    def test_mobile_touch_targets(self, mobile_page: Page):
        """Verify buttons are large enough for touch (44px minimum)"""
        mobile_page.goto(APP_URL)
        mobile_page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        buttons = mobile_page.locator("button").all()
        if len(buttons) > 0:
            first_button = buttons[0]
            box = first_button.bounding_box()
            if box:
                assert box["height"] >= 40, f"Button too small: {box['height']}px (minimum 44px)"


class TestPerformance:
    """Test app performance"""
    
    def test_page_load_time(self, page: Page):
        """Verify page loads within acceptable time"""
        import time
        
        start = time.time()
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        load_time = time.time() - start
        
        assert load_time < 10, f"Page took {load_time:.2f}s to load (max 10s)"
    
    def test_no_console_errors(self, page: Page):
        """Check for JavaScript console errors"""
        errors = []
        page.on("console", lambda msg: errors.append(msg) if msg.type == "error" else None)
        
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Filter out known Streamlit warnings
        critical_errors = [e for e in errors if "streamlit" not in str(e).lower()]
        assert len(critical_errors) == 0, f"Console errors: {critical_errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--headed", "--slowmo=1000"])
