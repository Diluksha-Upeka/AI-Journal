import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_agent

load_dotenv()

# 1. Setup Brain
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0) # temperature=0 for deterministic output

# 2. Setup Tools
# The "Python REPL" allows the LLM to execute Python code
# REPL = Read-Eval-Print Loop
python_tool = PythonREPLTool()

tools = [python_tool]   # List of tools available to the agent

# 3. Initialize Agent using the modern create_agent
agent_executor = create_agent(llm, tools)

# Helper function to show agent's reasoning
def run_agent_with_details(query):
    """Run the agent and display its thinking process"""
    print(f"\n{'='*60}")
    print(f"USER QUERY: {query}")
    print('='*60)
    
    result = agent_executor.invoke({"messages": [("user", query)]}) # Invoke the agent with the user query
    
    # Display all messages to show the reasoning process
    print("\n--- AGENT'S THINKING PROCESS ---")
    for i, msg in enumerate(result["messages"]):
        if hasattr(msg, 'type'):
            if msg.type == "human":
                print(f"\n USER: {msg.content}")
            elif msg.type == "ai":
                print(f"\n AGENT: {msg.content}")
                # Show tool calls if present
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        print(f"\n TOOL USED: {tool_call['name']}")
                        print(f" CODE TO EXECUTE:\n{tool_call['args'].get('code', tool_call['args'])}")
            elif msg.type == "tool":
                print(f"\n TOOL OUTPUT: {msg.content}")
    
    print(f"\n{'='*60}")
    print(f" FINAL ANSWER: {result['messages'][-1].content}")
    print('='*60)
    
    return result

if __name__ == "__main__":
    print(" Coder Agent is ready. Writing software...\n")
    print("  Python REPL can execute arbitrary code. Use with caution.\n")
    
    # Challenge 1: Sorting logic (Hard for LLMs to do in their head)
    query_1 = """
    Create a list of random numbers between 1 and 100. 
    Sort them in descending order. 
    Print the first 5 numbers.
    """
    
    # Challenge 2: String manipulation
    query_2 = "Reverse the string 'Artificial Intelligence' and count how many vowels are in it."
    
    run_agent_with_details(query_1)
    print("\n" + "-" * 70 + "\n")
    run_agent_with_details(query_2)
