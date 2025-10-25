import os
import io
import json
import argparse
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from openai import OpenAI

# Optional imports for file parsing (loaded at runtime in helpers)
# from pypdf import PdfReader
# import docx  # from python-docx

# -------------------------------------------------------------
# 1) Environment and OpenAI client
# -------------------------------------------------------------
load_dotenv()  # loads OPENAI_API_KEY and OPENAI_MODEL if present
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# -------------------------------------------------------------
# 2) Structured output schema (Pydantic)
# -------------------------------------------------------------
class Score(BaseModel):
    overall: int = Field(ge=0, le=100)
    ats_alignment: int = Field(ge=0, le=100)
    impact_quantification: int = Field(ge=0, le=100)
    tech_relevance: int = Field(ge=0, le=100)

class EditSuggestion(BaseModel):
    section: str
    before: Optional[str] = None
    after: str
    rationale: str

class RoleMatch(BaseModel):
    role: str
    fit_summary: str
    gaps: List[str]
    actions: List[str]

class CVAdvice(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    red_flags: List[str]
    ats_keywords: List[str]
    role_matches: List[RoleMatch]
    quantification_opportunities: List[str]
    project_recommendations: List[str]
    linkedin_headlines: List[str]
    tailored_summary_for_target_role: str
    edit_suggestions: List[EditSuggestion]
    score: Score

# -------------------------------------------------------------
# 3) Prompt templates (system + few-shot + user)
# -------------------------------------------------------------
SYSTEM_PROMPT = """
You are a senior tech recruiter and resume coach specializing in software roles.
Return ONLY JSON that strictly matches the given schema. Be specific, concise, and use action verbs.
Use New Zealand/Australia tech hiring context when relevant (ATS, skills, impact, compliance).
Focus on quantifying impact (%, $, time saved), modern stacks (cloud, AI/ML, data), and clarity.
"""

FEW_SHOT_CV = (
    "Edison Zhang — Projects: React + FastAPI app; Python data analysis; AWS basics.\n"
    "Experience: Volunteer Web Developer at NGO (2025), built OCR pipeline;\n"
    "Education: Master of Software Engineering (Yoobee, 2026 expected); MBA (2021).\n"
)

FEW_SHOT_JSON = {
  "summary": "Solid academic/vocational foundation with recent hands-on projects. Strong potential for full-stack roles.",
  "strengths": ["Full-stack stack exposure (React, FastAPI)", "Financial industry background", "Initiative via volunteering"],
  "gaps": ["Production-scale deployments", "Automated tests", "CI/CD depth"],
  "red_flags": ["Long bullet lists without impact metrics"],
  "ats_keywords": ["React", "TypeScript", "FastAPI", "PostgreSQL", "Docker", "AWS", "CI/CD", "Unit testing"],
  "role_matches": [
    {"role":"Junior Full-Stack Developer","fit_summary":"Strong fit with modern web stack and recent projects.",
     "gaps":["Deeper testing"],
     "actions":["Add pytest examples", "Containerize with Docker compose", "Show deploy URLs"]}
  ],
  "quantification_opportunities": [
    "State perf improvements (e.g., reduced API latency by 30%)",
    "Show user impact (e.g., 200+ monthly active users)",
    "Cost savings (e.g., $500/month via serverless)"
  ],
  "project_recommendations": [
    "Production-ready app with login, RBAC, and CI pipeline",
    "Small ML feature (resume keyword extractor)",
    "Cloud deploy to Render/Fly.io/AWS"
  ],
  "linkedin_headlines": [
    "Full-Stack Developer | React • FastAPI • AWS | Building data-driven apps",
    "Software Engineer (Full-Stack) | React/TypeScript • Python/APIs • Cloud"
  ],
  "tailored_summary_for_target_role": "Full-stack engineer with React/TypeScript and Python APIs, delivering data products and automation with cloud-first mindset.",
  "edit_suggestions": [
    {"section":"Experience","before":"Built web features","after":"Delivered 6 React features and 3 FastAPI endpoints; cut manual reconciliation by 30% using OCR.","rationale":"Add scope and measurable outcomes."}
  ],
  "score": {"overall": 78, "ats_alignment": 82, "impact_quantification": 65, "tech_relevance": 80}
}

USER_TEMPLATE = (
    "Analyze the following CV text and a target role, then return STRICT JSON for the schema.\n\n"
    "CV:\n{cv_text}\n\n"
    "TARGET_ROLE: {target_role}\n\n"
    "Requirements:\n"
    "- Give concrete, quantified, industry-relevant recommendations.\n"
    "- Assume NZ hiring context for ATS and tech stack.\n"
    "- Suggest modern keywords without keyword stuffing.\n"
    "- Provide edit suggestions with before/after and rationale.\n"
)

# -------------------------------------------------------------
# 4) Helpers: file text extraction
# -------------------------------------------------------------

def read_txt_bytes(b: bytes) -> str:
    """Decode TXT bytes to UTF-8 with fallback."""
    return b.decode("utf-8", errors="ignore")


def read_pdf_bytes(b: bytes) -> str:
    """Extract text from PDF bytes using pypdf."""
    try:
        from pypdf import PdfReader
    except Exception as e:
        raise RuntimeError("pypdf is required for PDF parsing. pip install pypdf") from e
    text = []
    reader = PdfReader(io.BytesIO(b))
    for page in reader.pages:
        try:
            text.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(text).strip()


def read_docx_bytes(b: bytes) -> str:
    """Extract text from DOCX bytes using python-docx."""
    try:
        import docx
    except Exception as e:
        raise RuntimeError("python-docx is required for DOCX parsing. pip install python-docx") from e
    tmp = io.BytesIO(b)
    document = docx.Document(tmp)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text_from_upload(upload: UploadFile) -> str:
    """Route file to appropriate reader based on extension/MIME."""
    name = (upload.filename or "").lower()
    content = upload.file.read()
    # Rewind not required for BytesIO usage; we read raw bytes once.
    if name.endswith(".pdf") or (upload.content_type == "application/pdf"):
        return read_pdf_bytes(content)
    if name.endswith(".docx") or (upload.content_type in {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"}):
        return read_docx_bytes(content)
    # Default to TXT
    return read_txt_bytes(content)

# -------------------------------------------------------------
# 5) FastAPI app (web UI with file upload)
# -------------------------------------------------------------
app = FastAPI(title="Week13 – CV Analyzer (OpenAI API, file upload)")

INDEX_HTML = """
<!doctype html><html><head>
<meta charset='utf-8'/><meta name='viewport' content='width=device-width, initial-scale=1'/>
<title>CV Analyzer (Week 13)</title>
<style>
body{max-width:960px;margin:2rem auto;font-family:system-ui,Arial}
textarea,input,select{width:100%;padding:.6rem;border:1px solid #d0d7de;border-radius:10px}
.card{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:12px 0}
.btn{padding:.6rem 1rem;border-radius:10px;background:#111;color:#fff;border:none;cursor:pointer}
pre{white-space:pre-wrap;word-wrap:break-word}
small{color:#6b7280}
</style>
</head><body>
<h1>LLM-Powered CV Analyzer</h1>
<div class='card'>
  <form method='post' action='/analyze' enctype='multipart/form-data'>
    <label>Target role (e.g., Junior Full-Stack Developer, Data Analyst)</label>
    <input name='target_role' value='Junior Full-Stack Developer' />
    <br/><br/>
    <label>Upload your CV (PDF/DOCX/TXT)</label>
    <input type='file' name='cv_file' accept='.pdf,.docx,.txt' />
    <div><small>You can upload a file OR paste text below; pasted text overrides if both are provided.</small></div>
    <br/>
    <label>Or paste CV text</label>
    <textarea name='cv_text' rows='14' placeholder='Paste your CV text here...'></textarea>
    <br/><br/>
    <button class='btn' type='submit'>Analyze</button>
  </form>
</div>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(INDEX_HTML)

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(cv_text: str = Form(""), target_role: str = Form("Junior Full-Stack Developer"), cv_file: UploadFile = File(None)):
    # Resolve CV text: prefer pasted text; otherwise try file upload.
    if not cv_text and cv_file is not None:
        try:
            cv_text = extract_text_from_upload(cv_file)
        except Exception as e:
            return HTMLResponse(f"<pre>File parsing error: {e}</pre>")
    if not cv_text:
        return HTMLResponse("<pre>No CV text provided. Upload a file or paste your CV text.</pre>")

    # Compose messages: system, few-shot, and user
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": FEW_SHOT_CV},
        {"role": "assistant", "content": json.dumps(FEW_SHOT_JSON)},
        {"role": "user", "content": USER_TEMPLATE.format(cv_text=cv_text, target_role=target_role)},
    ]

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        advice = CVAdvice(**data)  # Validate JSON against schema
    except (ValidationError, json.JSONDecodeError) as e:
        return HTMLResponse(f"<pre>Schema/JSON error: {e}</pre>")
    except Exception as e:
        return HTMLResponse(f"<pre>OpenAI error: {e}</pre>")

    # Render a minimal but readable HTML report from the structured advice
    role_cards = []
    for rm in advice.role_matches:
        g = ''.join(f"<li>{x}</li>" for x in rm.gaps)
        a = ''.join(f"<li>{x}</li>" for x in rm.actions)
        role_cards.append(
            f"<div class='card'><h3>{rm.role}</h3><p>{rm.fit_summary}</p><b>Gaps</b><ul>{g}</ul><b>Actions</b><ul>{a}</ul></div>"
        )

    edits = ''.join(
        f"<li><b>{e.section}</b><br/>Before: <pre>{(e.before or '').strip()}</pre>After: <pre>{e.after.strip()}</pre><i>{e.rationale}</i></li>"
        for e in advice.edit_suggestions
    )

    html = f"""
    <!doctype html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width, initial-scale=1'/>
    <title>CV Report</title>
    <style>body{{max-width:960px;margin:2rem auto;font-family:system-ui,Arial}} .card{{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:12px 0}} .pill{{display:inline-block;padding:.2rem .6rem;border:1px solid #d1d5db;border-radius:999px}}</style>
    </head><body>
    <h2>CV Analysis for: {target_role}</h2>
    <div class='card'><p>{advice.summary}</p></div>
    <div class='card'><h3>Strengths</h3><ul>{''.join(f'<li>{s}</li>' for s in advice.strengths)}</ul></div>
    <div class='card'><h3>Gaps</h3><ul>{''.join(f'<li>{g}</li>' for g in advice.gaps)}</ul></div>
    <div class='card'><h3>Red Flags</h3><ul>{''.join(f'<li>{r}</li>' for r in advice.red_flags)}</ul></div>
    <div class='card'><h3>ATS Keywords</h3><p>{', '.join(advice.ats_keywords)}</p></div>
    {''.join(role_cards)}
    <div class='card'><h3>Quantification Opportunities</h3><ul>{''.join(f'<li>{q}</li>' for q in advice.quantification_opportunities)}</ul></div>
    <div class='card'><h3>Project Recommendations</h3><ul>{''.join(f'<li>{p}</li>' for p in advice.project_recommendations)}</ul></div>
    <div class='card'><h3>LinkedIn Headlines</h3><ul>{''.join(f'<li>{h}</li>' for h in advice.linkedin_headlines)}</ul></div>
    <div class='card'><h3>Tailored Summary</h3><p>{advice.tailored_summary_for_target_role}</p></div>
    <div class='card'><h3>Edit Suggestions (Before → After)</h3><ul>{edits}</ul></div>
    <div class='card'><h3>Score</h3>
      <span class='pill'>Overall: {advice.score.overall}</span>
      <span class='pill'>ATS: {advice.score.ats_alignment}</span>
      <span class='pill'>Impact: {advice.score.impact_quantification}</span>
      <span class='pill'>Tech Relevance: {advice.score.tech_relevance}</span>
    </div>
    <a href='/'>Analyze another CV</a>
    </body></html>
    """
    return HTMLResponse(html)

# -------------------------------------------------------------
# 6) CLI mode (now supports --file)
# -------------------------------------------------------------

def read_file_to_text(path: str) -> str:
    """Read a file from disk and extract text based on extension."""
    p = path.lower()
    with open(path, "rb") as f:
        data = f.read()
    if p.endswith(".pdf"):
        return read_pdf_bytes(data)
    if p.endswith(".docx"):
        return read_docx_bytes(data)
    return read_txt_bytes(data)


def run_cli(file_path: Optional[str]):
    if file_path and os.path.exists(file_path):
        cv_text = read_file_to_text(file_path)
    else:
        print("CV Analyzer (CLI) — paste CV text (end with an empty line):")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            lines.append(line)
        cv_text = "\n".join(lines)
    if not cv_text:
        cv_text = FEW_SHOT_CV

    target_role = input("Target role (default 'Junior Full-Stack Developer'): ") or "Junior Full-Stack Developer"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": FEW_SHOT_CV},
        {"role": "assistant", "content": json.dumps(FEW_SHOT_JSON)},
        {"role": "user", "content": USER_TEMPLATE.format(cv_text=cv_text, target_role=target_role)},
    ]

    try:
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=0.4,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        advice = CVAdvice(**data)
    except Exception as e:
        print("Error:", e)
        return

    print("\n=== SUMMARY ===\n" + advice.summary)
    print("\n=== TOP KEYWORDS ===\n" + ", ".join(advice.ats_keywords))
    print("\n=== ROLE MATCHES ===")
    for rm in advice.role_matches:
        print(f"- {rm.role}: {rm.fit_summary}")
        if rm.gaps:
            print("  gaps:", "; ".join(rm.gaps))
        if rm.actions:
            print("  actions:", "; ".join(rm.actions))
    print("\n=== EDIT SUGGESTIONS ===")
    for e in advice.edit_suggestions:
        print(f"* {e.section} -> {e.after}  (why: {e.rationale})")
    print("\nSCORE:", advice.score.overall, "(ATS:", advice.score.ats_alignment, ", Impact:", advice.score.impact_quantification, ", Tech:", advice.score.tech_relevance, ")")

# Entrypoint for CLI flag
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode instead of web server')
    parser.add_argument('--file', type=str, help='Path to CV file (.pdf, .docx, .txt)')
    args = parser.parse_args()
    if args.cli:
        run_cli(args.file)
