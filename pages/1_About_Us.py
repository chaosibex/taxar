import streamlit as st

st.set_page_config(page_title="About Us", page_icon="ℹ️")


st.sidebar.header("About Us")

about_us = """
# About Us
## Project Scope
- Personal Tax Reliefs

## Objectives
- 

## Data Sources

## Features
- Explain Personal Tax Relief
- Provide Estimates on Relief and Tax Payable based on input profile
"""

st.markdown(about_us)
