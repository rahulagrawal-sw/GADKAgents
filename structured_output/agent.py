from google.adk.agents.llm_agent import Agent

from pydantic import BaseModel, Field

class city_details(BaseModel):
    city_name: str  #This will represent city_name
    population: int #This will hold population of a given city

class india_states(BaseModel):
    cities: list[city_details]


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    output_schema=india_states,
)
