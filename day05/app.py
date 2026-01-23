import streamlit as st
import os
import json # to handle JSON data
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0.0 # Temp 0.0 is best for json
)

st.set_page_config(page_title="Resume Optimizr 📝✨", layout="wide")

st.title("Resume Optimizr 📝✨")
st.subheader("ATS Optimization and Scoring System")

resume_text = st.text_area("Paste your resume text here:", height=300)


def _parse_llm_json(text: str) -> dict:
    text = (text or "").strip()

    # Common: model wraps JSON in ```json ... ``` fences.
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```\s*$", "", text)
        text = text.strip()

    # Common: model adds a short preface; extract the largest JSON object.
    start = text.find("{")
    end = text.rfind("}")
    candidate = text[start : end + 1] if start != -1 and end != -1 and end > start else text

    return json.loads(candidate)

if st.button("Optimize My Resume"):
    if resume_text:
        with st.spinner("Calculating ATS score..."):

            # PROMPT - ask for JSON output (no markdown, no extra text)
            system_prompt = (
                "You are an expert technical recruiter and ATS specialist. "
                "Return ONLY valid JSON. Do not include markdown, code fences, or any extra keys."
            )
            user_prompt = f"""Analyze the resume text.

Return ONLY a valid JSON object with exactly these keys:
- score: integer from 0 to 100
- missing_keywords: array of strings
- summary: string (1 sentence)
- hiring_decision: string, either Yes or No

JSON format example (replace values, keep keys):
{{"score":75,"missing_keywords":["Kubernetes"],"summary":"...","hiring_decision":"No"}}

Resume Text:
{resume_text}
"""

            # EXECUTION
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ])

            try:
                data = _parse_llm_json(response.content)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(label="ATS Score", value=f"{data['score']}/100", delta = data['score'] - 75)

                with col2:
                    st.metric(label="Hiring Decision", value=data['hiring_decision'])

                with col3:
                    st.info(f"Summary: {data['summary']}")

                st.write("### Missing Critical Skills:")
                st.write("Consider adding these keywords to improve your resume:")
                for skill in data['missing_keywords']:
                    st.code(skill, language='text')
            
            except Exception as e:
                st.error("Failed to parse LLM response. Please try again.")
                st.caption(f"Parser error: {type(e).__name__}: {e}")
                with st.expander("Show raw model output"):
                    st.text(response.content)
    else:
        st.error("Please enter your resume text to optimize.")