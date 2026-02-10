# Day 23: The "Coder" Agent (Python REPL)
**Date:** Wednesday, Feb 11, 2026

## What We Built Today
An AI agent that can **write and execute its own Python code** to solve problems. This is called a Python REPL (Read-Eval-Print Loop) Agent.

## Why This Matters
- LLMs can't do complex calculations or sorting in their "head"
- By giving them the ability to write and run code, they can:
  - Sort lists
  - Check palindromes
  - Do complex math
  - Process data
  - Build algorithms on the fly

## How It Works
1. **User asks a question**: "What is the 10th Fibonacci number?"
2. **Agent writes Python code**: Creates a loop or recursive function
3. **System executes the code**: Runs it safely in the environment
4. **Agent reads the output**: "The answer is 55"

## Example Output
```
USER: Create a list of random numbers between 1 and 100. 
         Sort them in descending order. Print the first 5 numbers.

AGENT: [Decides to use Python_REPL]

TOOL USED: Python_REPL
CODE TO EXECUTE:
import random; 
numbers = [random.randint(1, 100) for _ in range(10)]; 
numbers.sort(reverse=True); 
print(numbers[:5])

TOOL OUTPUT: [96, 78, 72, 64, 58]

FINAL ANSWER: This code generates 10 random numbers between 1 and 100,
                 sorts them in descending order, and prints the first 5.
```

## Key Components

### 1. The Brain
```python
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
```
Using temperature=0 for consistent, deterministic code generation.

### 2. The Tool
```python
python_tool = PythonREPLTool()
```
From `langchain-experimental` - allows executing Python code.

### 3. The Agent
```python
agent_executor = create_agent(llm, tools)
```
The modern LangChain agent that can use tools autonomously.

## What Makes This Powerful
This is how features like **GitHub Copilot** and **code assistants** work:
- They don't "guess" the answer
- They write valid algorithms
- They execute on your CPU
- They read and interpret the output

## Safety Notes 
- The Python REPL can execute **any** Python code
- Don't ask it to delete files or system operations
- Modern OS permissions usually block dangerous operations
- Use in controlled environments

## Extra Tasks

### Challenge 1: Recursive Factorial
Ask the agent: "Calculate the factorial of 12 using a recursive function."

### Challenge 2: Safety Test
**DO NOT TRY THIS**: Asking it to delete system files could be dangerous!

### Challenge 3: More Complex Tasks
Try these queries:
- "Generate the first 20 prime numbers"
- "Check if 'racecar' is a palindrome"
- "Calculate the mean, median, and mode of [5, 2, 8, 2, 9, 1, 2]"
- "Create a simple text-based calculator that can add, subtract, multiply, and divide"

## Technical Notes

### Dependencies
```bash
pip install langchain langchain-experimental langchain-groq
```

## Running the Agent
```bash
python day23/coder_agent.py
```

## What's Next?
Now that your agent can:
- Use calculators (Day 22)
- Write and execute code (Day 23)

What if it could also:
- Read files?
- Search the web?
- Query databases?
- Control your computer?

The possibilities are endless! This is the foundation of **Autonomous AI Agents** that can perform complex tasks by writing and executing code on their own.

## Engineering Insight
**You just built an Autonomous Software Engineer.**

It can:
- ✅ Understand requirements (NLP)
- ✅ Write algorithms (Code generation)
- ✅ Execute and test (REPL)
- ✅ Debug and iterate (Feedback loop)

This is the foundation of AI-assisted programming!
