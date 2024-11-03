import streamlit as st
from helpers.utils import check_password

st.set_page_config(page_title="Methodology", page_icon="💡")


if not check_password():  
    st.stop()

st.markdown("""
## RAG Architecture
Utilised `crewai_tools` to create tools to allow AI Agents to conduct semantic searches within the specified content of websites.

Below is the overview of how it works:

1. Initialize Resources: Load essential resources at application startup.
2. Process User Query: Accept and process the user's query.
3. Generate Research Tools: Use crewai_tools to create tools that perform semantic searches within designated URLs.""")


st.markdown("""
## Usecase Flowchart
A classifier agent operates as the first layer to direct incoming queries to the appropriate agents or "crew"", 
enabling the integration of both use cases into a single chatbot.
""")


st.image("resources/img/usecase_flowchart.png")

st.markdown("""
### Agents Roles and Responsibilities

#### Classifier Agent
This agent categorizes each query into one of three categories:
1. Explaining Tax Policy: Provides users with clear, up-to-date explanations of tax policies to support their understanding of complex tax topics.
2. Tax Relief Recommendation and Estimation: Reviews the user's profile to suggest potential tax reliefs and estimate the total relief amount.
3. Not Applicable: If the query is unrelated to tax, it is categorized as “Not Applicable.”

#### "Explain" Crew
The "crew" consists of a Recommender Manager, two Research Assistants, and a Writer. The Recommender Manager receives each query and delegates tasks to the most appropriate agent based on the query type. For accurate results, the Recommender Manager is guided to use the research tools exclusively.

#### Recommender Agent
This agent analyzes the user's profile to recommend and estimate tax reliefs. It generates a report in a specified format for consistency and clarity.

#### Chart Agent
The Chart Agent uses the Recommender Agent's output to extract the recommended reliefs, converting them into a YAML format. This structured data is then used to create a pie chart with Matplotlib, visually displaying the breakdown of estimated reliefs.
""")

st.markdown("""
## Prompting techniques
### Classifier Agent
- Roleplay Mode: Role play as an experienced Customer Support

### "Explain" Crew
- Roleplay Mode: Role play as Manager, Researcher, Writer
- Step by Step: Task is broken down into steps

### Recommender Agent
- Roleplay Mode: Role play as an experienced Tax Consultant
- One shot learning: Given an example of the format of reply to return. Given an example of what not to reply
- Step by Step: Task is broken down into steps, and prompted to double check on it given matches the user profile

### Chart Agent
- Roleplay Mode: Role play as an experienced Data Anaylst
- One shot learning: Given an example of the format of reply to return.
- Step by Step: Task is broken down into steps
- Task specific: Tasked to extract into yaml format
""")

st.markdown("""
## LLM Parameters
Set temperature to 0.5 to balance between coherence and diversity to make the reply is more natural and engaging.
""")

st.markdown("""
## Obstacles
1. **Hallucination**: The model may generate incorrect information or fabricate details that don't exist, leading to unreliable outputs.
2. **Lack of Conversation Memory**: Each prompt is processed independently, with no recall of previous interactions, resulting in a loss of conversational continuity and context.
""")

st.markdown("""
## Potential Improvements
1. Hallucination
    
    a. **Introduce Step-by-Step Prompts**: Break down complex queries into sequential steps, guiding the AI to reason and respond methodically.
    
    b. **Error-Checking Layer**: Implement an additional AI agent layer dedicated to verifying the response for inaccuracies or inconsistencies.
    
    c. **Tuning Parameters**: Consider setting lower temperature and top-p to have a more deterministic output.
2. Memory
    
    a. **Conversation Storage in Vector Store**: Save chat conversations in a vector store to retain context across sessions and retrieve past interactions as needed.
    
    b. **Summary Cache**: Use an agent to generate and save summarized versions of conversations in a cache or session state. The prompt can be crafted to selectively extract key points for summarization.
""")
