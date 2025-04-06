from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PyPDF2 import PdfReader
import docx2txt
import re
import os
import sys

# Allow imports from parent directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.jd_summarizer import summarize_jd
from agents.resume_extractor import extract_resume_data
from agents.match_scorer import calculate_match_score
from utils.database import save_candidate

# ✅ Define app
app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Helper: Extract resume text
def extract_text_from_resume(file: UploadFile) -> str:
    content_type = file.content_type
    filename = file.filename.lower()

    if filename.endswith(".pdf") or content_type == "application/pdf":
        pdf_reader = PdfReader(file.file)
        return " ".join(page.extract_text() or "" for page in pdf_reader.pages)

    elif filename.endswith(".docx") or content_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        return docx2txt.process(file.file)

    elif filename.endswith(".txt") or content_type == "text/plain":
        return (file.file.read()).decode("utf-8")

    else:
        raise ValueError("Unsupported file format")

# ✅ Helper: Save candidate & email logic (runs in background)
def handle_shortlist(name, email, match_score, match_result):
    save_candidate(name, email, match_score, match_result)
    # You can add real email logic here later (SMTP, SendGrid, etc.)

# ✅ Endpoint
@app.post("/match")
async def match(
    background_tasks: BackgroundTasks,
    resume: UploadFile = File(...),
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None)
):
    try:
        resume_text = extract_text_from_resume(resume)
    except Exception as e:
        return {"error": f"Failed to read resume: {str(e)}"}

    if jd_file:
        jd_content = (await jd_file.read()).decode("utf-8")
    elif jd_text:
        jd_content = jd_text
    else:
        return {"error": "Job description not provided."}

    jd_summary = summarize_jd(jd_content)
    resume_info = extract_resume_data(resume_text)
    match_result = calculate_match_score(jd_summary, resume_info)

    try:
        match_score = int(re.search(r"Match Score:\s*(\d+)", match_result).group(1))
        name = re.search(r"Name:\s*(.+)", resume_info).group(1).strip()
        email = re.search(r"Email:\s*(.+)", resume_info).group(1).strip()
    except Exception:
        return {"error": "Failed to extract name, email, or score from resume."}

    email_preview = f"""
Dear {name},

Congratulations! Based on our AI system, you’ve been shortlisted with a match score of {match_score}%.

We’ll be in touch shortly.

Best,
Recruitment Team
"""

    if match_score >= 80:
        # ⏳ Run in background to avoid delay
        background_tasks.add_task(handle_shortlist, name, email, match_score, match_result)
        return {
            "name": name,
            "match_score": match_score,
            "shortlisted": True,
            "email": email_preview.strip()
        }

    return {
        "name": name,
        "match_score": match_score,
        "shortlisted": False,
        "email": None
    }
