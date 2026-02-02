# Automated Testing for SoulSkill AI Resume Builder

## 🎯 What We Created

We've set up **3 layers of automated testing**:

### 1. **Unit Tests** (`test_app.py`)
- Tests individual components and functions
- Verifies templates load correctly
- Checks data structures
- Fast execution (~5 seconds)

### 2. **End-to-End Tests** (`test_e2e.py`)  
- Tests the live app like a real user
- Uses Playwright to control a browser
- Clicks buttons, fills forms, verifies outputs
- Tests mobile responsiveness

### 3. **CI/CD Pipeline** (`.github/workflows/test.yml`)
- Runs automatically on every code push
- Daily health checks of live app
- Performance audits with Lighthouse
- Sends notifications if something breaks

---

## 🚀 How to Run Tests

### Option 1: Run All Tests Locally
```bash
# Install test dependencies
pip install pytest playwright pytest-cov

# Install browser for E2E tests
playwright install chromium

# Run unit tests
pytest test_app.py -v

# Run E2E tests (headless)
pytest test_e2e.py -v

# Run E2E tests (see browser)
pytest test_e2e.py -v --headed --slowmo=1000

# Run with coverage report
pytest test_app.py --cov=. --cov-report=html
```

### Option 2: GitHub Actions (Automatic)
Tests run automatically when you push to GitHub:
- ✅ Every push to `main` branch
- ✅ Every pull request
- ✅ Daily at 2 AM UTC
- ✅ Manual trigger from Actions tab

View results: https://github.com/renga270122/soulvest-soulskill/actions

---

## 📊 What Gets Tested

### ✅ Template System
- All 29 templates load without errors
- Templates have required fields (font, color, ATS score)
- Country-specific features (photo guidance)

### ✅ Resume Builder
- Form inputs render correctly
- Data validation works
- Auto-save functionality

### ✅ Premium Features
- Job Description Matcher visible
- ATS Compatibility Checker works
- Skill Gap Analysis functional

### ✅ Export Functionality
- PDF download available
- All 6 formats supported (HTML, PDF, DOCX, TXT, JSON, MD)

### ✅ Mobile Experience
- Works on phone screens (375px)
- Touch targets are 44px minimum
- No horizontal scrolling

### ✅ Performance
- Page loads in <10 seconds
- No JavaScript console errors
- Lighthouse performance score

### ✅ Live App Health
- App is accessible (200 status)
- Response time <15 seconds

---

## 🔧 Customizing Tests

### Add a New Test
Edit `test_app.py` or `test_e2e.py`:

```python
def test_my_feature(self, page: Page):
    """Test my new feature"""
    page.goto(APP_URL)
    page.wait_for_load_state("networkidle")
    
    # Your test code here
    assert True
```

### Run Specific Tests
```bash
# Run only unit tests
pytest test_app.py

# Run only E2E tests
pytest test_e2e.py

# Run specific test class
pytest test_app.py::TestTemplateConfig -v

# Run specific test function
pytest test_e2e.py::TestHomePage::test_page_loads -v
```

### Skip Slow Tests
```bash
# Skip integration tests
pytest -m "not integration"
```

---

## 📈 Viewing Test Results

### Local Results
After running tests:
```bash
# Open HTML coverage report
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### GitHub Actions Results
1. Go to https://github.com/renga270122/soulvest-soulskill/actions
2. Click on latest workflow run
3. View test results, screenshots, coverage

### Lighthouse Reports
Performance audit results appear in Actions artifacts:
- Performance score
- Accessibility score
- Best practices score
- SEO score

---

## 🐛 Debugging Failed Tests

### Test Failed Locally
```bash
# Run with more verbose output
pytest test_app.py -vv

# Run with debugger
pytest test_app.py --pdb

# Show print statements
pytest test_app.py -s
```

### Test Failed in GitHub Actions
1. Go to Actions tab
2. Click failed workflow
3. Expand failed job
4. Review error logs
5. Download artifacts (screenshots)

### Common Issues
- **Import errors**: Make sure dependencies are installed
- **Timeout errors**: Increase `time.sleep()` values in E2E tests
- **Element not found**: Streamlit structure may have changed, update selectors
- **Browser not found**: Run `playwright install chromium`

---

## 🎯 Next Steps

### Immediate
1. ✅ Push test files to GitHub
2. ✅ Verify GitHub Actions runs successfully
3. ✅ Check test coverage report

### Short-term
- Add tests for AI features (Job Matcher, Skill Gap)
- Test all 29 templates individually
- Add screenshot comparison tests
- Test PDF export quality

### Long-term
- Set up Codecov for coverage tracking
- Add visual regression testing
- Create load testing (simulate 100 users)
- Set up error monitoring (Sentry)

---

## 📚 Resources

- **Pytest Docs**: https://docs.pytest.org/
- **Playwright Docs**: https://playwright.dev/python/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Lighthouse CI**: https://github.com/GoogleChrome/lighthouse-ci

---

## 💡 Pro Tips

1. **Run tests before pushing**: `pytest -v`
2. **Write tests for bugs**: Convert each bug into a test case
3. **Keep tests fast**: Unit tests should run in seconds
4. **Use fixtures**: Avoid code duplication in tests
5. **Mock external APIs**: Don't call real Gemini API in tests
6. **Test edge cases**: Empty inputs, very long text, special characters

---

## ✅ Test Coverage Goals

- **Unit Tests**: 80%+ code coverage
- **E2E Tests**: Cover all user workflows
- **CI/CD**: 100% of pushes should be tested
- **Performance**: <10s page load, >90 Lighthouse score

---

Ready to test! 🚀 All tests will run automatically when you push to GitHub.
