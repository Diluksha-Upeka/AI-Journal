import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from a local `.env` file.
load_dotenv()

# Optional safety check: fail fast with a friendly message if the key is missing.
# This helps beginners understand what went wrong.
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "Missing GROQ_API_KEY. Add it to your .env file like: GROQ_API_KEY=..."
    )

# Initialize the LLM (Large Language Model).
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # other option: "llama3-70b-8192"
    temperature=0.7,
)

# THE NEW PART: Define system prompts
messages = [
    # Define the system message to set the AI's persona
    SystemMessage(content="You are a sarcastic tech support guy from the 90s. You hate modern technology and think everything was better in 1999. Be rude but funny."),

    # Example user message
    HumanMessage(content="My computer won't turn on. What should I do?")
]

# Send the messages to the LLM and get the response
response = llm.invoke(messages)
# Print the model's reply
print("-" * 20)
print(response.content)

