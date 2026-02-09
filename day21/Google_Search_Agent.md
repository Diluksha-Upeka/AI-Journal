# Google Search Agent — Simple but In-depth Explanation 

> This is an AI generated document that provides a detailed explanation (Only for educational purposes)

**Summary:** This document explains a simple, practical pattern: an LLM-powered agent that uses a web-search tool to fetch up-to-date information. It covers the architecture, how it works (step-by-step), a working example (based on `search_agent.py`), setup and dependencies, common pitfalls we fixed, and guidance for extending it.

---

## Table of Contents

- Overview 
- Key components 
- How it works (step-by-step) 
- Example: key code snippets (and explanation) 
- Setup & dependencies 
- Glossary 

---

## Overview 

A "search agent" is an intelligent wrapper around an LLM that can call an external search tool during reasoning. Instead of relying solely on its training data (which can be stale), the agent issues live searches, uses the results to update its internal reasoning, and produces an answer grounded in current information.

Why use one? It adds factual currency and tool-backed verification to model outputs, reducing hallucinations when the user asks about recent events.

---

## Key components 

- **LLM (Language Model):** the reasoning engine (e.g., Groq Llama via `langchain_groq.ChatGroq`). Configure temperature, model name, etc.
- **Tool(s):** code that performs actions — here a web search tool (e.g., Tavily / a Google search wrapper). Tools return structured search results.
- **Agent orchestration:** glue code that decides when to call tools, pass results back to the model, and continue reasoning. Many libraries (LangChain, LangGraph) provide `create_agent` / `create_react_agent` helpers.
- **Streaming/IO loop:** optional—streams the agent's internal thinking and partial results so you can show progress in real time.

---

## How it works (step-by-step) 

1. **User query arrives.** The agent receives a natural-language question that may require fresh information ("Who won X match in January 2026?").
2. **LLM reasons and decides to use a tool.** Using the ReAct (Reason+Act) pattern or equivalent, the model internally decides whether a search is required.
3. **Tool call is executed.** The agent invokes the search tool with a well-formed query, receives results (snippets, links, metadata).
4. **LLM consumes results and continues reasoning.** The agent provides tool output to the LLM as context; the LLM integrates the data to craft a final answer.
5. **Final answer is returned (optionally with citations).** The model may cite sources and give a summary.

This loop (reason → act → observe → reason) can run multiple times until the agent resolves the question.

---

## Example: key code snippets (and explanation) 

This example mirrors the `search_agent.py` in this repo. It shows the minimal pieces you'll need:

```python
# 1. Initialize LLM
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. Initialize a search Tool
# Note: the preferred modern import for Tavily is `langchain_tavily` (see troubleshooting).
from langchain_community.tools.tavily_search import TavilySearchResults
search_tool = TavilySearchResults()

# 3. Create an agent
from langchain.agents import create_agent
tools = [search_tool]
agent = create_agent(llm, tools)

# 4. Ask a question and stream the agent's output (shows reasoning and final answer)
query = "Who won the cricket match between Sri Lanka and England in January 2026?"
for chunk in agent.stream({"messages": [("human", query)]}, stream_mode="values"):
    # process streaming chunks and print only AI messages or final answers
    ...
```

Notes:
- The `agent.stream(...)` loop typically yields intermediate "thoughts", tool calls, and final answers. In practice you filter for messages that are human-readable and ignore raw tool JSON unless you want to log/cite it.
- Keep the LLM temperature low (e.g., 0) for factual queries.

---

## Setup & dependencies 

Recommended Python packages (example):

```bash
pip install -U langchain langchain-groq langchain-tavily langchain-community
# Optionally: pip install langgraph (if you use LangGraph features)
```

Important environment items:
- Provider API keys (e.g., for Groq / LLM provider), stored in `.env` and loaded with `python-dotenv` via `load_dotenv()`.

How to run:
1. Activate your virtual environment.
2. Install dependencies.
3. Add API keys to `.env`.
4. Run: `python day21/search_agent.py`

---


## Glossary 

- **LLM:** Large Language Model.
- **ReAct:** A pattern where the model alternates between reasoning (thoughts) and actions (tool calls).
- **Tool:** Any callable function the agent can use (search, calc, DB query).
- **Streaming:** Receiving partial outputs from the agent as it processes.

---

## Further reading & references 

- LangChain docs: https://langchain.readthedocs.io/
- Package notes: `langchain-groq`, `langchain-tavily` (check package homepages for the latest usage)
- ReAct paper and agent design patterns (search for "ReAct LLM agent" for background)

---
