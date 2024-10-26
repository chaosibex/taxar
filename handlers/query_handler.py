from crew_service.customer_support import assemble_classifier_crew
from crew_service.tax_explain import assemble_tax_explain_crew
from crew_service.tax_relief_recommender_estimator import assemble_tax_recommender_estimate_crew
from crew_service.charter import assemble_chart_crew
from helpers.utils import get_web_search_tools, extract_text
import streamlit as st
import yaml

def process_query(input, basic_profile):    
    crew = assemble_classifier_crew()
    classification = crew.kickoff(inputs={"query":input})
    
    
    research_tools = get_web_search_tools(st.session_state['resources'])

    if "TAX_EXPLAIN" in classification.raw:
        explain_crew = assemble_tax_explain_crew(research_tools)
        reply = explain_crew.kickoff(inputs={"query":input})
        return reply.raw, {}
    
    if "TAX_RELIEF_RECOMMENDER_EST" in classification.raw:
        recommender_crew = assemble_tax_recommender_estimate_crew(research_tools)
        reply = recommender_crew.kickoff(inputs={"query":input, "basic_profile": basic_profile})
        
        chart_crew = assemble_chart_crew()
        chart_reply = chart_crew.kickoff(inputs={"recommend": reply.raw})
        
        extract = extract_text(chart_reply.raw)
        chart_obj = yaml.safe_load(extract)
        
        chart = {}
        try:
            chart = chart_obj['pie_chart']
        except:
            chart = {}

        return reply.raw, chart

    return "Hello, thanks for your question, but we are currently unable to assist you with it. Sorry for the inconvenience. Happy to help you with other queries.", {}