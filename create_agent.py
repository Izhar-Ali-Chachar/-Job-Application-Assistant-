from job_search_tool import search_remote_jobs
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

def get_jobs(text: str):
    tools = [search_remote_jobs]

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite-preview-06-17")

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True  # ✅ Add this
    )

    # ✅ Fix the input format to be a clear question
    input_text = f"What are some remote jobs related to: {text}?"

    result = agent_executor.invoke({"input": input_text})

    # Optional: Just return the output portion (instead of full result dict)
    if isinstance(result, dict) and "output" in result:
        return result["output"]
    return str(result)
