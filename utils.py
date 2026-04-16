from PyPDF2 import PdfReader
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extract text from PDF
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Match score
def match_score(resume, job_desc):
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return score[0][0] * 100

# 🔥 Extract important keywords dynamically
def extract_keywords(text, top_n=20):
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform([text])
    words = tfidf.get_feature_names_out()
    scores = vectors.toarray()[0]

    word_scores = list(zip(words, scores))
    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)

    keywords = [word for word, score in sorted_words[:top_n]]
    return keywords

# Extract skills from resume (intersection)
def extract_resume_skills(resume_text, job_keywords):
    resume_words = set(resume_text.split())
    matched = [word for word in job_keywords if word in resume_words]
    return matched

# Missing skills
def missing_skills(resume_skills, job_keywords):
    return [skill for skill in job_keywords if skill not in resume_skills]

# Suggest improvements
def generate_suggestions(missing, score):
    suggestions = []

    if score < 50:
        suggestions.append("Your resume is not aligned with the job. Add relevant keywords and skills.")

    for skill in missing[:5]:
        suggestions.append(f"Consider adding or improving: {skill}")

    return suggestions