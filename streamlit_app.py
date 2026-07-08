# SoulSkill AI - Production Entry Point
# This file is used by Streamlit Cloud deployment

import os
import sys
import traceback

# Ensure the app can find all modules
sys.path.insert(0, os.path.dirname(__file__))


def _render_bootstrap_error(exc: Exception):
	"""Render a graceful error screen instead of crashing the Streamlit process."""
	import streamlit as st

	st.set_page_config(
		page_title="SoulSkill - Startup Recovery",
		page_icon="⚠️",
		layout="centered",
	)

	st.error("SoulSkill encountered a startup issue and entered recovery mode.")
	st.info(
		"Please refresh once. If this persists, check deployment logs and environment variables."
	)

	with st.expander("Technical details", expanded=False):
		st.code("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))


try:
	# Import and run the enhanced app.
	# app_enhanced executes the Streamlit UI at module load time.
	from app_enhanced import *  # noqa: F401,F403
except Exception as bootstrap_error:
	_render_bootstrap_error(bootstrap_error)
