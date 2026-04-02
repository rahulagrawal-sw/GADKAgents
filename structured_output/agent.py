import asyncio
from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService, session
from google.adk.runners import Runner

from google.genai import types

from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv(override=True)

APP_NAME = "agentwithstructuedoutput"
USER_ID = "rahul_12345"
SESSION_ID = "rahul_12345"


class city_details(BaseModel):
    city_name: str  #This will represent city_name
    population: int #This will hold population of a given city

class india_states(BaseModel):
    cities: list[city_details]


async def get_agent():
    root_agent = Agent(
        model='gemini-2.5-flash',
        name='root_agent',
        description='A helpful assistant for user questions.',
        instruction='Answer user questions to the best of your knowledge',
        output_schema=india_states,
        output_key="city_list_with_population",
    )
    return root_agent


async def main(user_query):
    # create a memory session
    session_service = InMemorySessionService()
    await session_service.create_session(app_name= APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # get root agent
    my_structured_output_agent = await get_agent()

    # create a runner
    runner = Runner(
        app_name=APP_NAME,
        agent=my_structured_output_agent,
        session_service=session_service
    )
    
     # format the query 
    user_content = types.Content(role = "user", parts= [types.Part(text=user_query)])
    print("Running agent with query:", user_query)
    
    # run the runner
    events = runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_content
        )
    
    # print the response
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)

            current_session = await session_service.get_session(app_name = APP_NAME, user_id = USER_ID, session_id = SESSION_ID)
            cities_list_with_population = current_session.state.get(my_structured_output_agent.output_key)
            print("Agent Response - cities:", cities_list_with_population)


if __name__ == "__main__":
    user_query = "What's population of any 3 cities in Maharashtra state in India ?"
    asyncio.run(main(user_query))
