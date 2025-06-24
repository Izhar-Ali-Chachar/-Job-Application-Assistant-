def get_jobs(query: str):
    from job_search_tool import search_remote_jobs
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain import hub
    from langchain.agents import create_react_agent, AgentExecutor

    tools = [search_remote_jobs]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite-preview-06-17")
    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    result = agent_executor.invoke({'input': query})

    # Try to extract jobs list
    jobs = result.get("output", result)

    if isinstance(jobs, list):
        formatted = "\n🧑‍💻 Remote Jobs Found:\n\n"
        for i, job in enumerate(jobs, 1):
            title = job.get("title", "No title")
            link = job.get("link", "No link")
            formatted += f"{i}. {title}\n   🔗 {link}\n"
        return formatted

    elif isinstance(jobs, str):
        return jobs.strip()  # Raw string output
    else:
        return f"Unexpected output format:\n{jobs}"
