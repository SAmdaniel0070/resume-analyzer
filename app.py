import streamlit as st
from utils import extract_text, clean_text, match_score, extract_keywords, extract_resume_skills, missing_skills, generate_suggestions

st.set_page_config(page_title="AI Resume Analyzer")

st.title("🚀 Smart Resume Analyzer")
st.write("Analyze your resume against any job description using AI")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if resume_file is None or job_desc.strip() == "":
        st.warning("Please upload resume and enter job description")
    
    else:
        try:
            # Extract text
            resume_text = extract_text(resume_file)
            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_desc)

            st.subheader("📄 Resume Preview")
            st.write(resume_text[:300])

            # Score
            score = match_score(resume_clean, job_clean)

            # 🔥 Dynamic keyword extraction
            job_keywords = extract_keywords(job_clean)

            # Match skills
            resume_skills = extract_resume_skills(resume_clean, job_keywords)

            # Missing skills
            missing = missing_skills(resume_skills, job_keywords)

            # Suggestions
            suggestions = generate_suggestions(missing, score)

            # Output
            st.subheader("📊 Results")
            st.write(f"### Match Score: {score:.2f}%")

            if score > 70:
                st.success("Strong match!")
            elif score > 50:
                st.warning("Moderate match")
            else:
                st.error("Low match")

            st.write("### ✅ Skills Matched")
            st.write(resume_skills)

            st.write("### ❌ Missing Skills")
            st.write(missing[:10])

            st.write("### 💡 Suggestions")
            for s in suggestions:
                st.write(f"- {s}")

        except Exception as e:
            st.error(f"Error: {e}")