
import re
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python", "java", "c++", "sql", "html", "css",
    "javascript", "machine learning", "deep learning",
    "artificial intelligence", "data science", "data analysis",
    "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "excel", "power bi", "tableau",
    "git", "github", "flask", "streamlit", "nlp",
    "statistics", "mysql", "mongodb", "cloud computing",
    "aws", "react", "django", "computer vision",
    "data structures", "algorithms"
]


def extract_resume_text(uploaded_file):
    """Extract text from an uploaded PDF."""
    try:
        reader = PdfReader(uploaded_file)
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )
        return text.strip()
    except Exception as exc:
        raise ValueError("Unable to read this PDF file.") from exc


def extract_skills(text):
    """Find supported skills mentioned in text."""
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return found


def text_similarity(resume_text, job_description):
    """Calculate TF-IDF cosine similarity."""
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        score = cosine_similarity(
            vectors[0:1], vectors[1:2]
        )[0][0]
        return round(float(score) * 100, 2)
    except ValueError:
        return 0.0


def analyze_resume(resume_text, job_description):
    """Compare a resume with a job description."""
    if not resume_text.strip():
        raise ValueError("Resume contains no readable text.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    required_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in required_skills
        if skill not in resume_skills
    ]

    similarity = text_similarity(
        resume_text, job_description
    )

    if required_skills:
        skill_score = len(matched) / len(required_skills) * 100
        final_score = 0.6 * similarity + 0.4 * skill_score
    else:
        skill_score = None
        final_score = similarity

    return {
        "score": round(final_score, 2),
        "similarity": similarity,
        "skill_score": (
            round(skill_score, 2)
            if skill_score is not None else None
        ),
        "matched_skills": matched,
        "missing_skills": missing
    }


def rank_resumes(resumes, job_description):
    """Analyze resumes and rank them by estimated match score."""
    results = []

    for resume in resumes:
        analysis = analyze_resume(
            resume["text"], job_description
        )

        results.append({
            "filename": resume["filename"],
            **analysis
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    for rank, result in enumerate(results, start=1):
        result["rank"] = rank

    return results
