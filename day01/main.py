"""Day 1: Hello AI

This script sends a single prompt to Groq's hosted LLM via LangChain and prints
the model's response.
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

def main() -> None:
    """Run a single prompt against the Groq chat model and print the output."""

    # 1) Load environment variables from a local `.env` file.
    load_dotenv()

    # Optional safety check: fail fast with a friendly message if the key is missing.
    # This helps beginners understand what went wrong.
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "Missing GROQ_API_KEY. Add it to your .env file like: GROQ_API_KEY=..."
        )

    # 2) Initialize the LLM (Large Language Model).
    #
    # - `model` chooses which Groq-hosted model to use.
    # - `temperature` controls randomness/creativity:
    #     0.0 = more deterministic and factual
    #     1.0 = more creative and varied
    llm = ChatGroq(
        model="llama-3.1-8b-instant",  # other option: "llama3-70b-8192"
        temperature=0.7,
    )

    # 3) The input prompt (what you ask the AI).
    # Try changing this string to experiment.
    user_message = "Tell me a joke about computers."

    # 4) The execution (send prompt to Groq and wait for the reply).
    # `invoke()` returns an AIMessage object; the text is in `response.content`.
    print("Thinking...")
    response = llm.invoke(user_message)

    # 5) The output (print the model's reply).
    print("-" * 20)
    print(response.content)
    print("-" * 20)


if __name__ == "__main__":
    # This makes sure main() runs only when you execute the file directly:
    #   python day1_hello_ai.py
    main()