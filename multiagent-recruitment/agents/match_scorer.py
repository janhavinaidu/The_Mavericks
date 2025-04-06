# agents/match_scorer.py

from ollama import Client

client = Client(host='http://localhost:11434')

def calculate_match_score(jd_summary, resume_info):
    prompt = f"""
    Compare the following job description summary and resume information.
    Based on skills, experience, and education, give a match percentage (0-100%)
    and a short justification for the score.

    Job Description Summary:
    {jd_summary}

    Candidate Resume Information:
    {resume_info}

    Respond in the format:
    Match Score: X%
    Reason: ...
    """

    response = client.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
