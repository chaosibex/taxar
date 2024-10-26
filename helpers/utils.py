import streamlit as st
import hmac
from crewai_tools import WebsiteSearchTool
import re

def check_password():  
    """Returns `True` if the user had the correct password."""
    def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):  
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  # Don't store the password.  
        else:  
            st.session_state["password_correct"] = False  
    # Return True if the passward is validated.  
    if st.session_state.get("password_correct", False):  
        return True  
    # Show input for password.  
    st.text_input(  
        "Password", type="password", on_change=password_entered, key="password"  
    )  
    if "password_correct" in st.session_state:  
        st.error("😕 Password incorrect")  
    return False

def footer():
    footer_html = """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            padding: 5px;
            background-color: #000;
            color: white;
            text-align: center;
            font-size:
        }
        p {
            font-size: 12px;
        }
        </style>
        <div class='footer'>
            <p>IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only.</p>
            <p>The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.</p>
            <p>Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.</p>
            <p>Always consult with qualified professionals for accurate and personalized advice.</p>
        </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)
    
    
def get_web_search_tools(urls):
    tools = []
    for url in urls:
        tools.append(WebsiteSearchTool(url))
    print (tools)
    return tools

def get_resources():
    with open('./resources/resources.txt', 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def escape_markdown(text):
    # List of markdown special characters to escape
    markdown_special_chars = r"$"

    # Escape each special character by preceding it with a backslash
    escaped_text = re.sub(f"([{re.escape(markdown_special_chars)}])", r"\\\1", text)
    
    return escaped_text

def format_autopct(pct, all_values):
    absolute = int(pct / 100. * sum(all_values))
    return f'${absolute}\n({pct:.1f}%)'

def extract_text(text):
    # Regular expression to match text between ```json and ```
    # pattern = r'```json(.*?)```'
    pattern = r'```yaml(.*?)```'
    match = re.search(pattern, text, re.DOTALL)  # re.DOTALL handles multiline text if needed
    if match:
        extracted_text = match.group(1).strip()  # Extract and remove any surrounding whitespace
        return extracted_text  # Return the extracted text
    return None  # Return None if no match is found
