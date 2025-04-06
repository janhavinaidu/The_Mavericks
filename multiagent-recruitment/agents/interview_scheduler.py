# agents/interview_scheduler.py

from ollama import Client
client = Client()

def generate_email(name, email, date="10 April 2025", time="3:00 PM", format="Google Meet"):
    prompt = f"""
    Compose a professional and friendly interview invitation email to {name} at {email}.
    Mention the interview will take place on {date} at {time} via {format}.
    Include: greeting, confirmation request, closing.
    """
    response = client.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']
