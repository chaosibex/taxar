from crewai import Agent, Task, Crew

def assemble_chart_crew():
    agent_charts = Agent(
        role="Data Analyst",
        goal="Extract out tax relief estimates for creating charts",
        backstory="""You experienced data analyst that is passionate in story telling using charts and graphs.""",
        allow_delegation=False,
    )
    
    task_extract_chart = Task(
        description="""
        1. Extract the tax relief and its amount from Personal Tax Consultant Tax Relief Breakdown table output: {recommend}
        2. Output the data in YAML, along with the tax consultant raw reply""",

        expected_output='''\
        1. Output in YAML following the example format below \
        2. There could be more than 3 relief, below is just an example \
        3. The output should be enclosed in ```yaml ```` \

        ```yaml 
            pie_chart:
                tax_relief_name:
                    - "NSman Self Relief"
                    - "Grandparent Caregiver Relief"
                    - "Life Insurance Relief"
                tax_relief_amount:
                    - "750"
                    - "3000"
                    - "1000"
        ```
        ''',
        agent=agent_charts,
    )
    
    return Crew(
        agents=[agent_charts],
        tasks=[task_extract_chart],
        verbose=True,
    )
    