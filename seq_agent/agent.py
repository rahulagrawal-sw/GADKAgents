from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

research_agent_1 = LlmAgent(
    name = "research_agent_1",
    model = "gemini-2.5-flash",
    description= "Research Agent 1",
    instruction= """
    You are a financial research agent for National Stock Exchange for Equities. 
    You shortlist top 5 stocks for investment based on positive volume buyins
    """,
    tools= [google_search],
    output_key= "RESEARCH_OUTPUT_1"
)

research_agent_2 = LlmAgent(
    name = "research_agent_2",
    model = "gemini-2.5-flash",
    description= "Research Agent 2",
    instruction= "You are a financial news analyzer agent for National Stock Exchange Equities stocks",
    tools= [google_search],
    output_key= "RESEARCH_OUTPUT_2"
)

parallel_agent = ParallelAgent(
    name='parallel_agent',
    description= "Runs multiple research agents in parallel to gather information.",
    sub_agents=[research_agent_1, research_agent_2]
)

output_aggr_agent = LlmAgent(
    name = "output_aggregator_agent",
    model = "gemini-2.5-flash",
    description= "Output aggregator agent",
    instruction= """
    **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

     **Input Summaries:**

     *   **Top **
         {RESEARCH_OUTPUT_1}

     *   **Electric Vehicles:**
         {RESEARCH_OUTPUT_2}

     **Output Format:**

     ## Summary of investment advise

     ### Top stocks for investments are
     (Based on NSE positive volume buyins findings)
     [Synthesize and elaborate *only* on the input summary provided above.]

     ### Top stock news findings
     (Based on news analysis findings)
     [Synthesize and elaborate *only* on the news input summary provided above.]
""",
    output_key= "AGGR_OUTPUT"
)


root_agent = SequentialAgent(
    name='root_agent',
    description="Coordinates parallel research and synthesizes the results.",
    sub_agents=[parallel_agent, output_aggr_agent]
)

