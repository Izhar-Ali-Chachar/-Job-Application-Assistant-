import requests
from langchain.tools import tool

@tool
def search_remote_jobs(keyword: str = "python") -> str:
    """
    Searches remote jobs from Remote OK by keyword (e.g., 'python', 'react').
    Returns a list of job titles and links.
    """
    try:
        response = requests.get("https://remoteok.com/api")
        data = response.json()[1:]  # Skip metadata record

        results = [
            f"- {job['position']} at {job['company']} ({job['location']})\n  {job['url']}"
            for job in data
            if keyword.lower() in job.get("tags", []) or keyword.lower() in job["position"].lower()
        ]

        return "\n".join(results[:10]) if results else "No jobs found for that keyword."

    except Exception as e:
        return f"Error fetching jobs: {e}"