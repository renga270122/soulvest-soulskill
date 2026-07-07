#!/usr/bin/env python3
"""
Verify SoulSkill setup and functionality
"""
import os
import sys

def check_api_key():
    """Check if Google API key is configured"""
    print("🔍 Checking API Key Configuration...")
    
    # Check secrets.toml
    secrets_path = ".streamlit/secrets.toml"
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                print("  ✅ API key found in .streamlit/secrets.toml")
                return True
            else:
                print("  ❌ API key NOT found in .streamlit/secrets.toml")
    else:
        print("  ⚠️  .streamlit/secrets.toml not found")
    
    # Check environment variable
    if os.getenv('GOOGLE_API_KEY'):
        print("  ✅ API key found in environment variables")
        return True
    else:
        print("  ❌ API key NOT found in environment variables")
    
    return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking Dependencies...")
    
    required = [
        'streamlit',
        'google.generativeai',
        'sklearn',
        'numpy',
        'requests'
    ]
    
    all_ok = True
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if all required files exist"""
    print("\n📁 Checking Required Files...")
    
    required_files = [
        'app.py',
        'ai_assistant.py',
        'ai_advanced.py',
        'resume_generator.py',
        'requirements.txt',
        'template_config.py',
        'industry_config.py',
        'stream_config.py',
        'education_config.py'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            all_ok = False
    
    return all_ok

def check_ai_functionality():
    """Test if AI features work"""
    print("\n🤖 Checking AI Functionality...")
    
    try:
        from ai_assistant import AIResumeAssistant
        
        # Check if API key exists
        api_key = None
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
                api_key = st.secrets['GOOGLE_API_KEY']
        except:
            pass
        
        if api_key is None:
            api_key = os.getenv('GOOGLE_API_KEY')
        
        assistant = AIResumeAssistant(api_key)
        
        if assistant.enabled:
            print("  ✅ AI Assistant initialized successfully")
            print(f"  ✅ Using model: {assistant.model_name}")
            return True
        else:
            print("  ❌ AI Assistant disabled (check API key)")
            return False
            
    except Exception as e:
        print(f"  ❌ Error initializing AI: {str(e)}")
        return False

def check_autosave():
    """Check if autosave file exists"""
    print("\n💾 Checking Auto-save...")
    
    if os.path.exists("soulskill_autosave.json"):
        import json
        with open("soulskill_autosave.json", 'r') as f:
            data = json.load(f)
            print(f"  ✅ Auto-save file found")
            print(f"  📅 Last saved: {data.get('last_saved', 'Unknown')}")
            return True
    else:
        print("  ℹ️  No saved progress found (this is normal for first run)")
        return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("🔧 SOULSKILL SETUP VERIFICATION")
    print("=" * 60)
    
    checks = {
        "Files": check_files(),
        "Dependencies": check_dependencies(),
        "API Key": check_api_key(),
        "AI Functionality": check_ai_functionality(),
        "Auto-save": check_autosave()
    }
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All checks passed! Your SoulSkill app is ready.")
        print("\n🚀 To start the app, run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n📝 Common fixes:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Add API key to .streamlit/secrets.toml")
        print("   • Make sure all required files exist")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
