import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent

# 1. Load Keys
load_dotenv()

# 2. Setup the Brain (Groq Llama 3 is great for Agents)
# Using llama-3.3-70b-versatile which is currently supported
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 3. Setup the Tools
# We give the AI a "Search Tool"
search_tool = TavilySearchResults()

# We put tools in a list 
tools = [search_tool]

# 4. Initialize the Agent
# Using LangChain's create_agent (modern approach)
# This agent will automatically use the ReAct (Reasoning + Acting) pattern
agent = create_agent(llm, tools)

if __name__ == "__main__":
    print("Agent is ready. Asking about current events...")
    print("="*50)
    
    # A standard LLM would fail this because its training data is old.
    # An Agent searches for it.
    query = "Who won the cricket match between Sri Lanka and England in January 2026? Give me a summary of the match."
    
    print(f"\n Query: {query}\n")
    
    # Stream the agent's response to see its thinking
    for chunk in agent.stream({"messages": [("human", query)]}, stream_mode="values"):
        if "messages" in chunk:
            last_message = chunk["messages"][-1]
            
            # Only print AI messages and tool calls, not the raw tool results
            if hasattr(last_message, "content"):
                # Skip empty content
                if last_message.content and not last_message.content.startswith("[{"):
                    # Check if it's an AI message or the final answer
                    message_type = type(last_message).__name__
                    if message_type == "AIMessage":
                        # Check if there are tool calls
                        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                            print(" Agent is searching for information...")
                        elif last_message.content:
                            print("\nFinal Answer:")
                            print("-" * 50)
                            print(last_message.content)
    
    print("\n" + "="*50)