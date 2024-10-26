from crewai import Agent, Task, Crew

def assemble_tax_recommender_estimate_crew(research_tools):
    agent_personal_tax_consultant = Agent(
        role="Personal Tax Consultant",
        goal="Provide personalized tax recommendations and accurate estimations by analyzing the user's profile, suggesting applicable reliefs, and offering alternative scenarios to optimize their tax liabilities.",
        backstory="""You are an expert personal tax consultant responsible for recommending personalized tax reliefs and estimating tax liabilities based on the user's basic profiling information.
        Your goal is to guide users toward the most tax-efficient options, taking into account their personal circumstances. 
        When users provide incomplete information, you will suggest potential tax reliefs, deductions, or exemptions that may apply.
        You should explain different scenarios where applicable, such as how changes in income, family status, or other factors may impact tax liabilities.
        """,
        allow_delegation=False,
        tools=research_tools,
    )
    

    task_consult = Task(
        description="""\
            1. Analyse user query {query}
            2. Analyse user basic profile {basic_profile}
            3. Strictly use only the tools provided to gather information.
            4. Estimate the tax reliefs and tax liabilities of the user by carefully going through all the resources in the tools to ensure all tax relief that matches the user profile is recommended.
            5. Be sure to check that the recommended tax reliefs fits all criteria of the user profile. e.g. Working Mother Child Relief (WMCR) cannot be claimed by a Male.
            6. For tax relief that cannot be infered from the user basic profile, recommend it under the Recommendation and Optimization section.
            7. Give a detailed breakdown of the tax reliefs and the amount of the tax reliefs.
            8. Provide the URL reference you got your information from""",

        expected_output="""\
            1. Provide a response to the user's inquiry with the below format. Note that there can be more than 3 Tax Reliefs.
            2. Give an estimation of the tax relief and tax payable based on the given information.
            3. Detailed breakdown of tax payable showing the calculation steps.
            4. Provide recommendations and optimisation under then Recommendations section.
            5. If no information is found through available research tools, reply that the query cannot be answered due to a lack of relevant information. In such cases, you do not need to follow the reply format.
            
            # Tax Relief and Payable Estimate
            Total Tax Relief: $<Total Tax Relief Amount>
            Total Taxable Income: $<Total Tax Income>
            Total Tax Payable: $<Total Payable Tax>
            
            # Tax Relief Breakdown
            | Tax Relief     | Amount               | 
            | <Tax Relief 1> | <Tax Relief 1 Amount |
            | <Tax Relief 2> | <Tax Relief 2 Amount |
            | <Tax Relief 3> | <Tax Relief 3 Amount |
            
            ## Tax Relief 1
            <Tax Relief 1 breakdown Details>
            Reference: <URL>
            
            ## Tax Relief 2
            <Tax Relief 2 breakdown Details>
            Reference: <URL>
            
            ## Tax Relief 3
            <Tax Relief 3 breakdown Details>
            Reference: <URL>
            
            # Total Tax Payable Breakdown
            <Total Tax Payable breakdown details>
            
            # Recommendation and Optimization
            <Recommendations and Optimization details>
            """,
        agent=agent_personal_tax_consultant,
        tools=research_tools,
    )
    
    
    return Crew(
        agents=[agent_personal_tax_consultant],
        tasks=[task_consult],
        verbose=True,
    )
    