# agents/resume_extractor.py

from ollama import Client

client = Client(host='http://localhost:11434')

def extract_resume_data(resume_text):
    prompt = f"""
    Extract the following information from the candidate's resume:
    - Name
    - Email
    - Skills
    - Education
    - Experience
    - Certifications

    Resume Text:
    {resume_text}
    """

    response = client.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
