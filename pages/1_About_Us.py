import streamlit as st
from helpers.utils import check_password, get_resources

st.set_page_config(page_title="About Us", page_icon="ℹ️")

if not check_password():  
    st.stop()

about_us_p1 = """
# About Us
## Project Scope
The scope of this project ("Taxar") encompasses the development of an AI-driven solution to enhance users' understanding of Singapore tax policies and support personalized tax decision-making.
We aim to help users navigate complex tax scenarios by:
- automating responses to common individual tax reliefs questions,
- offer tailored estimations and recommendations


## Objectives
- To provide automated responses to user queries related to Singapore tax policies.
- To develop a recommendation engine that estimate tax based on the general user profile.
"""

about_us_p2 = """
## Data Sources
"""

about_us_p3 = """
## Features
### Usecase 1
- Explain Personal Tax Reliefs simply
- Explain Tax concepts and provide simple guides

### Usecase 2
- Offer estimates for relief and tax liabilities based on the user's input profile.
- Present a pie chart to visually illustrate the breakdown of estimated reliefs, where applicable.
"""

st.markdown(about_us_p1)

resources = "\n".join([f"- {item}" for item in get_resources()])

st.markdown(about_us_p2)

with st.expander("IRAS (Inland Revenue Authority of Singapore) websites"):
    st.markdown(resources)

st.markdown(about_us_p3)
