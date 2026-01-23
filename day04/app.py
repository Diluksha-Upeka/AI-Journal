import streamlit as st              # streamlit for ui
import os                           # os for environment variables access
from dotenv import load_dotenv      # load environment variables from .env file
from langchain_groq import ChatGroq  # Groq LLM wrapper
from langchain_core.messages import HumanMessage, SystemMessage # Message types

load_dotenv()  

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0.5
)

# UI
st.title("Helpful Career Coach 🤖🔥")
st.write("Paste your resume below and get humble, constructive feedback")

# Input box
resume_text = st.text_area("Enter your resume here:", height=300)

# Button to trigger roasting
if st.button("Roast My Resume"):
    if resume_text:
        st.write("Analyzing your resume...")

        messages = [
            SystemMessage(content = "You are a career coach that provides constructive and humorous feedback on resumes. You are helpful and honest, but always kind."),
            HumanMessage(content = f"Resume: {resume_text}")
        ]

        response = llm.invoke(messages)

        # OUTPUT
        st.success("Here's your resume roast:")
        st.balloons()  # Fun visual effect
        st.write(response.content) # Display the roast
    else:
        st.error("Please enter your resume text before roasting.")