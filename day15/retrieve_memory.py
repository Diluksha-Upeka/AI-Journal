import os
import time
from dotenv import load_dotenv
import google.genai
from pinecone import Pinecone

load_dotenv()

# 2. Setup Google (The Embedder)
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

# 3. Setup Pinecone (The Database)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("memory-index")  # The name of the Pinecone index

def search_memory(query):
    print(f"Searching for: '{query}'...")

    # Embed the query to get its vector representation
    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[query]
    )
    query_vector = result.embeddings[0].values

    # Search in Pinecone
    search_results = index.query(
        vector=query_vector,
        top_k=1,                # Single best match
        include_metadata=True # This gives us the text back, not just the ID
    )

    # Display results
    if search_results['matches']:
        best_match = search_results['matches'][0]
        score = best_match['score'] # How confident is the AI? (0.0 to 1.0)
        text = best_match['metadata']['text']
        
        print(f" Found match (Confidence: {score:.2f})")
        print(f" Fact: {text}")
    else:
        print(" No relevant memories found.")

if __name__ == "__main__":
    search_memory("What do I hate?")