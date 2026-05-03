import asyncio

from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.genai import types

from dotenv import load_dotenv

load_dotenv(override=True)

APP_NAME = "My_LLM_Agent_App"
USER_ID = "rahul"
SESSION_ID = "12345"

def get_agent() -> Agent:
    my_llm_agent = Agent(
        name = "MyLLMAgent",
        description="My LLM Agent for runner example",
        model="gemini-2.5-flash",
        instruction="You are a helpful assistant. Give clear and concise answers"
    )
    return my_llm_agent


async def run_agent(user_input_query: str) -> str:
    output_result = ""
    # STEP - 1: Create InMemory SessionService
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # STEP - 2: ADK Agent
    my_llm_agent = get_agent()

    # STEP - 3: Runner
    runner = Runner(
        app_name = APP_NAME,
        agent = my_llm_agent,
        session_service = session_service,
    )

    # STEP - 4: Prepare user query content
    user_msg = types.Content(role = "user", parts= [types.Part(text=user_input_query)])

    # STEP - 5: Run the runner
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_msg)

    # STEP - 6: Print the response
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(f"final_response: {final_response}")
            output_result = final_response
    
    print(f"output_result: {output_result}")
    return output_result


if __name__ == "__main__":
    user_input_query = "2+5"
    print(f"user_input_query: {user_input_query}")
    asyncio.run(run_agent(user_input_query))