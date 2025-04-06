from ollama import Client

client = Client(host="http://localhost:11434")  # consistent across files

def summarize_jd(jd_text):
    client = Client()
    prompt = f"Summarize the following job description into:\n- Required Skills\n- Experience\n- Qualifications\n- Responsibilities\n\n{jd_text}"
    response = client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])

    return response['message']['content']
