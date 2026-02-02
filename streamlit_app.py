# SoulSkill AI - Production Entry Point
# This file is used by Streamlit Cloud deployment

import sys
import os

# Ensure the app can find all modules
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the enhanced app
from app_enhanced import *

# The app will automatically run when this file is executed by Streamlit
