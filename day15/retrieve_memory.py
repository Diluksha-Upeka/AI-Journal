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
index = pc.Index("memory-index")  # The name of the Pinecone index (database)

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
        top_k=3,                # Get top 3 matches
        include_metadata=True # This gives us the text back, not just the ID
    )

    # Display results with confidence threshold
    CONFIDENCE_THRESHOLD = 0.5  # Adjusted for better recall
    
    if search_results['matches']:
        print(f"\n All matches found:")
        for match in search_results['matches']:
            print(f"   [{match['score']:.3f}] {match['metadata']['text']}")
        
        relevant_matches = [m for m in search_results['matches'] if m['score'] >= CONFIDENCE_THRESHOLD]
        
        if relevant_matches:
            print(f"\n Relevant matches (≥{CONFIDENCE_THRESHOLD}):\n")
            for i, match in enumerate(relevant_matches, 1):
                score = match['score']
                text = match['metadata']['text']
                print(f" {i}. [{score:.3f}] {text}")
        else:
            print(f"\n No matches above threshold ({CONFIDENCE_THRESHOLD})")
    else:
        print(" No relevant memories found.")

if __name__ == "__main__":
    search_memory("What do I hate?")