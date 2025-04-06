# EXISTING CODE (Don't remove)
import re
from agents.jd_summarizer import summarize_jd
from agents.resume_extractor import extract_resume_data
from agents.match_scorer import calculate_match_score
from utils.database import init_db, save_candidate

init_db()

with open('data/jds/sample.txt', 'r') as file:
    jd_text = file.read()

with open('data/resumes/sample_resume.txt', 'r') as file:
    resume_text = file.read()

jd_summary = summarize_jd(jd_text)
resume_info = extract_resume_data(resume_text)
match_result = calculate_match_score(jd_summary, resume_info)

print("📝 JD Summary:\n", jd_summary)
print("\n📄 Resume Info:\n", resume_info)
print("\n📊 Match Result:\n", match_result)

match_score = int(re.search(r"Match Score:\s*(\d+)", match_result).group(1))

if match_score >= 80:
    name = re.search(r"Name:\s*(.+)", resume_info).group(1).strip()
    email = re.search(r"Email:\s*(.+)", resume_info).group(1).strip()
    save_candidate(name, email, match_score, match_result)
    print(f"\n✅ Candidate {name} shortlisted with score {match_score}%")
else:
    print("\n❌ Candidate not shortlisted.")

# 🆕 ADD THIS AFTER EVERYTHING ABOVE
# INTERVIEW SCHEDULER AGENT
from agents.interview_scheduler import generate_email
import sqlite3

def send_emails():
    conn = sqlite3.connect('database/recruitment.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM shortlisted")
    candidates = cursor.fetchall()

    for name, email in candidates:
        print("\n📧 Generating interview email for:", name)
        email_content = generate_email(name, email)
        print(email_content)

    conn.close()

send_emails()
