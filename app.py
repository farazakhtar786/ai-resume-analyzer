import streamlit as st
import PyPDF2
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to analyze resume using AI
def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an AI hiring assistant.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Analyze the resume and provide:
    1. Resume match percentage
    2. Missing skills
    3. Suggestions to improve the resume
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer")

st.title("📄 AI Resume Analyzer & Job Matcher")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):
    if uploaded_file is not None and job_description.strip() != "":
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)
            st.success("Analysis Complete")
            st.write(result)
    else:
        st.warning("Please upload a resume and paste job description.")
