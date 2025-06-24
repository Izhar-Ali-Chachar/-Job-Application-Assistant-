from create_agent import get_jobs
from extract_job_search_query import extract_job_search_query

text = extract_job_search_query('resume.pdf')

print(get_jobs(text))