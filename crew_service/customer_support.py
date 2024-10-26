from crewai import Agent, Task, Crew

def assemble_classifier_crew():
    agent_customer_support_classifier = Agent(
        role="Customer Support (Query Classifier)",
        goal="To accurately classify user queries based on the context.",
        cache=True,
        backstory="""As an experienced Customer Support Specialist handling tax-related matters, you excel at quickly analyzing user queries and identifying subtle nuances in context to classify them accurately. By ensuring precise query classification, you help direct inquiries to the appropriate departments or personnel, facilitating timely and effective responses."""
    )
    
    task_classify = Task(
        description="""\
        Task Objective: The goal of this task is to accurately and efficiently classify user queries into their respective categories.
        
        Current Classification Categories:
            - Explaining Tax Policy: Provide users with concise and accurate explanations and guidance of the most relevant and up-to-date tax policies, helping them navigate and understand complex tax-related topics.
            - Tax Relief Recommendation and Estimation: Based on the user's profile, recommend potential tax reliefs they may be eligible for and estimate their total relief amount.
        
        Task Guidelines:
            1. Analyze the user query: {query}
            2. Accurately classify the query into one of the following categories: Explaining Tax Policy or Tax Relief Recommendation and Estimation.
            3. If the query is not tax-related, respond with NOT_APPLICABLE.
        """,

        expected_output="""\
            Return Format: Return only the classification key. The classification keys are as follows:
            - `TAX_EXPLAIN`: For queries related to explaining tax policies.
            - `TAX_RELIEF_RECOMMENDER_EST`: For tax relief recommendations and estimations.
            - `NOT_APPLICABLE`: For non-tax-related queries.
            """,
        agent=agent_customer_support_classifier
    )
    
    return Crew(
        agents=[agent_customer_support_classifier],
        tasks=[task_classify],
        verbose=True,
        memory=True,
        cache=True,
    )