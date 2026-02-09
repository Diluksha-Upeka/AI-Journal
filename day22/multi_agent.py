import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from langchain_community.tools import Tool
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 1. Setup Brain
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. Setup Tools
# Tool A: Search (for finding facts)
search_tool = TavilySearchResults()

# Tool B: Calculator (for doing math)
# Creating a custom calculator tool that evaluates Python expressions
def calculator(expression: str) -> str:
    """Useful for when you need to answer questions about math. 
    Input should be a valid Python mathematical expression like '2**0.23' or '45**0.23'."""
    try:
        # Safe evaluation of mathematical expressions
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

math_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Useful for when you need to answer questions about math. Input should be a valid Python mathematical expression."
)

# Combine them into a "Toolbox" - search and math
tools = [search_tool, math_tool]

# 3. Initialize the Agent
# Using the modern create_agent approach with ReAct pattern
# The AI will look at the tool descriptions to decide which one to pick.
agent = create_agent(llm, tools)

if __name__ == "__main__":
    print("Agent is ready. Solving complex problem...")
    print("="*50)
    
    # A generic LLM would fail this completely.
    # It requires: 
    # 1. Search (Find age)
    # 2. Math (Calculate power)
    query = "Who is the current President of France? Take his age and raise it to the power of 0.23."
    
    print(f"\nQuery: {query}\n")
    
    # Stream the agent's response to see its thinking (ReAct pattern)
    for chunk in agent.stream({"messages": [("human", query)]}, stream_mode="values"):
        if "messages" in chunk:
            last_message = chunk["messages"][-1]
            message_type = type(last_message).__name__
            
            # Show AI's Thought and Action
            if message_type == "AIMessage":
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"\n Thought: I need to use a tool")
                        print(f" Action: {tool_call['name']}")
                        print(f" Action Input: {tool_call['args']}")
                elif last_message.content:
                    # Final answer
                    print(f"\n Final Answer:")
                    print("-" * 50)
                    print(last_message.content)
            
            # Show Tool's Observation
            elif message_type == "ToolMessage":
                print(f"  Observation: {last_message.content[:200]}..." if len(last_message.content) > 200 else f"👁️  Observation: {last_message.content}")
    
    print("\n" + "="*50)