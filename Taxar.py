import streamlit as st
from handlers.query_handler import process_query
from helpers.utils import check_password, escape_markdown, format_autopct, get_resources
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load import only when deployed on streamlit
if not load_dotenv('.env'):
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

APP_NAME = "Taxar"

NOTICE ="""⚠️ **IMPORTANT NOTICE**:
        
This web application is a prototype developed for **educational purposes only**.
        
The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
        
**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**
        
Always consult with qualified professionals for accurate and personalized advice."""

USAGE_GUIDE="""Hello 👋🏻, I am Taxar your personal tax assistant.

I am good at explaining personal tax reliefs, and I am able to give a rough estimation of your tax reliefs.

You can fill in your profile over at the side bar 👈🏻 so that I can know you better!

And don't worry, I do not save any of your data. Just hit the refresh button ↪️ and I will forget about you 😬
"""

def pie_chart_colours():
    return ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#FF69B4',
            '#CD5C5C', '#8A2BE2', '#00CED1', '#DC143C', '#FFDAB9', '#7FFF00', 
            '#32CD32', '#FF4500', '#800080', '#00FA9A', '#FF6347', '#4682B4', 
            '#D2B48C', '#DAA520']

def build_input_fields():
    return [
        {"label": "Age", "type": "number_input", "step": 1, "key": "age"},
        {"label": "Sex", "type": "selectbox", "options": ("Male", "Female"), "placeholder": "Choose an option", "key": "sex"},
        {"label": "Annual Gross Income", "type": "text_input", "key": "annual_income"},
        {"label": "Annual CPF Top up", "type": "text_input", "key": "annual_cpf_top_up"},
        {"label": "Annual Life Insurance premium", "type": "text_input", "key": "annual_life_insurance_premium"},
        {"label": "Marital Status", "type": "selectbox", "options": ("Single", "Married", "Widowed", "Separated", "Divorced"), "placeholder": "Choose an option", "key": "marital_status"},
        {"label": "Number of children", "type": "number_input", "step": 1, "key": "child_num"},
        {"label": "Child(ren) Age Range", "type": "text_input", "key": "children_age_range"},
        {"label": "Child(ren) taken care by grandparents", "type": "selectbox", "options": ("Yes", "No"), "placeholder": "Choose an option", "key": "grandparent_take_care_of_children"},
        {"label": "Employment Status", "type": "selectbox", "options": ("Self-employed", "Unemployed", "Part-time", "Internship", "Full-time", "National Service Full time"), "placeholder": "Choose an option", "key": "employment_status"},
        {"label": "National Service Status", "type": "multiselect", "options": ("National Service Full Time", "NSMan", "Did not serve", "NSMan Spouse", "NSMan Parents"), "placeholder": "Choose options that apply", "key": "national_service"},
        {"label": "Other Remarks", "type": "text_input", "key": "other_remarks"},
    ]

def get_basic_profile():
    input_fields = build_input_fields()
    return {field["key"]: st.session_state.get(field["key"]) for field in input_fields}

def send_message():
    prompt = st.session_state.user_prompt
    basic_profile = get_basic_profile()
    st.session_state["messages"].append({"role": "user", "content": prompt})

    try:
        bot_response, chart = process_query(prompt, basic_profile)
    except:
        err_response = "Something went wrong, sorry for the inconvenience."
        st.session_state["messages"].append({"role": "bot", "content": err_response})
        return

    st.session_state["messages"].append({"role": "bot", "content": bot_response, "chart": chart})


def layout():
    st.set_page_config(
        layout="centered",
        page_title=APP_NAME
    )
    
    st.title(APP_NAME)
    st.session_state['resources'] = get_resources()

    if not check_password():  
        st.stop()

    st.sidebar.header("Personal Profile")

    with st.sidebar:
        is_resident = st.selectbox(
            "Are you a Tax Resident?",
            ("Yes", "No"),
            placeholder="Choose an option",
            index=None,
            key="tax_resident"
        )
        
        if is_resident == "Yes":
            for field in build_input_fields():
                if field["type"] == "text_input":
                    st.text_input(field["label"], key=field["key"])
                elif field["type"] == "number_input":
                    st.number_input(field["label"], step=field.get("step", 1), key=field["key"])
                elif field["type"] == "selectbox":
                    st.selectbox(field["label"], field["options"], key=field["key"], placeholder=field.get("placeholder", ""), index=None)
                elif field["type"] == "multiselect":
                    st.multiselect(field["label"], field["options"], key=field["key"], placeholder=field.get("placeholder", ""))
        else:
            st.write("As a non-tax resident in Singapore, you are not eligible to claim personal income tax reliefs.")

    if "messages" not in st.session_state:

        st.session_state["messages"] = []
        st.session_state["messages"].append({"role": "bot", "content": NOTICE})
        st.session_state["messages"].append({"role": "bot", "content": USAGE_GUIDE})

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(escape_markdown(message["content"]))
            if message.get('chart'):
                chart_data = message['chart']
                amounts = list(map(int, chart_data['tax_relief_amount']))
                plt.pie(amounts, labels=chart_data['tax_relief_name'], colors=pie_chart_colours(), autopct=lambda pct: format_autopct(pct, amounts))
                st.pyplot (plt)

    st.chat_input(placeholder="Enter your message here...", on_submit=send_message, key="user_prompt")

if __name__ == "__main__":
    layout()