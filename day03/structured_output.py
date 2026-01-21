# ETL PIPELINE (Extract, Transform, Load)

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from a local `.env` file.
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature = 0 # Temp = 0 is critical for JSON
)

# The messy input data
user_bio = "I built a robotics startup in San Francisco when I was 25. Now, at 30, I'm a software engineer who loves biking, painting, and playing the guitar."


# The prompt that forces JSON structured output

prompt = f"""
Extract the following information from the text below:
1. Name
2. Age
3. Project Name
4. Profession
5. City 
6. Hobbies (as a list)

Return the output as a SINGLE VALID JSON OBJECT. Don't write "Here is the JSON" or any other text. Just the JSON.

Text:
{user_bio}
"""

print("Extracting...")
response = llm.invoke([HumanMessage(content=prompt)])

try:
    # response.content should be a JSON string. json.loads will parse it into a Python dictionary.
    data = json.loads(response.content)

    print("___SUCCESS!Extracted Data___")
    print(f"Name: {data['Name']}")
    print(f"Age: {data['Age']}")
    print(f"First Hobby: {data['Hobbies'][0]}")
    print(f"City: {data['City']}")
    print(f"Profession: {data['Profession']}")
    print(f"Project Name: {data['Project Name']}")

except json.JSONDecodeError:
    print("Failed to parse JSON. Here's the raw response:")
    print("Raw Output:", response.content)