import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_agent

load_dotenv()

# Setup
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
python_tool = PythonREPLTool()
tools = [python_tool]
agent_executor = create_agent(llm, tools)

def run_agent_with_details(query):
    """Run the agent and display its thinking process"""
    print(f"\n{'='*60}")
    print(f"USER QUERY: {query}")
    print('='*60)
    
    result = agent_executor.invoke({"messages": [("user", query)]})
    
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
                        code = tool_call['args'].get('query', tool_call['args'])
                        print(f" CODE TO EXECUTE:\n{code}")
            elif msg.type == "tool":
                print(f"\n TOOL OUTPUT: {msg.content}")
    
    print(f"\n{'='*60}")
    print(f" FINAL ANSWER: {result['messages'][-1].content}")
    print('='*60)
    
    return result

if __name__ == "__main__":
    print("\n HOMEWORK CHALLENGES FOR DAY 23\n")
    print("  Python REPL can execute arbitrary code. Use with caution.\n")
    
    # Challenge 1: Recursive Factorial
    print("\n" + " CHALLENGE 1: RECURSIVE FACTORIAL" + "\n")
    query_1 = "Calculate the factorial of 12 using a recursive function."
    run_agent_with_details(query_1)
    
    print("\n" + "="*70 + "\n")
    
    # Challenge 2: Prime Numbers
    print("\n" + " CHALLENGE 2: PRIME NUMBERS" + "\n")
    query_2 = "Generate the first 20 prime numbers and display them."
    run_agent_with_details(query_2)
    
    print("\n" + "="*70 + "\n")
    
    # Challenge 3: Palindrome Check
    print("\n" + " CHALLENGE 3: PALINDROME CHECK" + "\n")
    query_3 = "Check if 'racecar' is a palindrome. Also check 'hello'."
    run_agent_with_details(query_3)
    
    print("\n" + "="*70 + "\n")
    
    # Challenge 4: Statistics
    print("\n" + " CHALLENGE 4: STATISTICS" + "\n")
    query_4 = "Calculate the mean, median, and mode of this list: [5, 2, 8, 2, 9, 1, 2, 15, 8]"
    run_agent_with_details(query_4)
    
    print("\n\n ALL HOMEWORK CHALLENGES COMPLETED!\n")
