import asyncio

from dotenv import load_dotenv
load_dotenv(override=True)

from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

from google.genai import types

APP_NAME = "agent_with_runner_app"
USER_ID = "rahul_12345"
SESSION_ID = "rahul_12345"

async def get_agent():

    # create a toolset
    toolset = McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://127.0.0.1:8000/mcp"
        )
    )

    root_agent = Agent(
        model='gemini-2.5-flash',
        name='root_agent_2',
        description='Google ADK Agent with Runner & Tools - get_weather',
        instruction='You are a helpful assistant',
        tools=[toolset]
    )

    return root_agent, toolset

async def main(user_query):
    # create a memory session
    session_service = InMemorySessionService()
    await session_service.create_session(app_name= APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # get root agent
    my_agent, toolset = await get_agent()

    # create a runner
    runner = Runner(
        app_name=APP_NAME,
        agent=my_agent,
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

    # close MCP Server
    await toolset.close()


if __name__ == "__main__":
    user_query = "How is weather in Delhi?"
    asyncio.run(main(user_query))